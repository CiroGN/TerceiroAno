#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void bubbleSortIterativo(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int trocou = 0;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                trocou = 1;
            }
        }
        if (!trocou) break;
    }
}

void bubbleSortRecursivo(int arr[], int n) {
    if (n == 1) return;
    for (int i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            int temp = arr[i];
            arr[i] = arr[i + 1];
            arr[i + 1] = temp;
        }
    }
    bubbleSortRecursivo(arr, n - 1);
}

// gera array aleatório
void gerarArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 100000; 
    }
}

int main() {
    int tamanhos[] = {1000, 2000, 5000, 10000};
    int qtd = sizeof(tamanhos) / sizeof(tamanhos[0]);

    FILE *f = fopen("C:/Users/cirog/source/TerceiroAno/2Semestre/EstruturaDeDados/SeminarioAlgoritmos/BubbleSort/tempos.csv", "w");
    if (!f) {
        printf("Erro ao abrir arquivo!\n");
        return 1;
    }

    fprintf(f, "n,iterativo_ms,recursivo_ms\n");

    for (int k = 0; k < qtd; k++) {
        int n = tamanhos[k];
        int *arr1 = malloc(n * sizeof(int));
        int *arr2 = malloc(n * sizeof(int));

        gerarArray(arr1, n);
        for (int i = 0; i < n; i++) arr2[i] = arr1[i];

        clock_t inicio = clock();
        bubbleSortIterativo(arr1, n);
        clock_t fim = clock();
        double tempo_iter = (double)(fim - inicio) / CLOCKS_PER_SEC * 1000.0;

        inicio = clock();
        bubbleSortRecursivo(arr2, n);
        fim = clock();
        double tempo_rec = (double)(fim - inicio) / CLOCKS_PER_SEC * 1000.0;

        fprintf(f, "%d,%.5f,%.5f\n", n, tempo_iter, tempo_rec);

        free(arr1);
        free(arr2);
    }

    fclose(f);
    printf("Arquivo tempos.csv gerado com sucesso!\n");
    return 0;
}
