import re

# PATH do arquivo (ajuste se necessário)
FILE_PATH = "modelo.txt"

# ---------- utilitários ----------
def float_eq(a, b, eps=1e-9):
    return abs(a - b) <= eps

def fmt1(x):
    """Formata números com 1 casa decimal; None -> 'None'"""
    if x is None:
        return "None"
    try:
        xf = float(x)
    except:
        return "None"
    return "{:.1f}".format(xf)

def fmt(x):
    """Formatação para debug/valores variáveis (6 casas se não inteiro)"""
    try:
        xf = float(x)
    except:
        return "None"
    if float_eq(round(xf), xf):
        return str(int(round(xf)))
    return "{:.6f}".format(xf)

# ---------- parser robusto (ajustado para retornar A original também) ----------
def Ler_Modelo(arquivo):
    """
    Lê o arquivo e retorna:
    nova_c (lista) : custos das variáveis EXPANDIDAS (ordem 1..n)
    nova_A (lista de listas) : matriz A expandida (linhas)
    b (lista) : RHS
    Sinal (lista) : operadores das restrições ("<=", ">=", "=")
    nova_VD (lista) : nomes das variáveis expandidas em ordem
    VD_orig (lista) : nomes originais (x1..xN)
    transform_map (dict) : original_var -> list of (trans_var_name, factor)
    A_orig (lista de listas) : matriz A na ordem das variáveis originais (VD)
    """
    with open(arquivo, "r", encoding="utf-8") as f:
        linhas = [ln.rstrip() for ln in f.readlines()]

    # remover cabeçalhos vazios iniciais
    while linhas and linhas[0].strip() == "":
        linhas.pop(0)

    if not linhas:
        raise ValueError("Arquivo vazio.")

    # 1) Ler FO (linha que começa com MAX ou MIN)
    fo_line = None
    fo_idx = None
    for i, ln in enumerate(linhas):
        if ln.strip() == "":
            continue
        if re.match(r'^\s*(MAX|MIN)\b', ln, re.I):
            fo_line = ln.strip()
            fo_idx = i
            break
    if fo_line is None:
        raise ValueError("FO (MAX/MIN) não encontrada.")

    # remover linhas antes da FO e a própria FO da lista remanescente
    linhas = linhas[fo_idx:]
    fo_line = linhas.pop(0).strip()
    # pular possíveis linhas vazias
    while linhas and linhas[0].strip() == "":
        linhas.pop(0)

    m = re.match(r'^(MAX|MIN)\s+(.*)$', fo_line, re.I)
    if not m:
        raise ValueError("Formato FO inválido.")
    sentido = m.group(1).upper()
    expr = m.group(2)

    # extrair termos: captura coef e variável (ex: "10 x10", "-3 x2", "0 x3")
    termos = re.findall(r'([+-]?\s*\d+(?:\.\d+)?)\s*(x\d+)', expr)
    VD = []
    c = []
    for coef_str, var in termos:
        coef = float(coef_str.replace(" ", ""))
        VD.append(var)
        c.append(coef)

    if sentido == "MIN":
        c = [-ci for ci in c]

    # 2) Ler restrições: até encontrar linha que começa com 'x' definindo domínios
    restricoes = []
    while linhas:
        if linhas[0].strip() == "":
            linhas.pop(0)
            continue
        # detecta início das definições de domínio (linhas começando com xN)
        if re.match(r'^\s*x\d+\b', linhas[0], re.I):
            break
        restricoes.append(linhas.pop(0).strip())

    A = []
    b = []
    Sinal = []

    for r in restricoes:
        # achar operador relacional
        mrel = re.search(r'(<=|>=|=)', r)
        if not mrel:
            raise ValueError("Restrição sem relacional: " + r)
        rel = mrel.group(1)
        lhs = r[:mrel.start()].strip()
        rhs_str = r[mrel.end():].strip()
        try:
            rhs = float(rhs_str)
        except:
            raise ValueError("RHS inválido na restrição: " + r)

        # parse lhs com regex robusto (permite floats)
        termos_lhs = re.findall(r'([+-]?\s*\d+(?:\.\d+)?)\s*(x\d+)', lhs)
        # montar dicionário var->coef
        d = {}
        for coef_str, var in termos_lhs:
            coef = float(coef_str.replace(" ", ""))
            d[var] = coef
            if var not in VD:
                VD.append(var)
                c.append(0.0)

        # montar linha com colunas na ordem VD atual
        row = [0.0] * len(VD)
        for j, var in enumerate(VD):
            if var in d:
                row[j] = d[var]
        # se VD teve extensão por restrição, ajustar linhas anteriores
        for prev in A:
            if len(prev) < len(VD):
                prev.extend([0.0] * (len(VD) - len(prev)))
        A.append(row)
        b.append(rhs)
        Sinal.append(rel)

    # Salva A original (na ordem VD)
    A_orig = [list(r) for r in A]

    # 3) Ler domínios (linhas restantes)
    dominios = {v: ">=" for v in VD}
    while linhas:
        ln = linhas.pop(0).strip()
        if ln == "":
            continue
        parts = ln.split()
        if len(parts) >= 2:
            var = parts[0]
            tail = " ".join(parts[1:]).lower()
            if "livre" in tail:
                dominios[var] = "livre"
            elif "<= 0" in tail or "<=0" in tail:
                dominios[var] = "<="
            elif ">= 0" in tail or ">=0" in tail:
                dominios[var] = ">="
            elif parts[1] in ("<=", ">=") and len(parts) == 3 and parts[2] == "0":
                dominios[var] = parts[1]
            else:
                # busca por tokens
                if "<=" in ln:
                    dominios[var] = "<="
                elif ">=" in ln:
                    dominios[var] = ">="
                else:
                    dominios[var] = ">="

    # 4) Expandir variáveis segundo domínio
    nova_VD = []
    nova_c = []
    transform_map = {}  # original_var -> list of (trans_var_name, factor)

    for i, var in enumerate(VD):
        dom = dominios.get(var, ">=")
        if dom == ">=":
            nova_VD.append(var)
            nova_c.append(c[i])
            transform_map[var] = [(var, 1.0)]
        elif dom == "<=":
            # x <= 0  -> x = -y, y >=0
            y = var + "_neg"
            nova_VD.append(y)
            nova_c.append(-c[i])
            transform_map[var] = [(y, -1.0)]
        elif dom.lower() == "livre":
            p = var + "_pos"
            n = var + "_neg"
            nova_VD.append(p); nova_VD.append(n)
            nova_c.append(c[i]); nova_c.append(-c[i])
            transform_map[var] = [(p, 1.0), (n, -1.0)]
        else:
            # default
            nova_VD.append(var)
            nova_c.append(c[i])
            transform_map[var] = [(var, 1.0)]

    # ajustar matriz A conforme expansão
    nova_A = []
    for row in A:
        new_row = []
        for j, var in enumerate(VD):
            dom = dominios.get(var, ">=")
            val = row[j]
            if dom == ">=":
                new_row.append(val)
            elif dom == "<=":
                new_row.append(-val)
            elif dom.lower() == "livre":
                new_row.append(val)
                new_row.append(-val)
            else:
                new_row.append(val)
        nova_A.append(new_row)

    return nova_c, nova_A, b, Sinal, nova_VD, VD, transform_map, A_orig

