%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
int yyerror(char *s);
extern int lineno;

int debug = 1;
%}

%union {
    int num;
    char* str;
}

/* Tokens */
%token <str> TYPE VARIABLE STRING
%token <num> NUMBER
%token IF ELSE FOR WHILE BREAK CONTINUE TRY CATCH RETURN STRUCT PRINT
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON EQUAL
%token LESS GREATER LESSEQ GREATEREQ EQUALTO NOTEQUAL
%token AND OR NOT
%token PLUS MINUS TIMES DIVIDE MOD

/* Precedências */
%left OR
%left AND
%left NOT
%left EQUALTO NOTEQUAL
%left LESS GREATER LESSEQ GREATEREQ
%left PLUS MINUS
%left TIMES DIVIDE MOD
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%start program

%%

program:
    function
    { if (debug) printf("Programa reconhecido com sucesso!\n"); }
    ;

function:
    TYPE VARIABLE LPAREN RPAREN LBRACE statements RBRACE
    { if (debug) printf("Função %s reconhecida\n", $2); }
    ;

statements:
    /* vazio */
    | statements statement
    ;

statement:
    declaration SEMICOLON
    | if_statement
    | print_statement SEMICOLON
    | block
    | for_statement
    | while_statement
    | expression SEMICOLON
    | assignment SEMICOLON
    ;

declaration:
    TYPE VARIABLE EQUAL expression
    ;

assignment:
    VARIABLE EQUAL expression
    ;

condition:
    logical_expression
    ;

logical_expression:
    logical_expression OR logical_expression
    | logical_expression AND logical_expression
    | NOT logical_expression
    | comparison_expression
    | LPAREN logical_expression RPAREN
    ;

comparison_expression:
    additive_expression LESS additive_expression
    | additive_expression GREATER additive_expression
    | additive_expression LESSEQ additive_expression
    | additive_expression GREATEREQ additive_expression
    | additive_expression EQUALTO additive_expression
    | additive_expression NOTEQUAL additive_expression
    ;

additive_expression:
    multiplicative_expression
    | additive_expression PLUS multiplicative_expression
    | additive_expression MINUS multiplicative_expression
    ;

multiplicative_expression:
    primary_expression
    | multiplicative_expression TIMES primary_expression
    | multiplicative_expression DIVIDE primary_expression
    | multiplicative_expression MOD primary_expression
    ;

primary_expression:
    VARIABLE
    | NUMBER
    | LPAREN additive_expression RPAREN  /* Alteração crucial aqui */
    ;

expression:
    logical_expression
    | additive_expression
    ;

print_statement:
    PRINT LPAREN STRING RPAREN
    ;

block:
    LBRACE statements RBRACE
    ;

for_statement:
    FOR LPAREN for_init SEMICOLON condition SEMICOLON for_step RPAREN statement
    ;

for_init:
    declaration
    | assignment
    | /* vazio */
    ;

for_step:
    expression
    | assignment
    | /* vazio */
    ;

while_statement:
    WHILE LPAREN condition RPAREN statement
    ;

if_statement:
    IF LPAREN condition RPAREN statement %prec LOWER_THAN_ELSE
    | IF LPAREN condition RPAREN statement ELSE statement
    ;

%%

int yyerror(char *s) {
    fprintf(stderr, "Erro de sintaxe na linha %d: %s\n", lineno, s);
    return 0;
}

int main() {
    if (debug) printf("Iniciando análise...\n");
    int result = yyparse();
    if (debug) printf("Análise concluída com código %d\n", result);
    return result;
}