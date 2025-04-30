%{
#include <stdio.h>

void yyerror(const char *str) {
	printf("DESCONHECIDO: %s\n", str);
	return;
}
%}

%option noyywrap

KEYWORD     (break|continue|else|for|if|return|struct|while)
TYPE     (char|int|long|short|void)
IDENTIFIER   [a-zA-Z_][a-zA-Z0-9_]*
NUMBER       [0-9]+
OPERATORS (\+|\-|\*|\/|%|\|\||&&|==|!=|<=|>=|<|>|!)
SYMBOL (!|@|#|\$|%|\^|&|\*|\(|\)|\-|=|\+|\\)


%%

{KEYWORD}  { printf("KEYWORD: %s\n", yytext); }
{TYPE}  { printf("TYPE: %s\n", yytext); }
{IDENTIFIER}  { printf("IDENTIFIER: %s\n", yytext); }
{NUMBER}  { printf("NUMBER: %s\n", yytext); }
{OPERATORS}  { printf("OPERATORS: %s\n", yytext); }
{SYMBOL}  { printf("SYMBOL: %s\n", yytext); }



[ \t\n]      { /* Ignorar espaÃ§os em branco */ }
.            { yyerror(yytext); }

%%

int main() {
	yylex();
}