# PARTE 2/4

# ---------- construir tableau fase 1 (ajustado) ----------
def build_tableau_phase1_from_matrix(A, b, Sinal, n_vars):
    """
    Constrói o tableau de fase 1 (cada linha representa uma restrição).
    Retorna tableau, total_vars, artificials, slack_indices, cons_for_print
    tableau row format: [basic_index(float), cb, xb, coeffs(list index 0 unused -> 1..total_vars)]
    """
    m = len(A)
    add = 0
    for rel in Sinal:
        if rel == "<=":
            add += 1
        elif rel == ">=":
            add += 2
        elif rel == "=":
            add += 1
    total_vars = n_vars + add

    tableau = []
    artificials = []
    slack_indices = []
    nxt = n_vars

    cons_for_print = []

    for i in range(m):
        rowA = A[i]
        coeffs = [0.0] * (total_vars + 1)
        for j in range(len(rowA)):
            coeffs[j+1] = float(rowA[j])
        rel = Sinal[i]
        rhs = float(b[i])

        cons_for_print.append((coeffs[:], rel, rhs))

        if rel == "<=":
            nxt += 1
            coeffs[nxt] = 1.0
            slack_indices.append(nxt)
            # variável básica: folga (nxt)
            tableau.append([float(nxt), 0.0, rhs, coeffs])
        elif rel == ">=":
            # excesso then artificial
            nxt += 1
            coeffs[nxt] = -1.0  # excesso
            nxt += 1
            coeffs[nxt] = 1.0   # artificial
            artificials.append(nxt)
            tableau.append([float(nxt), 1.0, rhs, coeffs])
        else:  # "="
            nxt += 1
            coeffs[nxt] = 1.0
            artificials.append(nxt)
            tableau.append([float(nxt), 1.0, rhs, coeffs])

    return tableau, total_vars, artificials, slack_indices, cons_for_print

