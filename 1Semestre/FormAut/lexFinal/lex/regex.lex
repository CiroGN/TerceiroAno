%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"

int lineno = 1;
%}

%option noyywrap
%option nounput
%option noinput

KEYWORD     (break|continue|else|for|if|return|struct|while|print|try|catch)
TYPE        (char|int|long|short|void)
VARIABLE    [a-zA-Z_][a-zA-Z0-9_]*
NUMBER      [0-9]+
STRING      \"([^\\\"]|\\.)*\"

%%

"="         { return EQUAL; }
";"         { return SEMICOLON; }
"("         { return LPAREN; }
")"         { return RPAREN; }
"{"         { return LBRACE; }
"}"         { return RBRACE; }
"<"         { return LESS; }
">"         { return GREATER; }
"<="        { return LESSEQ; }
">="        { return GREATEREQ; }
"=="        { return EQUALTO; }
"!="        { return NOTEQUAL; }
"&&"        { return AND; }
"||"        { return OR; }
"!"         { return NOT; }
"+"         { return PLUS; }
"-"         { return MINUS; }
"*"         { return TIMES; }
"/"         { return DIVIDE; }
"%"         { return MOD; }

"if"        { return IF; }
"else"      { return ELSE; }
"for"       { return FOR; }
"while"     { return WHILE; }
"break"     { return BREAK; }
"continue"  { return CONTINUE; }
"try"       { return TRY; }
"catch"     { return CATCH; }
"return"    { return RETURN; }
"struct"    { return STRUCT; }
"print"     { return PRINT; }

{TYPE}      { yylval.str = strdup(yytext); return TYPE; }
{VARIABLE}  { yylval.str = strdup(yytext); return VARIABLE; }
{NUMBER}    { yylval.num = atoi(yytext); return NUMBER; }
{STRING}    { yylval.str = strdup(yytext); return STRING; }

[ \t]+      { /* ignora espaços */ }
\n          { lineno++; }

.           { /* ignora outros caracteres */ }

%%