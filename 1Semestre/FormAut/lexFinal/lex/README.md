# Compilador C−−

**Integrante(s):**  
- Ciro Guilherme Nass
- Rafael Correia Alves

## Descrição
Este projeto é um compilador simples para a linguagem fictícia C−−, baseada em um subconjunto da linguagem C.  
Foi implementado usando as ferramentas **Flex (analisador léxico)** e **Bison (analisador sintático)**.

## Estrutura do Projeto

- `regex.lex` — analisador léxico
- `parser.y` — analisador sintático
- `Makefile` — automatiza compilação
- `input.cmm` — arquivo de exemplo para testes

## Compilação

Para compilar o projeto, basta rodar:

```bash
make
```

## Rodar

Para rodar o projeto, basta rodar:

```bash
make run
```

## Excluir para aplicar mudanças dos analizadores

Para excluir arquivos poscompilados, basta rodar:

```bash
make clean
```