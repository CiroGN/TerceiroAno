def lerModelo():
    c = [3, 2]

    A = [[2, 1],[3, 2]]

    b = [6, 12]

    VD = ['x1', 'x2']

    return c, A, b, VD

def imprimirTableau(Base, Iter, Variaveis, Tableau):
    Cabecalho = ['VB', '-Z'] + Variaveis + ['b']
    Largura = 6 # para as colunas numericas

    # Impressao
    print(f'=== Iteracao: {Iter} ===')
    print(f'{Cabecalho[0]:>15}', end = '')
    for elemento in Cabecalho[1:]:
        print(f'{elemento:>{Largura}}', end = '')
    print()

    # Impressao das variaveis basicas
    for i, var in enumerate(Base):
        print(f'{var:>15}', end = '')
        for valor in Tableau[i]:
            print(f'{valor:>{Largura}.2f}', end = '')
        print()

    # impressao da funcao objetivo
    print(f'{"-Z":>15}', end = '')
    for valor in Tableau[-1]:
        print(f'{valor:>{Largura}.2f}', end = '')
    print()

def metodoSimplex(c, A, b, VD):
    # contando VDs e Restricoes
    m = len(A) # numero de restricoes
    n = len(c) # numero de variaveis de decisao VDs

    # Coeficienta das restricoes
    Tableau = []
    for i in range(m):
        linha = [0] + A[i][:] + [0]*m + [b[i]]
        linha[n + i + 1] = 1
        Tableau.append(linha)

    # Coeficientes da funcao objetivo
    linhaFO = [1] + [-j for j in c] + [0]*m + [0]
    Tableau.append(linhaFO)

    # Nomeando as variaveis de folga
    Folgas = [f's{i+1}' for i in range(m)]
    VDFolgas = VD + Folgas
    Base = Folgas[:]

    Iter = 0
    imprimirTableau(Base, Iter, VDFolgas, Tableau)
    print()

    #Loop principlal do Simplex
    while True:
        ZLinha = Tableau[-1][1:-1] # ultima linha do tableau da primeira ate a ultima coluna
        menorCoef = min(ZLinha)

        if menorCoef >= 0: # criterio de parada  
            print("\nSolução Otima Encontrada!")
            break

        # Encontrando a variavel que entra na base
        colunaPivo = ZLinha.index(menorCoef) + 1

        # Encontrando a variavel que sai da base
        vetorBloqueio = []
        for i in range(m):
            if Tableau[i][colunaPivo] > 0:
                valorBloq = Tableau[i][-1] / Tableau[i][colunaPivo]
            else:
                valorBloq = float('inf')
            vetorBloqueio.append(valorBloq)
        linhaPivo = vetorBloqueio.index(min(vetorBloqueio))

        # identificando solucoes ilimitadas
        if min(vetorBloqueio) == float('inf'):
            print("Solução Ilimitada!")
            break

        # normalizacao da linha pivo
        pivo = Tableau[linhaPivo][colunaPivo]
        for j in range(len(Tableau[linhaPivo])):
            Tableau[linhaPivo][j] /= pivo # tableau[linhaPivo][j] = (tableau[linhaPivo][j]) / pivo
        
        # zerando as colunas acima r abaixo da linha pivo (escalonamento de gauss)
        for i in range(len(Tableau)):
            if i != linhaPivo:
                fator = Tableau[i][colunaPivo]
                for j in range(len(Tableau[1])):
                    Tableau[i][j] -= fator * Tableau[linhaPivo][j] # tableau[i][j] = tableau[i][j] - fator * tableau[linhaPivo][j]

        # atualizando a base
        Base[linhaPivo] = VDFolgas[colunaPivo - 1]
        Iter += 1
        imprimirTableau(Base, Iter, VDFolgas, Tableau)
        print()

if __name__ == "__main__":
    c, A, b, VD = lerModelo()
    metodoSimplex(c, A, b, VD)