#include <iostream>
using namespace std;

const int MAX = 100;
int matriz[MAX][MAX];
int visitados[MAX][MAX];
int pai_x[MAX][MAX], pai_y[MAX][MAX];
int L, C;

// Função para imprimir a matriz com o caminho marcado
void imprime_matriz(){
    for(int i = 0; i < C; i++){
        for(int j = 0; j < L; j++){
            if (matriz[i][j] == 2)
                cout << "* ";
            else if (matriz[i][j] == 0)
                cout << "  ";
            else
                cout << matriz[i][j] << " ";
        }
        cout << endl;
    }
    cout << "-------------------------------\n";
}

// Marcar caminho de trás pra frente com base nos pais
void marcar_caminho(int xi, int yi, int xf, int yf) {
    int x = xf;
    int y = yf;

    while (!(x == xi && y == yi)) {
        matriz[x][y] = 2;
        int px = pai_x[x][y];
        int py = pai_y[x][y];
        x = px;
        y = py;
        imprime_matriz();
    }
    matriz[xi][yi] = 2; // marca o ponto de início também
}

// Implementação da busca BFS
bool bfs(int xi, int yi, int xf, int yf) {
    // fila manual usando arrays
    int fila_x[MAX * MAX];
    int fila_y[MAX * MAX];
    int ini = 0, fim = 0;

    // inicia com o ponto de partida
    fila_x[fim] = xi;
    fila_y[fim] = yi;
    fim++;
    visitados[xi][yi] = 1;

    while (ini < fim) {
        int x = fila_x[ini];
        int y = fila_y[ini];
        ini++;

        if (x == xf && y == yf) {
            marcar_caminho(xi, yi, xf, yf);
            return true;
        }

        // tenta mover para os 4 vizinhos
        int dx[] = {0, -1, 0, 1};  // cima, esquerda, baixo, direita
        int dy[] = {-1, 0, 1, 0};

        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            if (nx >= 0 && nx < C && ny >= 0 && ny < L &&
                matriz[nx][ny] == 0 && visitados[nx][ny] == 0) {
                fila_x[fim] = nx;
                fila_y[fim] = ny;
                fim++;

                visitados[nx][ny] = 1;
                pai_x[nx][ny] = x;
                pai_y[nx][ny] = y;
            }
        }
    }

    return false;
}

int main(){
    L = 8;
    C = 8;

    int mat[8][8] = {
        { 0, 0, 0, 1, 0, 1, 0, 1},
        { 0, 0, 0, 0, 0, 0, 0, 1},
        { 0, 1, 1, 1, 1, 1, 0, 1},
        { 0, 0, 0, 0, 0, 1, 0, 1},
        { 0, 0, 0, 1, 0, 1, 0, 1},
        { 0, 0, 0, 0, 0, 0, 0, 1},
        { 0, 0, 0, 1, 1, 0, 0, 1},
        { 0, 0, 0, 1, 1, 1, 0, 1}
    };

    for(int i = 0; i < L; i++){
        for(int j = 0; j < C; j++){
            matriz[i][j] = mat[i][j];
            visitados[i][j] = 0;
        }
    }

    int xi = 5, yi = 2;
    int xf = 7, yf = 6;

    if (bfs(xi, yi, xf, yf)) {
        cout << "Caminho encontrado!" << endl;
    } else {
        cout << "Não há caminho!" << endl;
    }

    imprime_matriz();
}