# ---------- compute zj and rel ----------
def compute_zj_rel(tableau, costs, total_vars):
    zj = [0.0] * (total_vars + 1)
    for row in tableau:
        cb = row[1]
        coeffs = row[3]
        for j in range(1, total_vars + 1):
            zj[j] += cb * coeffs[j]
    rel = [0.0] * (total_vars + 1)
    for j in range(1, total_vars + 1):
        rel[j] = costs.get(j, 0.0) - zj[j]
    return zj, rel

# ---------- pivot ----------
def pivot(tableau, r, col, total_vars):
    pv = tableau[r][3][col]
    if float_eq(pv, 0.0):
        raise Exception("Pivot zero.")
    tableau[r][2] = tableau[r][2] / pv
    for j in range(1, total_vars + 1):
        tableau[r][3][j] = tableau[r][3][j] / pv
    for i in range(len(tableau)):
        if i == r:
            continue
        factor = tableau[i][3][col]
        if float_eq(factor, 0.0):
            continue
        tableau[i][2] = tableau[i][2] - factor * tableau[r][2]
        for j in range(1, total_vars + 1):
            tableau[i][3][j] = tableau[i][3][j] - factor * tableau[r][3][j]

# ---------- imprimir iteração ----------
def print_iteration(it, tableau, total_vars):
    print(f"\n----- Iteração {it} -----")
    header = ["B", "CB", "XB"] + [f"x{j}" for j in range(1, total_vars + 1)]
    print("\t".join(header))
    for (basic, cb, xb, coeffs) in tableau:
        row = [f"x{int(basic)}", fmt(cb), fmt(xb)]
        row += [fmt(coeffs[j]) for j in range(1, total_vars + 1)]
        print("\t".join(row))
    print()

