#include <stdio.h>
#include <time.h>

void bubbleSortRecursivo(int arr[], int n, int vez) {
    if (n == 1) return;

    for (int i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            int temp = arr[i];
            arr[i] = arr[i + 1];
            arr[i + 1] = temp;
            printf("\nOredenando array na vez %d: ", vez);
            for (int j = 0; j < n; j++) {
                printf("%d ", arr[j]);
            }
        }
        vez++;
    }
    bubbleSortRecursivo(arr, n - 1, vez);
}

int main() {
    int arr[] = {643, 3, 4, 1, 2, 5, 7, 43, 31, 5, 23, 46, 23, 4};
    int n = sizeof(arr) / sizeof(arr[0]); // sizeof * 4 bytes / 4 bytes

    printf("\nArray inicial: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    int vez = 1;
    clock_t inicio = clock();
    bubbleSortRecursivo(arr, n, vez);
    clock_t fim = clock();

    double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC * 1000.0; // ms

    printf("\nArray ordenado: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\nTempo de execucao: %.5f ms\n", tempo);

    return 0;
}
