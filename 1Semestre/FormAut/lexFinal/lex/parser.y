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
%token LBRACKET RBRACKET COMMA


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
    TYPE VARIABLE LPAREN argument_list RPAREN LBRACE statements RBRACE
    {
        if (debug) {
            printf("Função %s com argumentos reconhecida\n", $2);
        }
    }
    ;

argument_list:
    /* vazio */
    | argument_declaration
    | argument_list COMMA argument_declaration
    ;

argument_declaration:
    TYPE VARIABLE
    ;


statements:
    /* vazio */
    | statements statement
    ;

statement:
    declaration SEMICOLON
    | assignment SEMICOLON
    | expression SEMICOLON
    | if_statement
    | while_statement
    | for_statement
    | print_statement SEMICOLON
    | return_statement
    | block
    ;

declaration:
    TYPE VARIABLE EQUAL expression
    {
        if (debug) {
            printf("Regex: /%s/ → [tipo de dado] (linha %d)\n", $1, lineno);
            printf("Regex: /%s/ → [declaração de variável] (linha %d)\n", $2, lineno);
        }
    }
    ;

assignment:
    VARIABLE EQUAL expression
    {
        if (debug) {
            printf("Regex: /%s/ → [atribuição de variável] (linha %d)\n", $1, lineno);
        }
    }
    ;

expression:
    logical_expression
    | additive_expression
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
    | LPAREN additive_expression RPAREN
    ;

print_statement:
    PRINT LPAREN STRING RPAREN
    {
        if (debug) {
            printf("Regex: /print/ → [comando de saída] (linha %d)\n", lineno);
            printf("Regex: %s → [mensagem a ser exibida] (linha %d)\n", $3, lineno);
        }
    }
    ;

return_statement:
    RETURN expression SEMICOLON
    {
        if (debug) printf("Regex: /return/ → [retorno de função] (linha %d)\n", lineno);
    }
    ;

block:
    LBRACE statements RBRACE
    ;

if_statement:
    IF LPAREN condition RPAREN statement %prec LOWER_THAN_ELSE
    {
        if (debug) printf("Regex: /if/ → [condição] (linha %d)\n", lineno);
    }
    | IF LPAREN condition RPAREN statement ELSE statement
    {
        if (debug) {
            printf("Regex: /if/ → [condição] (linha %d)\n", lineno);
            printf("Regex: /else/ → [alternativa] (linha %d)\n", lineno);
        }
    }
    ;


condition:
    logical_expression
    ;

while_statement:
    WHILE LPAREN condition RPAREN statement
    {
        if (debug) printf("Regex: /while/ → [laço de repetição] (linha %d)\n", lineno);
    }
    ;

for_statement:
    FOR LPAREN for_init SEMICOLON condition SEMICOLON for_step RPAREN statement
    {
        if (debug) printf("Regex: /for/ → [laço de repetição] (linha %d)\n", lineno);
    }
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
