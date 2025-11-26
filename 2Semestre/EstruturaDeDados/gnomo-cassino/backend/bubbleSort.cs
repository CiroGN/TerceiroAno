using Godot;
using System;
using System.Collections.Generic;
namespace backend;

public partial class BubbleSortManager : Node
{
    private List<Carta> cartasIniciais;     // Cartas embaralhadas
    private List<Carta> cartasJogador;      // Onde o jogador mexe
    private List<Carta> cartasAlgoritmo;    // O Bubble Sort irá ordenar
    private Queue<(int i, int j)> passosBubble; // Cada passo de comparação + swap previstos pelo algoritmo

    public int vidas = 3;

    public override void _Ready()
    {
        GerarCartas(10);     // gerar 10 cartas por padrão
        CalcularPassosBubble(); 
    }

    // --------------------------------------------------------------------
    // 1. GERAR CARTAS EMBARALHADAS
    // --------------------------------------------------------------------
    private void GerarCartas(int quantidade)
    {
        // Gera um baralho completo
        List<Carta> baralho = GerarBaralho();

        // Embaralha
        Random rand = new Random();
        for (int i = 0; i < baralho.Count; i++)
        {
            int r = rand.Next(baralho.Count);
            (baralho[i], baralho[r]) = (baralho[r], baralho[i]);
        }

        // Pega apenas a quantidade desejada
        cartasIniciais = baralho.GetRange(0, quantidade);

        // Cria as cópias
        cartasJogador = new List<Carta>(cartasIniciais);
        cartasAlgoritmo = new List<Carta>(cartasIniciais);

        GD.Print("Cartas iniciais:");
        foreach (var c in cartasIniciais)
            GD.Print($"{c.Serial}");
    }

    // --------------------------------------------------------------------
    // 2. GERAÇÃO DO BARALHO COMPLETO
    // --------------------------------------------------------------------
    private List<Carta> GerarBaralho()
    {
        string[] naipes = { "Copas", "Ouros", "Espadas", "Paus" };
        List<Carta> baralho = new List<Carta>();
        int serial = 1;

        foreach (string naipe in naipes)
        {
            for (int valor = 1; valor <= 13; valor++)
            {
                baralho.Add(new Carta
                {
                    Valor = valor,
                    Naipe = naipe,
                    Serial = serial
                });
                serial++;
            }
        }

        return baralho;
    }

    // --------------------------------------------------------------------
    // 3. CALCULAR PASSOS DO BUBBLE SORT (APENAS OS SWAPS)
    // --------------------------------------------------------------------
    private void CalcularPassosBubble()
    {
        passosBubble = new Queue<(int i, int j)>();

        // Bubble Sort clássico, mas **armazenando trocar previstas**
        for (int i = 0; i < cartasAlgoritmo.Count - 1; i++)
        {
            for (int j = 0; j < cartasAlgoritmo.Count - i - 1; j++)
            {
                if (cartasAlgoritmo[j].Serial > cartasAlgoritmo[j + 1].Serial)
                {
                    // Armazena o swap necessário
                    passosBubble.Enqueue((j, j + 1));

                    // Aplica no array do algoritmo
                    (cartasAlgoritmo[j], cartasAlgoritmo[j + 1]) = 
                        (cartasAlgoritmo[j + 1], cartasAlgoritmo[j]);
                }
            }
        }

        GD.Print($"Total de passos do Bubble: {passosBubble.Count}");
    }

    // --------------------------------------------------------------------
    // 4. JOGADOR TENTA FAZER UM SWAP
    // --------------------------------------------------------------------
    public bool JogadorFazSwap(int i, int j)
    {
        if (passosBubble.Count == 0)
        {
            GD.Print("Jogador terminou!");
            return true;
        }

        var proximoPasso = passosBubble.Peek();

        // Verifica se o jogador fez o swap correto
        if (proximoPasso.i == i && proximoPasso.j == j)
        {
            GD.Print("Movimento CORRETO!");

            // realiza o swap no array do jogador
            (cartasJogador[i], cartasJogador[j]) = (cartasJogador[j], cartasJogador[i]);

            // remove esse passo da fila
            passosBubble.Dequeue();
            return true;
        }
        else
        {
            vidas--;
            GD.Print($"Movimento ERRADO! Vidas restantes: {vidas}");

            return false;
        }
    }
}
