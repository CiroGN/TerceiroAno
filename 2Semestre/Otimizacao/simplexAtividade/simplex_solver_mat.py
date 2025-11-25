import re, os 

class SolverSimplex:
    def __init__(self):
        self.tableau = []
        self.headers = []
        self.M = 1e7  # Big M
        self.var_map = {} 
        self.basic_vars = [] 
        self.num_rows = 0
        self.num_cols = 0
        self.num_dec_vars = 0 
        self.negative_vars = set() 
        self.free_vars = set() # Variáveis livres (irrestritas)
        self.optimization_type = 'MAX'
        self.constraints = [] 

    def _parse_expression(self, expr):
        expr = expr.replace(" ", "")
        if not expr.startswith('+') and not expr.startswith('-'):
            expr = '+' + expr
        
        coeffs = {}
        pattern = re.compile(r'([+-])(\d*\.?\d*)?([a-zA-Z]+\d*)')
        matches = pattern.findall(expr)
        
        for sign, num, var in matches:
            if not var and not num: continue
            
            val = 1.0
            if num:
                val = float(num)
            if sign == '-':
                val = -val
            
            if var:
                if var in coeffs:
                    coeffs[var] += val
                else:
                    coeffs[var] = val
        return coeffs

    def _split_free_vars(self, coeffs):
        """Substitui variáveis livres xi por (xi_pos - xi_neg)"""
        new_coeffs = {}
        for var, val in coeffs.items():
            if var in self.free_vars:
                # xi = xi_pos - xi_neg
                # Coeff * xi => Coeff * xi_pos - Coeff * xi_neg
                new_coeffs[f"{var}_pos"] = val
                new_coeffs[f"{var}_neg"] = -val
            else:
                new_coeffs[var] = val
        return new_coeffs

    def carregar_arquivo(self, filename):
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        self.negative_vars = set()
        self.free_vars = set()
        bounds_lines = []
        equation_lines = []

        # Detecção de linhas de Restrição vs Linhas de Definição de Variável
        for line in lines:
            # Padrões de bounds: "x1 <= 0", "x1 >= 0", "x8 livre"
            is_bound = False
            if 'livre' in line.lower() or 'free' in line.lower():
                is_bound = True
            elif re.match(r'^[a-zA-Z]+\d*\s*(<=|>=)\s*0$', line):
                is_bound = True
            
            if is_bound:
                bounds_lines.append(line)
            else:
                equation_lines.append(line)

        # Processar definições de variáveis
        for line in bounds_lines:
            if 'livre' in line.lower() or 'free' in line.lower():
                # Formato esperado: "x8 livre"
                parts = line.split()
                var_name = parts[0]
                self.free_vars.add(var_name)
            elif '<=' in line and '0' in line:
                var_name = line.split('<=')[0].strip()
                self.negative_vars.add(var_name)
        
        obj_line = equation_lines[0]
        
        if obj_line.upper().startswith("MIN"):
            self.optimization_type = 'MIN'
        else:
            self.optimization_type = 'MAX'

        obj_expr = re.sub(r'^(MAX|MIN)\s*', '', obj_line, flags=re.IGNORECASE)
        obj_coeffs = self._parse_expression(obj_expr)

        # Ajustes na Função Objetivo
        for var in list(obj_coeffs.keys()):
            if var in self.negative_vars:
                obj_coeffs[var] = -obj_coeffs[var]
            if self.optimization_type == 'MIN':
                obj_coeffs[var] = -obj_coeffs[var]

        # Aplicar Split nas variáveis livres da Função Objetivo
        obj_coeffs = self._split_free_vars(obj_coeffs)

        all_vars = set(obj_coeffs.keys())
        self.constraints = [] 
        
        for line in equation_lines[1:]:
            operator = None
            if '<=' in line: operator = '<='
            elif '>=' in line: operator = '>='
            elif '=' in line: operator = '='
            
            if not operator: continue 
            
            lhs, rhs = line.split(operator)
            lhs_coeffs = self._parse_expression(lhs)
            rhs_val = float(rhs)
            
            # Ajustes nas Restrições (Negativas e Livres)
            # 1. Vars Negativas
            for var in list(lhs_coeffs.keys()):
                if var in self.negative_vars:
                    lhs_coeffs[var] = -lhs_coeffs[var]
            
            # 2. Vars Livres (Split)
            lhs_coeffs = self._split_free_vars(lhs_coeffs)
            
            all_vars.update(lhs_coeffs.keys())
            self.constraints.append({'coeffs': lhs_coeffs, 'type': operator, 'rhs': rhs_val})

        # Ordenação inteligente: tenta manter x8_pos e x8_neg juntos
        def sort_key(x):
            # Extrai número
            num_match = re.search(r'\d+', x)
            num = int(num_match.group()) if num_match else 0
            # Define ordem de sufixo: normal < neg < pos (arbitrário, apenas para agrupar)
            suffix_score = 0
            if '_neg' in x: suffix_score = 1
            if '_pos' in x: suffix_score = 2
            return (num, suffix_score)

        sorted_vars = sorted(list(all_vars), key=sort_key)
        self.var_map = {var: i for i, var in enumerate(sorted_vars)}
        self.num_dec_vars = len(sorted_vars)
        
        n_slack = 0
        n_surplus = 0
        n_artificial = 0
        row_setup = [] 

        for const in self.constraints:
            if const['type'] == '<=':
                n_slack += 1
                row_setup.append(('slack', n_slack, const))
            elif const['type'] == '>=':
                n_surplus += 1
                n_artificial += 1
                row_setup.append(('surplus_artificial', n_surplus, n_artificial, const))
            elif const['type'] == '=':
                n_artificial += 1
                row_setup.append(('artificial', n_artificial, const))

        total_vars = self.num_dec_vars + n_slack + n_surplus + n_artificial
        self.num_cols = total_vars
        self.num_rows = len(self.constraints) + 1 

        self.tableau = [[0.0] * (self.num_cols + 1) for _ in range(self.num_rows)]
        
        self.headers = sorted_vars[:]
        for i in range(1, n_slack + 1): self.headers.append(f's{i}')
        for i in range(1, n_surplus + 1): self.headers.append(f'e{i}')
        for i in range(1, n_artificial + 1): self.headers.append(f'a{i}')
        self.headers.append('Sol')

        # Preencher Objetivo
        for var in sorted_vars:
            self.tableau[0][self.var_map[var]] = -obj_coeffs.get(var, 0.0)
        
        current_slack = self.num_dec_vars
        current_surplus = self.num_dec_vars + n_slack
        current_artificial = self.num_dec_vars + n_slack + n_surplus
        artificial_rows_indices = []

        row_idx = 1
        for setup in row_setup:
            type_ = setup[0]
            const = setup[-1]
            
            for var, val in const['coeffs'].items():
                col_idx = self.var_map[var]
                self.tableau[row_idx][col_idx] = val
            
            self.tableau[row_idx][-1] = const['rhs']

            if type_ == 'slack':
                self.tableau[row_idx][current_slack] = 1.0
                self.basic_vars.append(f's{setup[1]}')
                current_slack += 1
            elif type_ == 'surplus_artificial':
                self.tableau[row_idx][current_surplus] = -1.0
                self.tableau[row_idx][current_artificial] = 1.0
                self.tableau[0][current_artificial] = self.M 
                self.basic_vars.append(f'a{setup[2]}')
                artificial_rows_indices.append((row_idx, current_artificial))
                current_surplus += 1
                current_artificial += 1
            elif type_ == 'artificial':
                self.tableau[row_idx][current_artificial] = 1.0
                self.tableau[0][current_artificial] = self.M
                self.basic_vars.append(f'a{setup[1]}')
                artificial_rows_indices.append((row_idx, current_artificial))
                current_artificial += 1
            
            row_idx += 1

        for r_idx, c_idx in artificial_rows_indices:
            mult = self.tableau[0][c_idx]
            for j in range(len(self.tableau[0])):
                self.tableau[0][j] -= mult * self.tableau[r_idx][j]

    def mostrar_tableau(self, iteracao):
        # Apenas mostra se a iteração for baixa para não poluir, ou a última
        if iteracao < 2:
            print(f"\n--- Iteração {iteracao} ---")
            header_str = " | ".join([f"{h:>7}" for h in self.headers])
            print(header_str)
            print("-" * len(header_str))
            labels = [' Z'] + [f"{b:>2}" for b in self.basic_vars]
            for i, row in enumerate(self.tableau):
                row_str = " | ".join([f"{val:>7.1f}" for val in row])
                label = labels[i] if i < len(labels) else f"R{i}"
                print(f"{label:<3} | {row_str}")

    def resolver(self):
        print(f"\n>>> Resolvendo problema de {self.optimization_type} <<<")
        iteracao = 0
        self.mostrar_tableau(iteracao)
        max_iteracoes = 5000
        
        while iteracao < max_iteracoes:
            min_val = 0
            pivot_col = -1
            # Bland's Rule para evitar ciclos: escolher o primeiro índice com valor negativo válido
            for j in range(self.num_cols):
                val = self.tableau[0][j]
                if val < min_val - 1e-7: # Tolerância
                    min_val = val
                    pivot_col = j
                    break # Bland's rule: pega o primeiro negativo (menor índice)
            
            if pivot_col == -1:
                break 
            
            min_ratio = float('inf')
            pivot_row = -1
            for i in range(1, self.num_rows):
                rhs = self.tableau[i][-1]
                coeff = self.tableau[i][pivot_col]
                if coeff > 1e-9:
                    ratio = rhs / coeff
                    if ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row = i
            
            if pivot_row == -1:
                print("\n>>> O problema é Ilimitado! <<<")
                return

            self.basic_vars[pivot_row - 1] = self.headers[pivot_col]
            
            pivot_element = self.tableau[pivot_row][pivot_col]
            for j in range(len(self.tableau[0])):
                self.tableau[pivot_row][j] /= pivot_element
            for i in range(self.num_rows):
                if i != pivot_row:
                    factor = self.tableau[i][pivot_col]
                    for j in range(len(self.tableau[0])):
                        self.tableau[i][j] -= factor * self.tableau[pivot_row][j]
            iteracao += 1
            if iteracao % 100 == 0:
                print(f"Iteração {iteracao}...")

        # --- RELATÓRIO FINAL ---
        print("\nSolução\n")
        
        val_z = self.tableau[0][-1]
        if self.optimization_type == 'MIN':
            val_z = -val_z
        print(f"FO: {val_z:.1f}")

        # Extrair valores crus do tableau
        raw_values = {}
        for i in range(1, self.num_rows):
            basic_var_name = self.basic_vars[i-1]
            val = self.tableau[i][-1]
            raw_values[basic_var_name] = val

        # Identificar todas as variáveis originais baseadas no map
        original_vars = set()
        for v in self.var_map.keys():
            # Limpa sufixos _pos e _neg para achar o nome original
            clean_name = v.replace('_pos', '').replace('_neg', '')
            if clean_name.startswith('x'):
                original_vars.add(clean_name)
        
        # Ordenar e imprimir
        print_real_values = {}
        sorted_orig_vars = sorted(list(original_vars), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)

        for var_name in sorted_orig_vars:
            val_real = 0.0
            
            if var_name in self.free_vars:
                # Recuperar partes pos e neg
                val_pos = raw_values.get(f"{var_name}_pos", 0.0)
                val_neg = raw_values.get(f"{var_name}_neg", 0.0)
                val_real = val_pos - val_neg
            else:
                val_prime = raw_values.get(var_name, 0.0)
                val_real = val_prime
                if var_name in self.negative_vars:
                    val_real = -val_prime
            
            print_real_values[var_name] = val_real # Guardar para cálculo das restrições
            
            # Formatação especial para 0.0 para evitar -0.0
            if abs(val_real) < 1e-9: val_real = 0.0
            
            print(f"{var_name} = {val_real:.1f}")

        print() 

        # 3. Análise das Restrições
        for i, const in enumerate(self.constraints):
            lhs_sum = 0.0
            
            # Iterar sobre os coeficientes armazenados (que já estão "splitados" ou "negativados")
            for var_tableau, coeff in const['coeffs'].items():
                val_tableau = raw_values.get(var_tableau, 0.0)
                lhs_sum += coeff * val_tableau
            
            rhs = const['rhs']
            op = const['type']
            r_name = f"R{i+1}"
            
            if abs(lhs_sum) < 1e-9: lhs_sum = 0.0

            if op == '<=':
                print(f"{r_name} = None <= {lhs_sum:.1f} <= {rhs:.1f}")
            elif op == '>=':
                print(f"{r_name} = {rhs:.1f} <= {lhs_sum:.1f} <= None")
            elif op == '=':
                print(f"{r_name} = {rhs:.1f} <= {lhs_sum:.1f} <= {rhs:.1f}")

