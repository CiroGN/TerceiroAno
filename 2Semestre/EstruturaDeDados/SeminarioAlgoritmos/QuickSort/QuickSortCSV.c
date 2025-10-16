#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// ---------- Funções de QuickSort ----------
int particiona(int arr[], int baixo, int alto) {
    int pivo = arr[alto];
    int i = (baixo - 1);
    for (int j = baixo; j < alto; j++) {
        if (arr[j] <= pivo) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i + 1];
    arr[i + 1] = arr[alto];
    arr[alto] = temp;
    return (i + 1);
}

void quickSortRecursivo(int arr[], int baixo, int alto) {
    if (baixo < alto) {
        int pi = particiona(arr, baixo, alto);
        quickSortRecursivo(arr, baixo, pi - 1);
        quickSortRecursivo(arr, pi + 1, alto);
    }
}

void quickSortIterativo(int arr[], int baixo, int alto) {
    int pilha[alto - baixo + 1];
    int topo = -1;

    pilha[++topo] = baixo;
    pilha[++topo] = alto;

    while (topo >= 0) {
        alto = pilha[topo--];
        baixo = pilha[topo--];

        int p = particiona(arr, baixo, alto);

        if (p - 1 > baixo) {
            pilha[++topo] = baixo;
            pilha[++topo] = p - 1;
        }
        if (p + 1 < alto) {
            pilha[++topo] = p + 1;
            pilha[++topo] = alto;
        }
    }
}

// ---------- Função para gerar array aleatório ----------
void gerarArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100000; // números entre 0 e 100000
    }
}

// ---------- Programa principal ----------
int main() {
    FILE *file = fopen("C:/Users/cirog/source/TerceiroAno/2Semestre/EstruturaDeDados/SeminarioAlgoritmos/QuickSort/tempos_quicksort.csv", "w");
    if (!file) {
        printf("Erro ao criar o arquivo CSV!\n");
        return 1;
    }

    fprintf(file, "n,recursivo,iterativo\n");

    srand(time(NULL));

    // Testar com diferentes tamanhos de entrada
    for (int n = 1000; n <= 10000; n += 1000) {
        int *arr1 = (int *)malloc(n * sizeof(int));
        int *arr2 = (int *)malloc(n * sizeof(int));

        gerarArray(arr1, n);
        for (int i = 0; i < n; i++) arr2[i] = arr1[i]; // cópia

        clock_t inicio, fim;
        double tempo_rec, tempo_iter;

        // Recursivo
        inicio = clock();
        quickSortRecursivo(arr1, 0, n - 1);
        fim = clock();
        tempo_rec = (double)(fim - inicio) / CLOCKS_PER_SEC;

        // Iterativo
        inicio = clock();
        quickSortIterativo(arr2, 0, n - 1);
        fim = clock();
        tempo_iter = (double)(fim - inicio) / CLOCKS_PER_SEC;

        fprintf(file, "%d,%f,%f\n", n, tempo_rec, tempo_iter);

        free(arr1);
        free(arr2);
    }

    fclose(file);
    printf("Arquivo tempos_quicksort.csv gerado com sucesso!\n");

    return 0;
}
