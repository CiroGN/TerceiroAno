potencia(_,0,1).

potencia(X,Y,V):-
    Y>0,
    Y1 is Y-1,
    potencia(X,Y1,V1),
    v is X * V1.