# --- BLOCO DE EXECUÇÃO DO PROBLEMA COMPLEXO ---

problema_complexo = """MAX 1 x1 + 7 x2 + 7 x3 + 8 x4 + 4 x5 + 6 x6 + 1 x7 + 10 x8 + 9 x9 + 8 x10
6 x1 + 2 x2 + 6 x3 + 7 x4 + 0 x5 + 2 x6 + 2 x7 + 5 x8 + 5 x9 + 10 x10 = 5
0 x1 + 9 x2 + 10 x3 + 9 x4 + 3 x5 + 3 x6 + 4 x7 + 6 x8 + 6 x9 + 8 x10 <= 60
1 x1 + 4 x2 + 1 x3 + 8 x4 + 6 x5 + 0 x6 + 6 x7 + 8 x8 + 4 x9 + 4 x10 <= 33
3 x1 + 5 x2 + 3 x3 + 2 x4 + 10 x5 + 4 x6 + 0 x7 + 1 x8 + 7 x9 + 7 x10 <= 57
7 x1 + 2 x2 + 3 x3 + 2 x4 + 9 x5 + 10 x6 + 6 x7 + 6 x8 + 9 x9 + 1 x10 <= 64
6 x1 + 10 x2 + 8 x3 + 5 x4 + 9 x5 + 4 x6 + 8 x7 + 2 x8 + 9 x9 + 5 x10 <= 67
7 x1 + 2 x2 + 10 x3 + 9 x4 + 3 x5 + 5 x6 + 8 x7 + 6 x8 + 4 x9 + 6 x10 <= 35
8 x1 + 7 x2 + 4 x3 + 0 x4 + 5 x5 + 7 x6 + 0 x7 + 5 x8 + 4 x9 + 4 x10 <= 42
4 x1 + 0 x2 + 3 x3 + 3 x4 + 1 x5 + 6 x6 + 6 x7 + 2 x8 + 6 x9 + 7 x10 <= 22
2 x1 + 10 x2 + 6 x3 + 6 x4 + 4 x5 + 4 x6 + 4 x7 + 9 x8 + 3 x9 + 10 x10 <= 74
1 x1 + 8 x2 + 10 x3 + 1 x4 + 5 x5 + 10 x6 + 7 x7 + 10 x8 + 8 x9 + 10 x10 <= 49
4 x1 + 2 x2 + 0 x3 + 8 x4 + 1 x5 + 9 x6 + 4 x7 + 10 x8 + 0 x9 + 10 x10 <= 89
0 x1 + 5 x2 + 7 x3 + 2 x4 + 10 x5 + 3 x6 + 5 x7 + 2 x8 + 6 x9 + 5 x10 <= 73
10 x1 + 8 x2 + 2 x3 + 3 x4 + 0 x5 + 6 x6 + 7 x7 + 7 x8 + 8 x9 + 3 x10 <= 64
4 x1 + 10 x2 + 10 x3 + 4 x4 + 9 x5 + 6 x6 + 4 x7 + 3 x8 + 1 x9 + 5 x10 <= 36
3 x1 + 9 x2 + 2 x3 + 0 x4 + 7 x5 + 5 x6 + 1 x7 + 8 x8 + 4 x9 + 8 x10 <= 44
2 x1 + 7 x2 + 8 x3 + 3 x4 + 2 x5 + 5 x6 + 9 x7 + 3 x8 + 3 x9 + 6 x10 <= 29
1 x1 + 7 x2 + 9 x3 + 6 x4 + 9 x5 + 0 x6 + 3 x7 + 7 x8 + 5 x9 + 9 x10 <= 28
8 x1 + 8 x2 + 7 x3 + 9 x4 + 3 x5 + 3 x6 + 7 x7 + 1 x8 + 2 x9 + 9 x10 <= 87
3 x1 + 8 x2 + 5 x3 + 6 x4 + 9 x5 + 2 x6 + 0 x7 + 3 x8 + 10 x9 + 0 x10 <= 100
9 x1 + 8 x2 + 6 x3 + 10 x4 + 5 x5 + 10 x6 + 7 x7 + 2 x8 + 6 x9 + 2 x10 <= 43
1 x1 + 9 x2 + 0 x3 + 10 x4 + 3 x5 + 6 x6 + 5 x7 + 6 x8 + 9 x9 + 4 x10 <= 78
7 x1 + 3 x2 + 6 x3 + 7 x4 + 4 x5 + 10 x6 + 5 x7 + 1 x8 + 3 x9 + 8 x10 <= 87
3 x1 + 0 x2 + 9 x3 + 5 x4 + 0 x5 + 10 x6 + 6 x7 + 10 x8 + 6 x9 + 10 x10 <= 7
9 x1 + 4 x2 + 5 x3 + 10 x4 + 7 x5 + 7 x6 + 9 x7 + 5 x8 + 0 x9 + 5 x10 <= 97
4 x1 + 7 x2 + 7 x3 + 2 x4 + 0 x5 + 1 x6 + 6 x7 + 0 x8 + 10 x9 + 6 x10 <= 68
3 x1 + 0 x2 + 2 x3 + 5 x4 + 5 x5 + 7 x6 + 10 x7 + 5 x8 + 5 x9 + 10 x10 <= 54
4 x1 + 10 x2 + 7 x3 + 9 x4 + 10 x5 + 4 x6 + 5 x7 + 6 x8 + 7 x9 + 9 x10 <= 48
4 x1 + 0 x2 + 8 x3 + 3 x4 + 0 x5 + 7 x6 + 4 x7 + 5 x8 + 10 x9 + 5 x10 <= 44
3 x1 + 4 x2 + 2 x3 + 7 x4 + 5 x5 + 3 x6 + 5 x7 + 3 x8 + 3 x9 + 2 x10 >= 38
x1 >= 0
x2 <= 0
x3 <= 0
x4 >= 0
x5 >= 0
x6 >= 0
x7 >= 0
x8 livre
x9 >= 0
x10 >= 0
"""

filename = "exemplo.txt"
if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write(problema_complexo)
    print(f"Arquivo '{filename}' gerado. Resolvendo...")


solver = SolverSimplex()
solver.carregar_arquivo(filename)
solver.resolver()