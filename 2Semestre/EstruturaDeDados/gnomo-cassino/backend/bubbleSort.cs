using System;
using System.Collections.Generic;

// Representa um passo do algoritmo
public class BubbleStep
{
    public int IndexA { get; set; }   // primeiro índice comparado
    public int IndexB { get; set; }   // segundo índice comparado
    public bool HouveTroca { get; set; }
    public int[] EstadoAtual { get; set; }
}

public class BubbleSortEducacional
{
    public List<BubbleStep> Passos { get; private set; } = new List<BubbleStep>();

    // Executa o bubble sort registrando cada passo
    public int[] OrdenarComPassos(int[] arrayOriginal)
    {
        int[] arr = (int[])arrayOriginal.Clone();
        int n = arr.Length;

        Passos.Clear();

        for (int i = 0; i < n - 1; i++)
        {
            for (int j = 0; j < n - i - 1; j++)
            {
                bool troca = false;

                // Se A > B troca
                if (arr[j] > arr[j + 1])
                {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    troca = true;
                }

                // Grava o passo atual
                Passos.Add(new BubbleStep
                {
                    IndexA = j,
                    IndexB = j + 1,
                    HouveTroca = troca,
                    EstadoAtual = (int[])arr.Clone()
                });
            }
        }

        return arr;
    }

    // Valida se o movimento do jogador corresponde ao passo correto
    public bool VerificarMovimento(int passo, int indexA, int indexB, bool jogadorTrocou)
    {
        if (passo >= Passos.Count)
            return false;

        BubbleStep p = Passos[passo];

        // O jogador precisa comparar os mesmos índices
        if (p.IndexA != indexA || p.IndexB != indexB)
            return false;

        // Se o algoritmo troca, o jogador deve trocar também
        if (p.HouveTroca != jogadorTrocou)
            return false;

        return true;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        int[] arr = { 5, 3, 8, 1, 4 };

        BubbleSortEducacional bubble = new BubbleSortEducacional();
        bubble.OrdenarComPassos(arr);

        Console.WriteLine("Passos registrados:");
        int i = 0;

        foreach (var p in bubble.Passos)
        {
            Console.WriteLine($"Passo {i++}: comparou [{p.IndexA}] com [{p.IndexB}] - Troca: {p.HouveTroca}");
            Console.WriteLine("Estado: " + string.Join(", ", p.EstadoAtual));
            Console.WriteLine();
        }
    }
}
