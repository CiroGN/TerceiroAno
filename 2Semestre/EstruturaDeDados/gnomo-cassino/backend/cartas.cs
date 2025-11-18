public class Carta
{
    public string Naipe { get; set; }
    public string Valor { get; set; }
    public int Serial { get; set; }   // 1..31 used for ordering

    public Carta(string naipe, string valor, int serial)
    {
        Naipe = naipe;
        Valor = valor;
        Serial = serial;
    }
}