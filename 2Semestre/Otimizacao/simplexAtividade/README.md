# 📊 Algoritmo Simplex - Resolvedor de Programação Linear
## Com Exibição de Tableau a Cada Iteração

## ✨ Características

- ✅ **Sem dependências externas** - Puro Python, sem NumPy ou SciPy
- ✅ **Suporta variáveis genéricas** - Não-negativas (≥0), não-positivas (≤0) e livres (irrestritas)
- ✅ **Múltiplos tipos de restrição** - ≤, ≥, e = (igualdade)
- ✅ **Maximização e Minimização**
- ✅ **Números decimais** - Coeficientes não-inteiros
- ✅ **Dimensão variável** - Funciona com qualquer número de variáveis e restrições
- ✅ **Tableau Simplex** - Exibição completa a cada iteração
- ✅ **Detecção de infactibilidade e ilimitação**
- ✅ **Análise de sensibilidade** - Exibe Lower ≤ x ≤ Upper para cada variável

## 📋 Formato do Arquivo de Entrada

### Estrutura Geral

```
[Linha 1] Função Objetivo
[Linha 2] Em branco
[Linhas 3+] Restrições
[Linha vazia] Em branco
[Resto] Domínios das variáveis
```

### Detalhes do Formato

#### 1. Função Objetivo
```
MAX 3 x1 + 2 x2 + 10 x3 + 0 x4 + 2 x5
```
ou
```
MIN 5 y1 - 3 y2 + 1.5 y3
```

**Regras:**
- Comece com `MAX` ou `MIN`
- Cada termo: `coeficiente variável` (separados por espaço)
- Entre termos: espaço, sinal `+` ou `-`, espaço
- Coeficientes podem ser decimais

#### 2. Restrições
```
3 x1 + 1 x2 + 7 x3 + 10 x4 + 0 x5 <= 6
1 x1 + 0 x2 + 7 x3 + 0 x4 + 9 x5 >= 46
8 x1 + 0 x2 + 1 x3 + 1 x4 + 1 x5 = 25
```

**Regras:**
- Mesmo formato da FO para os coeficientes
- Após último coeficiente/variável: espaço, relacional (`<=`, `>=` ou `=`), espaço, valor RHS
- RHS pode ser decimal
- Quantas restrições precisar

#### 3. Domínios das Variáveis
```
x1 >= 0
x2 >= 0
x3 >= 0
x4 <= 0
x5 livre
```

**Regras:**
- Uma linha por variável
- Variáveis não-negativas: `nome >= 0`
- Variáveis não-positivas: `nome <= 0`
- Variáveis livres (irrestritas): `nome livre`
- **IMPORTANTE:** Todas as variáveis que aparecem na FO e restrições devem ter seu domínio especificado

## 🚀 Como Usar

### Passo 1: Preparar o Arquivo
Crie um arquivo `.txt` seguindo o formato acima. Exemplo: `problema.txt`

### Passo 2: Executar o Solver

**Opção A - Com argumento de linha de comando:**
```bash
python simplex_solver.py problema.txt
```

**Opção B - Entrada interativa:**
```bash
python simplex_solver.py
# Será solicitado o nome do arquivo
```

## 📊 Saída do Programa

### Exemplo de Tableau (Iteração 1)

```
══════════════════════════════════════════════════════════════════════════════════════
ITERAÇÃO 1
══════════════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────────────┐
│ TABLEAU DO SIMPLEX                                                                   │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ Base              x1                x2                x3                x4       ... │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ x11            3.000000            1.000000            7.000000           10.000000 │
│ x12            1.000000            0.000000            7.000000            0.000000 │
│ x13            8.000000            0.000000            1.000000            1.000000 │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ Z (FO)         3.000000            2.000000           10.000000            0.000000 │
└──────────────────────────────────────────────────────────────────────────────────────┘

Variáveis Básicas: x11, x12, x13, ...
Não-Básicas:       x1, x2, x3, ...
Valor de Z (FO):   0.0000000000

  Variável ENTRA: x1
  Variável SAI:   x11
```

### Resultado Final

```
════════════════════════════════════════════════════════════════════════════════════════
RESULTADO FINAL
════════════════════════════════════════════════════════════════════════════════════════

✓ Status: SOLUÇÃO ÓTIMA ENCONTRADA
  Iterações: 8

Variável        Valor                Lower              Upper              Restrição      
─────────────────────────────────────────────────────────────────────────────────────────
x1              5.1234567890        0.000000           +∞                 ≥ 0.000000
x2              0.0000000000        0.000000           +∞                 ≥ 0.000000
x3              2.3456789012        0.000000           +∞                 ≥ 0.000000
x4             -1.2345678901       -∞                  0.000000           ≤ 0.000000
x5              3.4567890123       -∞                  +∞                 Livre
─────────────────────────────────────────────────────────────────────────────────────────

✓ Valor ótimo da Função Objetivo: 123.5678901234

════════════════════════════════════════════════════════════════════════════════════════
```

