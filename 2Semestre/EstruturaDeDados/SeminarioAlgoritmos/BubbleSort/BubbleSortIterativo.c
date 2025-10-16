#include <stdio.h>
#include <time.h>

void bubbleSort(int arr[], int n) {
    int vez = 1;
    for (int i = 0; i < n - 1; i++) {
        int trocou = 0;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                trocou = 1;
                printf("\nOrdenando array na vez %d: ", vez);
                for (int z = 0; z < n; z++) {
                    printf("%d ", arr[z]);
                }
            }
            vez++;
        }
        if (!trocou) break; // já está ordenado
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
    bubbleSort(arr, n);
    clock_t fim = clock();

    double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC * 1000.0; // ms

    printf("\nArray ordenado: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\nTempo de execucao: %.5f ms\n", tempo);

    return 0;
}
