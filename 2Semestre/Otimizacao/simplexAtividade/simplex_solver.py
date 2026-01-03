import re
import os

class SolucionadorSimplex:
    def __init__(self):
        self.tableau = []
        self.cabecalhos = []
        self.M = 10**7
        self.mapa_variaveis = {}
        self.variaveis_basicas = []
        self.num_linhas = 0
        self.num_colunas = 0
        self.num_variaveis_decisao = 0
        self.variaveis_negativas = set()
        self.variaveis_livres = set()
        self.tipo_otimizacao = 'MAX'
        self.restricoes = []

    def _dividir_variaveis_livres(self, coeficientes):
        novos = {}
        for var, val in coeficientes.items():
            if var in self.variaveis_livres:
                novos[f"{var}_pos"] = val
                novos[f"{var}_neg"] = -val
            else:
                novos[var] = val
        return novos

    def _parse_expressao(self, expr):
        expr = expr.replace(" ", "")
        if not expr.startswith('+') and not expr.startswith('-'):
            expr = '+' + expr
        padrao = re.compile(r'([+-])(\d*\.?\d*)?([a-zA-Z]+\d*)')
        encontrados = padrao.findall(expr)
        coef = {}
        for sinal, num, var in encontrados:
            if not var and not num:
                continue
            valor = 1.0
            if num:
                valor = float(num)
            if sinal == '-':
                valor = -valor
            if var in coef:
                coef[var] += valor
            else:
                coef[var] = valor
        return coef

    def carregar_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as f:
            linhas = [l.strip() for l in f if l.strip()]
        self.variaveis_negativas = set()
        self.variaveis_livres = set()
        linhas_limites = []
        linhas_equacoes = []
        for linha in linhas:
            eh_limite = False
            if 'livre' in linha.lower() or 'free' in linha.lower():
                eh_limite = True
            elif re.match(r'^[a-zA-Z]+\d*\s*(<=|>=)\s*0$', linha):
                eh_limite = True
            if eh_limite:
                linhas_limites.append(linha)
            else:
                linhas_equacoes.append(linha)
        for linha in linhas_limites:
            if 'livre' in linha.lower() or 'free' in linha.lower():
                partes = linha.split()
                var = partes[0]
                self.variaveis_livres.add(var)
            elif '<=' in linha and '0' in linha:
                var = linha.split('<=')[0].strip()
                self.variaveis_negativas.add(var)
        linha_obj = linhas_equacoes[0]
        if linha_obj.upper().startswith("MIN"):
            self.tipo_otimizacao = 'MIN'
        else:
            self.tipo_otimizacao = 'MAX'
        expr_obj = re.sub(r'^(MAX|MIN)\s*', '', linha_obj, flags=re.IGNORECASE)
        coef_obj = self._parse_expressao(expr_obj)
        for var in list(coef_obj.keys()):
            if var in self.variaveis_negativas:
                coef_obj[var] = -coef_obj[var]
            if self.tipo_otimizacao == 'MIN':
                coef_obj[var] = -coef_obj[var]
        coef_obj = self._dividir_variaveis_livres(coef_obj)
        todas_vars = set(coef_obj.keys())
        self.restricoes = []
        for linha in linhas_equacoes[1:]:
            operador = None
            if '<=' in linha:
                operador = '<='
            elif '>=' in linha:
                operador = '>='
            elif '=' in linha:
                operador = '='
            if not operador:
                continue
            lhs, rhs = linha.split(operador)
            coef_lhs = self._parse_expressao(lhs)
            valor_rhs = float(rhs)
            for var in list(coef_lhs.keys()):
                if var in self.variaveis_negativas:
                    coef_lhs[var] = -coef_lhs[var]
            coef_lhs = self._dividir_variaveis_livres(coef_lhs)
            todas_vars.update(coef_lhs.keys())
            self.restricoes.append({'coef': coef_lhs, 'tipo': operador, 'rhs': valor_rhs})
        def chave_ord(x):
            m = re.search(r'\d+', x)
            n = int(m.group()) if m else 0
            s = 0
            if '_neg' in x:
                s = 1
            if '_pos' in x:
                s = 2
            return (n, s)
        vars_ordenadas = sorted(list(todas_vars), key=chave_ord)
        self.mapa_variaveis = {v: i for i, v in enumerate(vars_ordenadas)}
        self.num_variaveis_decisao = len(vars_ordenadas)
        n_entraves = 0
        n_excedentes = 0
        n_artificiais = 0
        configuracao_linhas = []
        for r in self.restricoes:
            if r['tipo'] == '<=':
                n_entraves += 1
                configuracao_linhas.append(('entrave', n_entraves, r))
            elif r['tipo'] == '>=':
                n_excedentes += 1
                n_artificiais += 1
                configuracao_linhas.append(('excedente_artificial', n_excedentes, n_artificiais, r))
            elif r['tipo'] == '=':
                n_artificiais += 1
                configuracao_linhas.append(('artificial', n_artificiais, r))
        total_vars = self.num_variaveis_decisao + n_entraves + n_excedentes + n_artificiais
        self.num_colunas = total_vars
        self.num_linhas = len(self.restricoes) + 1
        self.tableau = [[0.0] * (self.num_colunas + 1) for _ in range(self.num_linhas)]
        self.cabecalhos = vars_ordenadas[:]
        for i in range(1, n_entraves + 1):
            self.cabecalhos.append(f's{i}')
        for i in range(1, n_excedentes + 1):
            self.cabecalhos.append(f'e{i}')
        for i in range(1, n_artificiais + 1):
            self.cabecalhos.append(f'a{i}')
        self.cabecalhos.append('Sol')
        for var in vars_ordenadas:
            self.tableau[0][self.mapa_variaveis[var]] = -coef_obj.get(var, 0.0)
        atual_entrave = self.num_variaveis_decisao
        atual_excedente = self.num_variaveis_decisao + n_entraves
        atual_artificial = self.num_variaveis_decisao + n_entraves + n_excedentes
        linhas_artificiais = []
        idx = 1
        for cfg in configuracao_linhas:
            tipo = cfg[0]
            restr = cfg[-1]
            for var, val in restr['coef'].items():
                col = self.mapa_variaveis[var]
                self.tableau[idx][col] = val
            self.tableau[idx][-1] = restr['rhs']
            if tipo == 'entrave':
                self.tableau[idx][atual_entrave] = 1.0
                self.variaveis_basicas.append(f's{cfg[1]}')
                atual_entrave += 1
            elif tipo == 'excedente_artificial':
                self.tableau[idx][atual_excedente] = -1.0
                self.tableau[idx][atual_artificial] = 1.0
                self.tableau[0][atual_artificial] = self.M
                self.variaveis_basicas.append(f'a{cfg[2]}')
                linhas_artificiais.append((idx, atual_artificial))
                atual_excedente += 1
                atual_artificial += 1
            elif tipo == 'artificial':
                self.tableau[idx][atual_artificial] = 1.0
                self.tableau[0][atual_artificial] = self.M
                self.variaveis_basicas.append(f'a{cfg[1]}')
                linhas_artificiais.append((idx, atual_artificial))
                atual_artificial += 1
            idx += 1
        for r_idx, c_idx in linhas_artificiais:
            mult = self.tableau[0][c_idx]
            for j in range(len(self.tableau[0])):
                self.tableau[0][j] -= mult * self.tableau[r_idx][j]

    def mostrar_tableau(self, iteracao):
        if iteracao < 2:
            print(f"\n--- Iteracao {iteracao} ---")
            cab = " | ".join([f"{h:>7}" for h in self.cabecalhos])
            print(cab)
            print("-" * len(cab))
            rotulos = [' Z'] + [f"{b:>2}" for b in self.variaveis_basicas]
            for i, linha in enumerate(self.tableau):
                linha_str = " | ".join([f"{val:>7.1f}" for val in linha])
                rot = rotulos[i] if i < len(rotulos) else f"L{i}"
                print(f"{rot:<3} | {linha_str}")

    def resolver(self):
        print(f"\n>>> Resolvendo problema de {self.tipo_otimizacao} <<<")
        it = 0
        self.mostrar_tableau(it)
        max_it = 5000
        while it < max_it:
            menor = 0
            coluna_pivo = -1
            for j in range(self.num_colunas):
                val = self.tableau[0][j]
                if val < menor - 1e-7:
                    menor = val
                    coluna_pivo = j
                    break
            if coluna_pivo == -1:
                break
            menor_ratio = float('inf')
            linha_pivo = -1
            for i in range(1, self.num_linhas):
                rhs = self.tableau[i][-1]
                coef = self.tableau[i][coluna_pivo]
                if coef > 1e-9:
                    ratio = rhs / coef
                    if ratio < menor_ratio:
                        menor_ratio = ratio
                        linha_pivo = i
            if linha_pivo == -1:
                print("\n>>> Problema ilimitado! <<<")
                return
            self.variaveis_basicas[linha_pivo - 1] = self.cabecalhos[coluna_pivo]
            pivo = self.tableau[linha_pivo][coluna_pivo]
            for j in range(len(self.tableau[0])):
                self.tableau[linha_pivo][j] /= pivo
            for i in range(self.num_linhas):
                if i != linha_pivo:
                    fator = self.tableau[i][coluna_pivo]
                    for j in range(len(self.tableau[0])):
                        self.tableau[i][j] -= fator * self.tableau[linha_pivo][j]
            it += 1
            if it % 100 == 0:
                print(f"Iteracao {it}...")
        print("\nSolução\n")
        valor_z = self.tableau[0][-1]
        if self.tipo_otimizacao == 'MIN':
            valor_z = -valor_z
        print(f"FO: {valor_z:.1f}")
        valores_raw = {}
        for i in range(1, self.num_linhas):
            nome_bas = self.variaveis_basicas[i-1]
            val = self.tableau[i][-1]
            valores_raw[nome_bas] = val
        vars_originais = set()
        for v in self.mapa_variaveis.keys():
            nome_limpo = v.replace('_pos', '').replace('_neg', '')
            if nome_limpo.startswith('x'):
                vars_originais.add(nome_limpo)
        valores_reais = {}
        ordenadas = sorted(list(vars_originais), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
        for nome in ordenadas:
            val_real = 0.0
            if nome in self.variaveis_livres:
                val_pos = valores_raw.get(f"{nome}_pos", 0.0)
                val_neg = valores_raw.get(f"{nome}_neg", 0.0)
                val_real = val_pos - val_neg
            else:
                val_prima = valores_raw.get(nome, 0.0)
                val_real = val_prima
                if nome in self.variaveis_negativas:
                    val_real = -val_prima
            valores_reais[nome] = val_real
            if abs(val_real) < 1e-9:
                val_real = 0.0
            print(f"{nome} = {val_real:.1f}")
        print()
        for i, restr in enumerate(self.restricoes):
            soma_lhs = 0.0
            for var_tab, coef in restr['coef'].items():
                val_tab = valores_raw.get(var_tab, 0.0)
                soma_lhs += coef * val_tab
            rhs = restr['rhs']
            op = restr['tipo']
            nome_r = f"R{i+1}"
            if abs(soma_lhs) < 1e-9:
                soma_lhs = 0.0
            if op == '<=':
                print(f"{nome_r} = None <= {soma_lhs:.1f} <= {rhs:.1f}")
            elif op == '>=':
                print(f"{nome_r} = {rhs:.1f} <= {soma_lhs:.1f} <= None")
            elif op == '=':
                print(f"{nome_r} = {rhs:.1f} <= {soma_lhs:.1f} <= {rhs:.1f}")

if __name__ == "__main__":
    arquivo = "exemplo2.txt"
    solver = SolucionadorSimplex()
    solver.carregar_arquivo(arquivo)
    solver.resolver()
