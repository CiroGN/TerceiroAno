#include <stdio.h>
#include <time.h>

// Função auxiliar para particionar o array
int particiona(int arr[], int baixo, int alto) {
    int pivo = arr[alto];
    int i = (baixo - 1);

    for (int j = baixo; j < alto; j++) {
        if (arr[j] <= pivo) {
            i++;
            // troca arr[i] e arr[j]
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    // troca arr[i+1] e arr[alto] (coloca o pivo na posição correta)
    int temp = arr[i + 1];
    arr[i + 1] = arr[alto];
    arr[alto] = temp;

    return (i + 1);
}

// Implementação iterativa do Quicksort
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

int main() {
    int arr[] = {643, 3, 4, 1, 2, 5, 7, 43, 31, 5, 23, 46, 23, 4};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("\nArray inicial: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }

    clock_t inicio = clock();
    quickSortIterativo(arr, 0, n - 1); // passando índices corretos
    clock_t fim = clock();

    double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC * 1000.0; // ms

    printf("\nArray ordenado: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }

    printf("\nTempo de execucao: %.5f ms\n", tempo);

    return 0;
}
