aluno(joao, calculo).
aluno(maria, calculo).
aluno(joel, programacao).
aluno(joel, estrutura).

frequenta(joao, puc).
frequenta(maria, puc).
frequenta(joel, ufrj).

professor(carlos, calculo).
professor(ana_paula, estrutura).
professor(pedro, programacao).

funcionario(pedro, ufrj).
funcionario(ana_paula, puc).
funcionario(carlos, puc).

alunos_do_professor(Professor, Aluno) :-
    professor(Professor, Disciplina),
    aluno(Aluno, Disciplina).

pessoa_associada_a_universidade(Pessoa, Universidade) :-
    (aluno(Pessoa, Disciplina), frequenta(Pessoa, Universidade));
    (professor(Professor, Disciplina), funcionario(Professor, Universidade), Pessoa = Professor).

/*Consultas de exemplo:
alunos_do_professor(carlos, X).
X = joao ;
X = maria.

pessoa_associada_a_universidade(pedro, X).
X = ufrj.*/