## 🎯 Informações Exibidas

### Tableau a Cada Iteração

O tableau exibe:
- **Base**: Variáveis atualmente na base
- **Colunas x₁, x₂, ..., xₙ**: Coeficientes de cada variável no sistema
- **RHS**: Lado direito (valores das variáveis básicas)
- **Linha Z (FO)**: Custos reduzidos de cada variável
- **Variáveis Básicas**: Lista das variáveis na base atual
- **Não-Básicas**: Lista das variáveis fora da base
- **Valor de Z**: Valor atual da função objetivo
- **Pivoteamento**: Indica qual variável entra e qual sai

### Resultado Final

Para cada variável, exibe:
- **Variável**: Nome da variável
- **Valor**: Valor ótimo encontrado
- **Lower**: Limite inferior (≥ ou -∞)
- **Upper**: Limite superior (≤ ou +∞)
- **Restrição**: Resumo do domínio em formato legível

## 📊 Exemplos

### Exemplo 1: Problema Simples

**Arquivo: `simples.txt`**
```
MAX 2 x1 + 3 x2

x1 + x2 <= 4
2 x1 + x2 <= 5

x1 >= 0
x2 >= 0
```

**Resultado Esperado:**
- Solução: x1 = 1, x2 = 3
- Valor: 11
- Tableau exibido para cada iteração

### Exemplo 2: Com Variáveis Livres

**Arquivo: `com_livres.txt`**
```
MIN x1 + 2 x2 + x3

x1 + x2 + x3 = 5
2 x1 - x2 + 3 x3 <= 10

x1 >= 0
x2 livre
x3 <= 0
```

## 🔍 Tratamento Especial de Variáveis

### Variáveis Não-Negativas (x ≥ 0)
- Entram normalmente na matriz
- Tableau exibe: `0.000000 ≤ x ≤ +∞`

### Variáveis Não-Positivas (x ≤ 0)
- Transformadas: x_original = -x_transformada
- Tableau exibe: `-∞ ≤ x ≤ 0.000000`

### Variáveis Livres (x ∈ ℝ)
- Decompostas: x = x⁺ - x⁻
- Tableau exibe: `-∞ ≤ x ≤ +∞ (Livre)`

## ⚙️ Parâmetros Ajustáveis

No código, é possível ajustar:

```python
self.tolerance = 1e-9  # Tolerância para comparações numéricas
max_iterations = 10000  # Máximo de iterações do Simplex
```

## 🐛 Possíveis Mensagens de Status

| Status | Significado |
|--------|-------------|
| `Ótimo` | Solução ótima encontrada ✓ |
| `Problema Ilimitado` | Função objetivo pode crescer infinitamente |
| `Problema Infactível` | Não há solução viável que satisfaça todas as restrições |
| `Máximo de iterações atingido` | Simplex não convergiu no limite especificado |
| `Erro na inversão da matriz base` | Matriz singular - problema na formulação |

## 💡 Dicas de Uso

1. **Visualizar iterações**: O tableau é exibido a cada iteração
2. **Acompanhar pivôs**: Veja qual variável entra e qual sai em cada passo
3. **Verificar custos reduzidos**: Procure por valores positivos para entender quando pará
4. **Análise de sensibilidade**: Use a coluna "Restrição" para análise de limitações
5. **Exportar resultados**: O programa exibe valores com 10 casas decimais

## 📝 Notas Importantes

- ⚠️ O código assume que sempre há uma solução básica viável inicial (variáveis de folga)
- ⚠️ Para problemas com restrições de igualdade (=), use a Fase I do Simplex se necessário
- ⚠️ Números muito pequenos ou muito grandes podem causar problemas numéricos
- ⚠️ Problemas mal-condicionados podem requerer ajuste de `tolerance`
- ℹ️ Tableau é exibido em formato de caixa com linhas ASCII para melhor visualização

## 📞 Suporte

Para problemas na execução:
1. Verifique o formato do arquivo
2. Confirme que todos os domínios estão definidos
3. Verifique se o RHS das restrições é válido
4. Teste com o arquivo `exemplo.txt` incluído
5. Verifique a saída do tableau para identificar o problema

---

**Bom uso! 🎯**
