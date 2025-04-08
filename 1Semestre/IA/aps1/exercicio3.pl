nota(joao, 5.0).
nota(maria, 6.0).
nota(joana, 8.0).
nota(mariana, 9.0).
nota(cleuza, 8.5).
nota(jose, 6.5).
nota(joaquim, 4.5).
nota(mara, 4.0).
nota(mary, 10.0).

situacao_aluno(Aluno, Situacao) :-
    nota(Aluno, Nota),
    (Nota >= 7.0 -> Situacao = aprovado;
     Nota >= 5.0 -> Situacao = recuperacao;
     Situacao = reprovado).

/*Consultas de exemplo:
situacao_aluno(joao, X).
X = recuperacao.

situacao_aluno(mary, X).
X = aprovado.

situacao_aluno(mara, X).
X = reprovado.*/