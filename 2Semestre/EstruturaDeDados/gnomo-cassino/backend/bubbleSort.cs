using System;
using System.Collections.Generic;
using cartas;
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
    void BubbleSortBySerial(List<Carta> cards)
{
    int n = cards.Count;
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - 1 - i; j++)
        {
            if (cards[j].Serial > cards[j + 1].Serial)
            {
                // swap objects
                var tmp = cards[j];
                cards[j] = cards[j + 1];
                cards[j + 1] = tmp;
            }
        }
    }
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
// create deck with serials 1..31
        List<Carta> deck = new List<Carta>();
        string[] naipes = { "Copas", "Paus", "Ouros", "Espadas" };
        for (int i = 1; i <= 31; i++)
        {
            string naipe = naipes[(i - 1) % naipes.Length];
            string valor = (i % 11 == 0) ? "K" : (i % 10 == 0) ? "J" : (i % 9 == 0) ? "Q" : i.ToString(); // example
            deck.Add(new Carta(naipe, valor, i));
        }
        BubbleSortEducacional bubble = new BubbleSortEducacional();
        bubble.BubbleSortBySerial(deck);

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
