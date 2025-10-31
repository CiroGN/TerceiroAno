#!/usr/bin/env python3
"""
instacart_son_dask.py

Single-file script to run a SON-style Market Basket Analysis (Apriori per-partition + global counting)
using Dask. Reads Instacart CSVs from a data directory, computes frequent itemsets and association rules,
and writes results to output files (CSV/Parquet).

Usage:
    python instacart_son_dask.py --data-dir ./data --min-support 0.001 --min-confidence 0.3 --nworkers 4 --nthreads 1

Notes:
- The script expects the following files in DATA_DIR:
    orders.csv, order_products__prior.csv, products.csv
- It's recommended to use product_id (integers) for processing. Product names are joined only when saving.
- You need Dask and dependencies: dask[complete], dask[distributed], pandas, pyarrow, fastparquet
"""

import os
import math
import argparse
from collections import Counter
from itertools import combinations
from pprint import pprint
import logging

import dask
import dask.dataframe as dd
from dask.distributed import Client

from functools import partial
from itertools import chain


# ---------------------------
# Helpers: Apriori local + SON
# ---------------------------
def apriori_local(transactions, support_threshold):
    """
    transactions: iterable of lists (transactions in this partition)
    support_threshold: absolute count threshold (int) for local frequent itemsets
    returns: list of frozenset itemsets (candidates found locally)
    """
    transactions = list(transactions)
    counts = Counter()
    for t in transactions:
        for item in set(t):
            counts[item] += 1
    L1 = {frozenset([item]) for item, c in counts.items() if c >= support_threshold}
    freq_itemsets = set(L1)
    current_L = L1
    k = 2
    while current_L:
        candidates = set()
        prev = list(current_L)
        for i in range(len(prev)):
            for j in range(i+1, len(prev)):
                union = prev[i] | prev[j]
                if len(union) == k:
                    candidates.add(union)
        cand_counts = Counter()
        for t in transactions:
            tset = set(t)
            for c in candidates:
                if c.issubset(tset):
                    cand_counts[c] += 1
        current_L = {c for c, cnt in cand_counts.items() if cnt >= support_threshold}
        freq_itemsets |= current_L
        k += 1
    return list(freq_itemsets)

def run_son(trans_bag, min_support_rel=0.001, verbose=True):
    """
    trans_bag: dask.bag of transactions (each transaction is a list of item ids)
    min_support_rel: relative support (e.g., 0.001 = 0.1%)
    returns: (frequent_itemsets: dict{frozenset: count}, total_tx)
    """
    # total de transações
    total_tx = trans_bag.count().compute()
    if verbose:
        print("Total transactions:", total_tx)

    # suporte global mínimo absoluto
    global_support_count = max(1, int(math.ceil(min_support_rel * total_tx)))

    npart = trans_bag.npartitions
    if verbose:
        print("Partitions:", npart, "Global support count:", global_support_count)

    # tamanho de cada partição
    part_sizes = trans_bag.map_partitions(lambda it: sum(1 for _ in it)).compute()

    # wrapper do apriori para cada partição
    def apriori_partition_wrapper(partition, global_support_count, part_size, idx=None):
        if idx is not None:
            print(f"Processing partition {idx+1}/{len(part_sizes)}")
        return apriori_local(list(partition), max(1, int(math.ceil(global_support_count * (part_size / total_tx)))))

    # processa cada partição como delayed
    candidate_lists_delayed = []
    for i, part_delayed in enumerate(trans_bag.to_delayed()):
        sz = part_sizes[i]
        candidate_lists_delayed.append(
            dask.delayed(apriori_partition_wrapper)(part_delayed, global_support_count, sz, i)
        )


    # computa todos os candidatos das partições
    candidate_lists_nested = dask.compute(*candidate_lists_delayed)

    # achata a lista de listas de candidatos
    candidate_lists = [c for sublist in candidate_lists_nested for c in sublist]

    # únicos candidatos
    unique_candidates = set(map(frozenset, candidate_lists))
    if verbose:
        print("Unique candidates from partitions:", len(unique_candidates))

    candidates_list = list(unique_candidates)

    # contagem global dos candidatos
    def map_partition_count(partition):
        counts = Counter()
        for t in partition:
            tset = set(t)
            for c in candidates_list:
                if c.issubset(tset):
                    counts[c] += 1
        return list(counts.items())

    part_counts = trans_bag.map_partitions(map_partition_count).compute()

    # achata a lista de listas de forma segura
    all_counts = list(chain.from_iterable(
        lst if isinstance(lst, list) else [lst] for lst in part_counts
    ))

    total_counts = Counter()
    for item in all_counts:
        if isinstance(item, tuple) and len(item) == 2:
            c, cnt = item
            total_counts[c] += cnt


    # filtra frequent itemsets pelo suporte global
    frequent_itemsets = {c: cnt for c, cnt in total_counts.items() if cnt >= global_support_count}
    if verbose:
        print("Frequent itemsets found:", len(frequent_itemsets))

    return frequent_itemsets, total_tx

