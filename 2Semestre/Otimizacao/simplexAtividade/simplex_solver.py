# ============================================================================
# ALGORITMO SIMPLEX - Resolução de Programação Linear
# COM EXIBIÇÃO DO TABLEAU A CADA ITERAÇÃO
# Sem importação de bibliotecas externas
# ============================================================================

class SimplexSolver:
    """
    Resolve problemas de programação linear usando o algoritmo Simplex.
    Exibe tableau completo a cada iteração.
    """
    
    def __init__(self, filename):
        self.filename = filename
        self.sense = None  # MAX ou MIN
        self.c = []  # Coeficientes da função objetivo
        self.A = []  # Matriz de restrições
        self.b = [val for val in []]  # Lado direito das restrições
        self.var_names = []  # Nomes das variáveis originais
        self.var_types = {}  # Tipo de cada variável (>=0, <=0, livre)
        self.num_original_vars = 0
        self.num_expanded_vars = 0
        self.num_slack_vars = 0
        self.var_map = {}
        self.tolerance = 1e-9
        self.original_lower = {}  # Limites inferiores originais
        self.original_upper = {}  # Limites superiores originais
        
    def parse_file(self):
        """Lê e interpreta o arquivo de entrada."""
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
        
        idx = 0
        
        # Linha 1: Função Objetivo
        self._parse_objective(lines[idx])
        idx += 1
        
        # Pula linha em branco
        while idx < len(lines) and lines[idx] == '':
            idx += 1
        
        # Restrições (até próxima linha em branco)
        while idx < len(lines) and lines[idx] != '':
            self._parse_constraint(lines[idx])
            idx += 1
        
        # Pula linha em branco
        while idx < len(lines) and lines[idx] == '':
            idx += 1
        
        # Domínios das variáveis
        while idx < len(lines) and lines[idx] != '':
            self._parse_domain(lines[idx])
            idx += 1
        
        # Validações
        self._validate_problem()
    
    def _parse_objective(self, line):
        """Parse da linha de função objetivo."""
        parts = line.split()
        self.sense = parts[0]  # MAX ou MIN
        
        self.c = []
        self.var_names = []
        
        i = 1
        first = True
        current_sign = 1
        
        while i < len(parts):
            try:
                coeff = float(parts[i])
                if not first:
                    coeff *= current_sign
                
                var_name = parts[i + 1]
                self.var_names.append(var_name)
                self.c.append(coeff)
                
                i += 2
                first = False
                
                # Próximo elemento pode ser sinal
                if i < len(parts) and parts[i] in ['+', '-']:
                    current_sign = 1 if parts[i] == '+' else -1
                    i += 1
            except (ValueError, IndexError):
                break
        
        self.num_original_vars = len(self.var_names)
    
    def _parse_constraint(self, line):
        """Parse de uma restrição."""
        parts = line.split()
        
        constraint = []
        i = 0
        relational = None
        rhs = None
        
        while i < len(parts):
            if parts[i] in ['<=', '>=', '=']:
                relational = parts[i]
                rhs = float(parts[i + 1])
                break
            
            try:
                coeff = float(parts[i])
                var_name = parts[i + 1]
                constraint.append(coeff)
                i += 2
                
                if i < len(parts) and parts[i] in ['+', '-']:
                    i += 1
            except (ValueError, IndexError):
                i += 1
        
        while len(constraint) < self.num_original_vars:
            constraint.append(0.0)
        
        if relational == '>=':
            constraint = [-c for c in constraint]
            rhs = -rhs
        elif relational == '=':
            pass
        
        self.A.append(constraint)
        self.b.append(rhs)
    
    def _parse_domain(self, line):
        """Parse do domínio de uma variável."""
        parts = line.split()
        var_name = parts[0]
        
        if len(parts) == 2 and parts[1] == 'livre':
            self.var_types[var_name] = 'livre'
            self.original_lower[var_name] = float('-inf')
            self.original_upper[var_name] = float('inf')
        elif len(parts) >= 2:
            relational = parts[1]
            if relational == '>=':
                self.var_types[var_name] = '>='
                self.original_lower[var_name] = 0.0
                self.original_upper[var_name] = float('inf')
            elif relational == '<=':
                self.var_types[var_name] = '<='
                self.original_lower[var_name] = float('-inf')
                self.original_upper[var_name] = 0.0
    
    def _validate_problem(self):
        """Valida o problema lido."""
        if len(self.c) != self.num_original_vars:
            raise ValueError("Inconsistência entre número de variáveis")
        
        for row in self.A:
            if len(row) != self.num_original_vars:
                raise ValueError("Inconsistência em número de variáveis nas restrições")
    
    def _preprocess_variables(self):
        """Transforma variáveis para formato padrão (todas >= 0)."""
        self.var_map = {}
        expanded_idx = 0
        
        new_c = []
        new_A = [[] for _ in range(len(self.A))]
        
        for i, var_name in enumerate(self.var_names):
            var_type = self.var_types.get(var_name, '>=')
            
            if var_type == '>=':
                new_c.append(self.c[i])
                for j in range(len(self.A)):
                    new_A[j].append(self.A[j][i])
                self.var_map[expanded_idx] = (var_name, 1, i)
                expanded_idx += 1
                
            elif var_type == '<=':
                new_c.append(-self.c[i])
                for j in range(len(self.A)):
                    new_A[j].append(-self.A[j][i])
                self.var_map[expanded_idx] = (var_name, -1, i)
                expanded_idx += 1
                
            elif var_type == 'livre':
                new_c.append(self.c[i])
                new_c.append(-self.c[i])
                for j in range(len(self.A)):
                    new_A[j].append(self.A[j][i])
                    new_A[j].append(-self.A[j][i])
                self.var_map[expanded_idx] = (var_name, 1, i)
                self.var_map[expanded_idx + 1] = (var_name, -1, i)
                expanded_idx += 2
        
        self.c = new_c
        self.A = new_A
        self.num_expanded_vars = len(self.c)
    
    def _add_slack_variables(self):
        """Adiciona variáveis de folga."""
        num_constraints = len(self.A)
        slack_start = self.num_expanded_vars
        
        for i in range(num_constraints):
            for j in range(num_constraints):
                if i == j:
                    self.A[i].append(1.0)
                else:
                    self.A[i].append(0.0)
        
        self.c.extend([0.0] * num_constraints)
        self.num_slack_vars = num_constraints
    
    def solve(self):
        """Resolve o problema usando Simplex."""
        print("\n" + "=" * 90)
        print("ALGORITMO SIMPLEX - RESOLUÇÃO DE PROGRAMAÇÃO LINEAR")
        print("=" * 90)
        
        # Parse do arquivo
        self.parse_file()
        print("\n✓ Arquivo lido com sucesso!")
        print(f"  Sentido: {self.sense}")
        print(f"  Variáveis originais: {self.num_original_vars} - {self.var_names}")
        print(f"  Restrições: {len(self.A)}")
        
        # Preprocessamento
        self._preprocess_variables()
        self._add_slack_variables()
        
        print(f"  Variáveis expandidas: {self.num_expanded_vars}")
        print(f"  Variáveis de folga: {self.num_slack_vars}")
        print("\n" + "=" * 90)
        
        # Simplex
        result = self._simplex()
        
        return result
    
    def _simplex(self):
        """Executa o algoritmo Simplex."""
        c = self.c[:]
        if self.sense == 'MIN':
            c = [-val for val in c]
        
        A = [row[:] for row in self.A]
        b = [val for val in self.b]
        
        num_vars = len(c)
        num_constraints = len(A)
        
        # Base inicial: variáveis de folga
        basis = list(range(num_vars - num_constraints, num_vars))
        
        iteration = 0
        max_iterations = 10000
        
        while iteration < max_iterations:
            iteration += 1
            
            # Exibe tableau
            self._print_tableau(A, b, c, basis, iteration)
            
            # Cálculo dos custos reduzidos
            try:
                B_inv = self._calculate_B_inverse(A, basis)
            except:
                return {'status': 'Erro na inversão da matriz base', 'iteracoes': iteration}
            
            c_B = [c[j] for j in basis]
            reduced_costs = self._calculate_reduced_costs(c, A, basis, c_B, B_inv)
            
            # Critério de entrada
            entering = -1
            max_reduced = 0
            for j in range(num_vars):
                if j not in basis and reduced_costs[j] > max_reduced:
                    entering = j
                    max_reduced = reduced_costs[j]
            
            if entering == -1:
                # Solução ótima
                print(f"\n{'─' * 90}")
                print("✓ SOLUÇÃO ÓTIMA ENCONTRADA!")
                print(f"{'─' * 90}")
                solution = self._extract_solution(A, b, basis, c, num_vars)
                solution['iteracoes'] = iteration
                return solution
            
            # Direção
            d = self._calculate_direction(A, entering, basis, B_inv)
            
            # Critério de saída (razão mínima)
            x_B = self._calculate_x_B(A, b, basis, B_inv)
            
            theta_min = float('inf')
            leaving_idx = -1
            
            for i, basis_var in enumerate(basis):
                if d[i] > self.tolerance:
                    theta = x_B[i] / d[i]
                    if theta >= -self.tolerance and theta < theta_min:
                        theta_min = theta
                        leaving_idx = i
            
            if leaving_idx == -1:
                return {
                    'status': 'Problema Ilimitado',
                    'iteracoes': iteration
                }
            
            # Atualiza base
            leaving_var = basis[leaving_idx]
            basis[leaving_idx] = entering
            
            print(f"  Variável ENTRA: x{entering + 1}")
            print(f"  Variável SAI:   x{leaving_var + 1}")
            print()
        
        return {
            'status': 'Máximo de iterações atingido',
            'iteracoes': max_iterations
        }
    
    def _print_tableau(self, A, b, c, basis, iteration):
        """Exibe o tableau Simplex de forma formatada."""
        num_vars = len(c)
        num_constraints = len(A)
        
        print(f"\n{'═' * 90}")
        print(f"ITERAÇÃO {iteration}")
        print(f"{'═' * 90}\n")
        
        # Calcula custos reduzidos
        try:
            B_inv = self._calculate_B_inverse(A, basis)
            c_B = [c[j] for j in basis]
            reduced_costs = self._calculate_reduced_costs(c, A, basis, c_B, B_inv)
            x_B = self._calculate_x_B(A, b, basis, B_inv)
        except:
            return
        
        # Cabeçalho
        col_width = 15
        header = "Base".ljust(col_width)
        for j in range(num_vars):
            header += f"x{j + 1}".ljust(col_width)
        header += "RHS".ljust(col_width)
        
        print("┌" + "─" * 90 + "┐")
        print("│ TABLEAU DO SIMPLEX" + " " * 70 + "│")
        print("├" + "─" * 90 + "┤")
        print("│ " + header + " │")
        print("├" + "─" * 90 + "┤")
        
        # Restrições
        for i, basis_var in enumerate(basis):
            row_str = f"x{basis_var + 1}".ljust(col_width)
            
            for j in range(num_vars):
                # Reconstrói a coluna através de B_inv
                if j in basis:
                    # Coluna de variável básica = coluna da identidade
                    col_val = 1.0 if j == basis_var else 0.0
                else:
                    # Coluna de variável não-básica
                    a_col = [A[k][j] for k in range(num_constraints)]
                    col_val = sum(B_inv[i][k] * a_col[k] for k in range(num_constraints))
                
                row_str += f"{col_val:14.6f}".ljust(col_width)
            
            row_str += f"{x_B[i]:14.6f}".ljust(col_width)
            print("│ " + row_str + " │")
        
        # Linha da função objetivo (custos reduzidos)
        print("├" + "─" * 90 + "┤")
        fo_str = "Z (FO)".ljust(col_width)
        
        z_value = sum(c_B[i] * x_B[i] for i in range(len(basis)))
        
        for j in range(num_vars):
            fo_str += f"{reduced_costs[j]:14.6f}".ljust(col_width)
        
        fo_str += f"{z_value:14.6f}".ljust(col_width)
        print("│ " + fo_str + " │")
        
        print("└" + "─" * 90 + "┘")
        
        # Informações de variáveis básicas e não-básicas
        print(f"\nVariáveis Básicas: {', '.join([f'x{b + 1}' for b in basis])}")
        non_basis = [j for j in range(num_vars) if j not in basis]
        print(f"Não-Básicas:       {', '.join([f'x{j + 1}' for j in non_basis])}")
        print(f"Valor de Z (FO):   {z_value:.10f}")
    
    def _calculate_B_inverse(self, A, basis):
        """Calcula inversa da matriz básica."""
        B = [[A[i][j] for j in basis] for i in range(len(A))]
        return self._matrix_inverse(B)
    
    def _matrix_inverse(self, M):
        """Inverte matriz usando eliminação Gaussiana."""
        n = len(M)
        
        aug = []
        for i in range(n):
            row = M[i][:] + [0.0] * n
            row[n + i] = 1.0
            aug.append(row)
        
        for col in range(n):
            pivot_row = col
            for row in range(col + 1, n):
                if abs(aug[row][col]) > abs(aug[pivot_row][col]):
                    pivot_row = row
            
            if abs(aug[pivot_row][col]) < 1e-12:
                raise ValueError("Matriz singular")
            
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
            
            pivot = aug[col][col]
            for j in range(2 * n):
                aug[col][j] /= pivot
            
            for row in range(n):
                if row != col:
                    factor = aug[row][col]
                    for j in range(2 * n):
                        aug[row][j] -= factor * aug[col][j]
        
        inv = [aug[i][n:] for i in range(n)]
        return inv
    
    def _calculate_reduced_costs(self, c, A, basis, c_B, B_inv):
        """Calcula custos reduzidos."""
        num_vars = len(c)
        reduced = [0.0] * num_vars
        
        for j in range(num_vars):
            if j not in basis:
                a_j_in_base = [sum(B_inv[i][k] * A[k][j] for k in range(len(A))) 
                               for i in range(len(B_inv))]
                reduced[j] = c[j] - sum(c_B[i] * a_j_in_base[i] for i in range(len(c_B)))
        
        return reduced
    
    def _calculate_direction(self, A, entering, basis, B_inv):
        """Calcula direção para variável entrante."""
        a_col = [A[i][entering] for i in range(len(A))]
        d = [sum(B_inv[i][k] * a_col[k] for k in range(len(A))) for i in range(len(A))]
        return d
    
    def _calculate_x_B(self, A, b, basis, B_inv):
        """Calcula valores das variáveis básicas."""
        x_B = [sum(B_inv[i][j] * b[j] for j in range(len(b))) for i in range(len(b))]
        return x_B
    
    def _extract_solution(self, A, b, basis, c, num_vars):
        """Extrai solução ótima."""
        B_inv = self._calculate_B_inverse(A, basis)
        x_B = self._calculate_x_B(A, b, basis, B_inv)
        
        solution_values = [0.0] * num_vars
        for i, basis_var in enumerate(basis):
            solution_values[basis_var] = max(0.0, x_B[i])
        
        # Valor objetivo
        if self.sense == 'MAX':
            obj_value = sum(c[i] * solution_values[i] for i in range(num_vars))
        else:
            obj_value = -sum(c[i] * solution_values[i] for i in range(num_vars))
        
        # Reconstrói em termos de variáveis originais
        original_solution = {}
        for expanded_idx in range(self.num_expanded_vars):
            if expanded_idx in self.var_map:
                var_name, sign, orig_idx = self.var_map[expanded_idx]
                if var_name not in original_solution:
                    original_solution[var_name] = 0.0
                original_solution[var_name] += sign * solution_values[expanded_idx]
        
        return {
            'status': 'Ótimo',
            'valor_objetivo': obj_value,
            'variaveis': original_solution,
            'basis': basis
        }