# ---------- função para remover colunas artificiais do tableau ----------
def remove_artificial_columns(tableau, artificials, total_vars):
    """
    Remove colunas correspondentes a variáveis artificiais do tableau.
    Retorna: (tableau_modificado, new_total_vars, old_to_new_index_map, kept_list)
    - old_to_new_index_map: dicionário {old_index: new_index}
    - kept_list: lista de índices antigos que foram mantidos (ordem preservada)
    """
    # lista de índices que vamos manter (1..total_vars) exceto artificiais
    kept = [j for j in range(1, total_vars + 1) if j not in artificials]
    new_total = len(kept)
    # mapeamento old->new (1-based)
    old_to_new = {old: new_i+1 for new_i, old in enumerate(kept)}

    # atualizar cada linha do tableau: reconstruir coeffs sem colunas artificiais
    for row in tableau:
        old_coeffs = row[3]
        new_coeffs = [0.0] * (new_total + 1)
        for old in kept:
            new_coeffs[old_to_new[old]] = old_coeffs[old]
        row[3] = new_coeffs

        # atualizar índice da variável básica se ela foi mantida
        basic_old = int(row[0])
        if basic_old in old_to_new:
            row[0] = float(old_to_new[basic_old])
        else:
            # basic era artificial (não mapeado) -> marcar como 0 e CB=0
            row[0] = float(0)
            row[1] = 0.0

    return tableau, new_total, old_to_new, kept

# PARTE 3/4

# ---------- simplex loop (min or max) ----------
def simplex_loop(tableau, costs, total_vars, mode="max", max_iters=1000):
    it = 0
    while True:
        it += 1
        zj, rel = compute_zj_rel(tableau, costs, total_vars)
        print_iteration(it, tableau, total_vars)
        rel_str = ", ".join([f"x{j}:{fmt(rel[j])}" for j in range(1, total_vars + 1)])
        print("Cj - Zj:", rel_str)
        # escolher entrada
        entering = -1
        if mode == "max":
            best = 0.0
            for j in range(1, total_vars + 1):
                if rel[j] > best + 1e-12:
                    best = rel[j]
                    entering = j
        else:  # min
            best = 0.0
            for j in range(1, total_vars + 1):
                if rel[j] < best - 1e-12:
                    best = rel[j]
                    entering = j
        if entering == -1:
            z_value = sum(row[1] * row[2] for row in tableau)
            print("Ótimo atingido. Z =", fmt(z_value))
            return True
        # razão mínima
        leaving = -1
        min_ratio = None
        for i, row in enumerate(tableau):
            aij = row[3][entering]
            if aij > 1e-12:
                ratio = row[2] / aij
                if min_ratio is None or ratio < min_ratio - 1e-12:
                    min_ratio = ratio
                    leaving = i
        if leaving == -1:
            print("Problema ilimitado detectado.")
            return False
        print(f"Entra: x{entering} | Sai: x{int(tableau[leaving][0])} (linha {leaving+1})")
        print(f"Pivot: ({leaving},{entering}) = {fmt(tableau[leaving][3][entering])}")
        pivot(tableau, leaving, entering, total_vars)
        tableau[leaving][0] = float(entering)
        tableau[leaving][1] = costs.get(entering, 0.0)
        if it >= max_iters:
            print("Máximo de iterações atingido.")
            return False

