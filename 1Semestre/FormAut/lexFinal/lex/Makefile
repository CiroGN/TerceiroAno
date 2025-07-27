# Makefile para compilador C--

# Nome do executável
EXEC = cmmc

# Fontes
LEX_FILE = regex.lex
YACC_FILE = parser.y

# Gerados
LEX_C = lex.yy.c
YACC_C = parser.tab.c
YACC_H = parser.tab.h

# Compilador
CC = gcc
CFLAGS = -Wall

# Regras
all: $(EXEC)

$(EXEC): $(LEX_C) $(YACC_C)
	$(CC) $(CFLAGS) -o $(EXEC) $(LEX_C) $(YACC_C)

$(LEX_C): $(LEX_FILE)
	flex $(LEX_FILE)

$(YACC_C) $(YACC_H): $(YACC_FILE)
	bison -d $(YACC_FILE)

run:
	@echo "Executando com entrada.cmm..."
	./$(EXEC) < input.cmm

clean:
	rm -f $(EXEC) $(LEX_C) $(YACC_C) $(YACC_H)