# ---------------------------
# Rules generation
# ---------------------------
def all_nonempty_subsets(itemset):
    s = list(itemset)
    for r in range(1, len(s)):
        for comb in combinations(s, r):
            yield frozenset(comb)

def generate_rules(frequent_itemsets, total_tx, min_confidence=0.3):
    support = {k: v / total_tx for k, v in frequent_itemsets.items()}
    rules = []
    for itemset, count in frequent_itemsets.items():
        if len(itemset) < 2:
            continue
        for A in all_nonempty_subsets(itemset):
            B = itemset - A
            if not B:
                continue
            A_count = frequent_itemsets.get(A, None)
            if not A_count:
                continue
            conf = frequent_itemsets[itemset] / A_count
            lift = conf / (support.get(B, 1e-9))
            if conf >= min_confidence:
                rules.append({
                    'antecedent': tuple(sorted(A)),
                    'consequent': tuple(sorted(B)),
                    'support': support[itemset],
                    'confidence': conf,
                    'lift': lift,
                    'support_count': frequent_itemsets[itemset]
                })
    rules_sorted = sorted(rules, key=lambda x: (-x['lift'], -x['confidence']))
    return rules_sorted

# ---------------------------
# Main pipeline
# ---------------------------
def build_transactions_bag(op_prior_ddf, npartitions=200):
    """
    Cria um dask.bag de transações (listas de product_id) a partir de um DataFrame de pedidos.
    """
    # Converte para DataFrame pandas por partição e agrega localmente
    def df_to_transactions(pdf):
        grouped = pdf.groupby('order_id')['product_id'].apply(list).reset_index()
        return grouped

    # Aplica a função por partição (mantém DataFrame)
    grouped_ddf = op_prior_ddf.map_partitions(df_to_transactions)

    # Converte para Dask Bag (só a coluna de listas de produtos)
    bag = grouped_ddf['product_id'].to_bag()
    bag = bag.repartition(npartitions)
    return bag