# ---------- duas fases usando Ler_Modelo (ajustado para LHS com A_orig e correção de transição) ----------
def two_phase_solve(file_path):
    nova_c, nova_A, b, Sinal, nova_VD, VD_orig, transform_map, A_orig = Ler_Modelo(file_path)
    n_vars = len(nova_VD)

    tableau, total_vars, artificials, slacks, cons_for_print = build_tableau_phase1_from_matrix(nova_A, b, Sinal, n_vars)

    # custos fase1: artificiais = 1 (minimizar soma)
    costs1 = {j: 0.0 for j in range(1, total_vars + 1)}
    for a in artificials:
        if a <= total_vars:
            costs1[a] = 1.0

    print("\n=== FASE I (minimizar soma artificiais) ===")

    # ajustar cb das linhas (CB = custo da básica) para fase1
    for row in tableau:
        basic = int(row[0])
        row[1] = costs1.get(basic, 0.0)

    ok1 = simplex_loop(tableau, costs1, total_vars, mode="min")

    if not ok1:
        print("Fase I falhou ou problema ilimitado.")
        return None

    # calcular valor da fase1
    phase1_val = 0.0
    for row in tableau:
        phase1_val += row[1] * row[2]

    print("Valor Fase I (soma artificiais) =", fmt(phase1_val))

    if not float_eq(phase1_val, 0.0):
        print("Problema inviável (Fase I > 0).")
        return None

    # --- Remover artificiais da base quando possível (tenta pivotar se XB==0) ---
    for i, row in enumerate(tableau):
        basic = int(row[0])
        if basic in artificials:
            if float_eq(row[2], 0.0):
                replaced = False
                for j in range(1, total_vars + 1):
                    if j not in artificials and not float_eq(row[3][j], 0.0):
                        pivot(tableau, i, j, total_vars)
                        tableau[i][0] = float(j)
                        tableau[i][1] = 0.0
                        replaced = True
                        break
                if not replaced:
                    tableau[i][1] = 0.0
            else:
                print("Inconsistência: artificial básica com XB != 0")
                return None

    # --- TRANSIÇÃO ADICIONAL PARA FASE II: REMOVER COLUNAS ARTIFICIAIS ---
    # Neste ponto já tentamos remover artificiais da base. Agora eliminamos
    # as colunas artificiais do tableau para evitar inconsistências na Fase II.

    if artificials:
        # remover colunas artificiais do tableau e ajustar total_vars
        tableau, total_vars, old_to_new, kept_list = remove_artificial_columns(tableau, artificials, total_vars)

        # reconstruir costs2 mapeando índices antigos -> novos
        # primeiro cria costs2_old com base em nova_c (e zeros para colunas extras)
        # NOTE: costs2_old size should be equal to antiga total_vars (antes de remoção)
        # mas aqui já temos apenas nova_c length; vamos criar um mapa antigo presumindo
        # que nova_c corresponde aos primeiros n_vars colunas originais.
        costs2_old = {}
        # reconstruct costs2_old for old indices 1..(n_vars + extras)
        # We'll set for original variables (1..n_vars) their costs, others 0
        for old_idx in range(1, total_vars + len(artificials) + 1):
            costs2_old[old_idx] = 0.0
        for idx, val in enumerate(nova_c):
            j = idx + 1
            if j in costs2_old:
                costs2_old[j] = float(val)

        # mapear costs2_old para costs2_new (no novo espaço sem artificiais)
        costs2 = {}
        for old_idx, new_idx in old_to_new.items():
            costs2[new_idx] = costs2_old.get(old_idx, 0.0)

        # atualizar os CB (custos das variáveis básicas) usando novo índice da básica
        for row in tableau:
            basic_idx = int(row[0])
            if basic_idx == 0:
                # linha com basic inválido (restante de artificial) -> CB=0
                row[1] = 0.0
            else:
                row[1] = costs2.get(basic_idx, 0.0)

    else:
        # se não há artificiais, apenas montamos costs2 normalmente
        costs2 = {j: 0.0 for j in range(1, total_vars + 1)}
        for idx, val in enumerate(nova_c):
            j = idx + 1
            if j <= total_vars:
                costs2[j] = float(val)

        # ajustar CB das linhas com os custos da Fase II
        for row in tableau:
            basic = int(row[0])
            row[1] = costs2.get(basic, 0.0)

    print("\n=== FASE II (maximizar objetivo transformado) ===")
    # agora podemos rodar simplex_loop no espaço sem artificiais com costs2
    ok2 = simplex_loop(tableau, costs2, total_vars, mode="max")

    if not ok2:
        print("Fase II falhou ou ilimitado.")
        return None

    # extrair solução (valores das variáveis transformadas)
    solution = [0.0] * (total_vars + 1)
    for (basic, cb, xb, coeffs) in tableau:
        bi = int(basic)
        if bi >= 0 and bi < len(solution):
            solution[bi] = xb

    # calcular valor objetivo Z
    z = 0.0
    for j in range(1, total_vars + 1):
        z += costs2.get(j, 0.0) * solution[j]

    # reconstruir valores das variáveis originais (VD_orig) a partir de transform_map
    # Nota: nova_VD tem as variáveis transformadas na ordem inicial (antes de remoção)
    trans_index = {name: idx + 1 for idx, name in enumerate(nova_VD)}  # name -> index (1-based)
    orig_values = {}
    for orig in VD_orig:
        parts = transform_map.get(orig, [(orig, 1.0)])
        val = 0.0
        for tname, factor in parts:
            if tname in trans_index:
                idx = trans_index[tname]
                if idx < len(solution):
                    val += factor * solution[idx]
                else:
                    # se índice maior que solution (por remoção) assumir 0
                    val += 0.0
        orig_values[orig] = val

    # calcular LHS para cada restrição usando A_orig e orig_values
    lhs_list = []
    for i, (coeffs_original, rel, rhs) in enumerate(cons_for_print):
        lhs = 0.0
        if i < len(A_orig):
            row_orig = A_orig[i]
            for j, var in enumerate(VD_orig):
                coef = row_orig[j] if j < len(row_orig) else 0.0
                lhs += coef * orig_values.get(var, 0.0)
        else:
            # fallback: compute from expanded coeffs and solution
            for j in range(1, len(solution)):
                lhs += coeffs_original[j] * solution[j]
        lhs_list.append(lhs)

    # calcular XB por linha a partir do tableau (valor da variável básica dessa linha)
    xb_list = [tableau[i][2] if i < len(tableau) else 0.0 for i in range(len(cons_for_print))]

    return {
        "Z": z,
        "solution_transformed": solution,
        "orig_values": orig_values,
        "nova_VD": nova_VD,
        "VD_orig": VD_orig,
        "lhs_list": lhs_list,
        "xb_list": xb_list,
        "cons_for_print": cons_for_print
    }
