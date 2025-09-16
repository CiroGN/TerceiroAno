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