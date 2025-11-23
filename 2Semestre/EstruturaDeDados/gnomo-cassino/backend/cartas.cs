namespace backend;
public class Carta
{
    public string Naipe { get; set; }
    public int Valor { get; set; }
    public int Serial { get; set; }   // 1..52 used for ordering

    public Carta(string naipe, int valor, int serial)
    {
        Naipe = naipe;
        Valor = valor;
        Serial = serial;
    }
    public Carta()
    {
    }
}