# PARTE 4/4

# ---------- main - Lógica de impressão ajustada ----------
def main():
    res = two_phase_solve(FILE_PATH)

    if res is None:
        print("Não foi possível resolver o modelo.")
        return

    Z = res["Z"]
    orig_values = res["orig_values"]
    VD_orig = res["VD_orig"]
    lhs_list = res["lhs_list"]
    xb_list = res["xb_list"]
    cons_for_print = res["cons_for_print"] # (coeffs, rel, rhs)

    # imprimir no formato solicitado
    print("\nSolução\n")
    print("FO: {}".format(fmt1(Z)))

    # garantir ordem x1..xN conforme VD_orig
    def index_of(name):
        m = re.match(r'x(\d+)', name)
        if m:
            return int(m.group(1))
        try:
            return VD_orig.index(name) + 1
        except:
            return 9999
    VD_sorted = sorted(VD_orig, key=index_of)
    for var in VD_sorted:
        val = orig_values.get(var, 0.0)
        print(f"{var} = {fmt1(val)}")

    print()
    # IMPRESSÃO DAS RESTRIÇÕES CORRIGIDA: Rk = LHS <= XB <= RHS
    for i in range(len(lhs_list)):
        # Obter o sinal e o RHS original da restrição i
        coeffs, rel, rhs = cons_for_print[i]

        # O valor calculado do lado esquerdo (LHS_calc)
        lhs_calc = lhs_list[i]

        # O valor da variável básica (XB) da linha no tableau final
        xb = xb_list[i]

        if rel == "=":
            lhs_str = fmt1(rhs)
            rhs_str = fmt1(rhs)
        elif rel == ">=":
            lhs_str = fmt1(lhs_calc)
            rhs_str = "None"
        elif rel == "<=":
            lhs_str = "None"
            rhs_str = fmt1(rhs)
        else:
            lhs_str = fmt1(lhs_calc)
            rhs_str = fmt1(rhs)

        print(f"R{i+1} = {lhs_str} <= {fmt1(xb)} <= {rhs_str}")

if __name__ == "__main__":
    main()