#include <stdio.h>
#include <time.h>

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

void quickSort(int arr[], int baixo, int alto) {
    if (baixo < alto) {
        int pi = particiona(arr, baixo, alto);
        quickSort(arr, baixo, pi - 1);
        quickSort(arr, pi + 1, alto);
    }
}

int main() {
    int arr[] = {643, 3, 4, 1, 2, 5, 7, 43, 31, 5, 23, 46, 23, 4};
    int n = sizeof(arr) / sizeof(arr[0]); // sizeof * 4 bytes / 4 bytes

    printf("\nArray inicial: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    clock_t inicio = clock();
    quickSort(arr, 0, n - 1);
    clock_t fim = clock();

    double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC * 1000.0; // ms

    printf("\nArray ordenado: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\nTempo de execucao: %.5f ms\n", tempo);

    return 0;
}