def main(args):
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(asctime)s %(levelname)s %(message)s")
    # Start Dask client (local) -- for cluster, set --scheduler-address
    if args.scheduler_address:
        client = Client(args.scheduler_address)
    else:
        client = Client(n_workers=args.nworkers, threads_per_worker=args.nthreads, memory_limit=args.memory_limit)
    logging.info("Dask client started: %s", client)

    DATA_DIR = args.data_dir
    # check expected files
    expected = ['order_products__prior.csv', 'products.csv', 'orders.csv']
    for f in expected:
        path = os.path.join(DATA_DIR, f)
        if not os.path.exists(path):
            logging.warning("Expected file not found: %s", path)

    # Read CSVs with dask
    op_prior = dd.read_csv(os.path.join(DATA_DIR, 'order_products__prior.csv'),
                           dtype={'order_id': 'int64', 'product_id': 'int64', 'add_to_cart_order': 'int64', 'reordered': 'int64'})
    products = dd.read_csv(os.path.join(DATA_DIR, 'products.csv'),
                           dtype={'product_id': 'int64', 'product_name': 'object', 'aisle_id': 'int64', 'department_id': 'int64'})

    # Build transactions bag (using product_id)
    trans_bag = build_transactions_bag(op_prior[['order_id', 'product_id']], npartitions=args.npartitions)
    logging.info("Transactions bag created. Partitions: %s", trans_bag.npartitions)

    # Run SON
    frequent_itemsets, total_tx = run_son(trans_bag, min_support_rel=args.min_support, verbose=args.verbose)

    # Generate rules
    rules = generate_rules(frequent_itemsets, total_tx, min_confidence=args.min_confidence)

    # Prepare output directory
    out_dir = args.output_dir
    os.makedirs(out_dir, exist_ok=True)

    # Save frequent itemsets summary (CSV)
    import pandas as pd
    rows = []
    for itemset, cnt in frequent_itemsets.items():
        rows.append({'itemset': ','.join(map(str, sorted(itemset))), 'support_count': cnt, 'support_rel': cnt / total_tx})
    df_freq = pd.DataFrame(rows).sort_values('support_count', ascending=False)
    freq_csv = os.path.join(out_dir, 'frequent_itemsets.csv')
    df_freq.to_csv(freq_csv, index=False)
    logging.info("Frequent itemsets saved to %s (rows=%d)", freq_csv, len(df_freq))

    # Save rules
    df_rules = pd.DataFrame(rules)
    rules_csv = os.path.join(out_dir, 'association_rules.csv')
    df_rules.to_csv(rules_csv, index=False)
    logging.info("Association rules saved to %s (rows=%d)", rules_csv, len(df_rules))

    # Optional: map product_id -> product_name for readability (save top rules with names)
    try:
        prod_df = products[['product_id', 'product_name']].compute()
        id_to_name = dict(zip(prod_df['product_id'], prod_df['product_name']))
        def name_tuple(tup):
            return tuple(id_to_name.get(int(x), str(x)) for x in tup)
        df_rules['antecedent_names'] = df_rules['antecedent'].apply(lambda x: name_tuple(eval(x) if isinstance(x,str) else x))
        df_rules['consequent_names'] = df_rules['consequent'].apply(lambda x: name_tuple(eval(x) if isinstance(x,str) else x))
        rules_named_csv = os.path.join(out_dir, 'association_rules_named.csv')
        df_rules.to_csv(rules_named_csv, index=False)
        logging.info("Named rules saved to %s", rules_named_csv)
    except Exception as e:
        logging.warning("Could not map product names: %s", e)

    print("Done. Outputs written to:", out_dir)
    print("Total transactions:", total_tx)
    print("Frequent itemsets found:", len(frequent_itemsets))
    print("Rules generated (>= min_confidence):", len(rules))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Instacart SON + Dask Market Basket Analysis")
    parser.add_argument('--data-dir', type=str, default='./data', help='Path to Instacart CSVs')
    parser.add_argument('--output-dir', type=str, default='./output', help='Directory to write outputs')
    parser.add_argument('--min-support', type=float, default=0.001, help='Relative min support (e.g., 0.001)')
    parser.add_argument('--min-confidence', type=float, default=0.3, help='Min confidence for association rules')
    parser.add_argument('--nworkers', type=int, default=4, help='Dask local cluster: number of workers')
    parser.add_argument('--nthreads', type=int, default=1, help='Threads per worker')
    parser.add_argument('--memory-limit', type=str, default='4GB', help='Memory limit per worker')
    parser.add_argument('--npartitions', type=int, default=200, help='Number of partitions for transactions bag')
    parser.add_argument('--scheduler-address', type=str, default=None, help='If connecting to external Dask scheduler, provide address')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    args = parser.parse_args()
    main(args)
