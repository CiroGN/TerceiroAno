#include <iostream>
using namespace std;

void imprime_matriz();
const int MAX = 100;
int matriz[MAX][MAX];
int visitados[MAX][MAX];
int L, C;

// DFS - implementação recursiva
bool dfs(int x, int y, int xf, int yf){

    // verificação de parada
    // Quando retorna falso??? Fora da matriz, barreira (1), já visitada
    
    if (x >= C || x < 0 || y < 0 || y >= L || matriz[x][y] == 1 || visitados[x][y] == 1 ){
        return false;
    }

    // marcar posição como visitada
    visitados[x][y] = 1;

    // verifica o objetivo (chegar no ponto final)
    if (x == xf && y == yf){
	matriz[x][y] = 2;
        return true;
    }

    // chamar a recursão para toda a vizinhança
    if ( dfs(x, y-1, xf, yf) || // cima
        dfs(x-1, y, xf, yf) || // esquerda
        dfs(x, y+1, xf, yf) || // baixo
        dfs(x+1, y, xf, yf) ) // direitta
        {
    	    matriz[x][y] = 2;
	    imprime_matriz();
    	    return true;
    }


    return false;

}

void imprime_matriz(){
    for(int i=0; i<C; i++){
        for(int j=0; j<L; j++){
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
    // copiar para a matriz global
    for(int i=0; i < L; i++){
        for(int j=0; j < C; j++){
            matriz[i][j] = mat[i][j];
        }
    }
    // definir ponto de partida
    int xi = 5;
    int yi = 2;

    // ponto de chegada
    int xf = 7;
    int yf = 6;

    if (dfs(xi, yi, xf, yf)) {
        cout << "Caminho encontrado!" << endl;
    }else{
        cout << "Não há caminho!" << endl;
    }

    imprime_matriz();	

}