def main():
    """Função principal."""
    import sys
    
    if len(sys.argv) < 2:
        filename = input("Digite o nome do arquivo: ")
    else:
        filename = sys.argv[1]
    
    try:
        solver = SimplexSolver(filename)
        result = solver.solve()
        
        print("\n" + "=" * 90)
        print("RESULTADO FINAL")
        print("=" * 90)
        
        if result['status'] == 'Ótimo':
            print(f"\n✓ Status: SOLUÇÃO ÓTIMA ENCONTRADA")
            print(f"  Iterações: {result['iteracoes']}")
            print(f"\n  Valor da Função Objetivo: {result['valor_objetivo']:.10f}")
            
            print(f"\n{'Variável':<15} {'Valor':<20} {'Lower':<20} {'Upper':<20} {'Restrição':<20}")
            print("─" * 95)
            
            for var_name in sorted(result['variaveis'].keys()):
                value = result['variaveis'][var_name]
                lower = solver.original_lower.get(var_name, float('-inf'))
                upper = solver.original_upper.get(var_name, float('inf'))
                
                # Formato dos limites
                lower_str = "-∞" if lower == float('-inf') else f"{lower:.6f}"
                upper_str = "+∞" if upper == float('inf') else f"{upper:.6f}"
                
                # Restricao
                if lower == float('-inf') and upper == float('inf'):
                    restricao = "Livre"
                elif lower == float('-inf'):
                    restricao = f"≤ {upper:.6f}"
                elif upper == float('inf'):
                    restricao = f"≥ {lower:.6f}"
                else:
                    restricao = f"{lower:.6f} ≤ x ≤ {upper:.6f}"
                
                print(f"{var_name:<15} {value:>18.10f} {lower_str:>18} {upper_str:>18} {restricao:<20}")
            
            print("─" * 95)
            print(f"\n✓ Valor ótimo da Função Objetivo: {result['valor_objetivo']:.10f}")
            
        else:
            print(f"\n✗ Status: {result['status']}")
            print(f"  Iterações: {result['iteracoes']}")
        
        print("\n" + "=" * 90)
        
    except FileNotFoundError:
        print(f"✗ Erro: Arquivo '{filename}' não encontrado!")
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
