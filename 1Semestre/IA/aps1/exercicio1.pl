mora(ciro, centro).
mora(bruno, centro).
mora(maia, sul).
mora(daniel, sul).
mora(eduardo, norte).
mora(fabiana, norte).
mora(natany, meio).

pertence(meio, araucaria).
pertence(centro, curitiba).
pertence(sul, curitiba).
pertence(norte, curitiba).

amigo(ciro, bruno).
amigo(ciro, maia).
amigo(carla, daniel).
amigo(eduardo, fabiana).
amigo(ciro, natany).

tem_carro(natany).
tem_carro(maia).
tem_carro(daniel).
tem_carro(eduardo).

pode_dar_carona(Pessoa1, Pessoa2) :-
    tem_carro(Pessoa1),
    mora(Pessoa1, Bairro1),
    mora(Pessoa2, Bairro2),
    pertence(Bairro1, Zona1),
    pertence(Bairro2, Zona2),
    Zona1 = Zona2, (amigo(Pessoa1, Pessoa2);
    amigo(Pessoa2, Pessoa1)).

/*
Consultas de exemplo:
pode_dar_carona(ciro, bruno).
false, nao tem carro.

pode_dar_carona(maia, daniel).
false, nao sao amigos.

pode_dar_carona(natany, ciro).
false, zonas diferentes.
*/
