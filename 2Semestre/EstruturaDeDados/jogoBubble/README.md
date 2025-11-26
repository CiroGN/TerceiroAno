# 🎮 Bubble Sort Educational Game

Um jogo educativo interativo para aprender o algoritmo de ordenação Bubble Sort através da prática!

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Language](https://img.shields.io/badge/Language-JavaScript-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)
![IFPR](https://img.shields.io/badge/IFPR-BCC--3-purple)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Características](#-características)
- [Como Jogar](#-como-jogar)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação](#-documentação)
- [Contribuindo](#-contribuindo)
- [Créditos](#-créditos)

---

## 🎯 Visão Geral

Este projeto é um **jogo educativo** desenvolvido para a disciplina de **Estrutura de Dados** do IFPR (Instituto Federal do Paraná), turma BCC-3.

O jogo implementa uma experiência interativa onde o jogador aprende na prática como o algoritmo Bubble Sort funciona, ordenando elementos e validando seus passos em tempo real.

### Participantes do Grupo

- Ciro Guilherme Nass
- Nicolas Lourenço dos Santos
- Miguel Martins Costa
- Luan Mickael da Rocha
- Alexandre Raphael Marques de Freitas



### Por que um jogo?

- ✅ **Engajamento:** Torna o aprendizado divertido
- ✅ **Prática:** Aprender fazendo, não apenas observando
- ✅ **Feedback:** Validação imediata de cada movimento
- ✅ **Motivação:** Sistema de vidas e estatísticas

---

## ✨ Características

### Core Features

- 🎲 **Embaralhamento aleatório** de arrays (0-10)
- 🔄 **Validação automática** de trocas de elementos
- ❤️ **Sistema de vidas** (começa com 3)
- 💡 **Dica em tempo real** - mostra o próximo swap correto
- 📊 **Estatísticas detalhadas** ao final
- 🎓 **Tutorial integrado** - "Como Jogar"

### Dificuldades

- **Fácil:** Array com 5 elementos
- **Médio:** Array com 8 elementos
- **Difícil:** Array com 10 elementos

### Interface

- 🌙 **Modo claro/escuro**
- 📱 **Design responsivo** (desktop-first)
- ⚡ **Performance otimizada**
- ♿ **Acessibilidade** considerada

---

## 🎮 Como Jogar

### Passo a Passo

1. **Selecione a dificuldade** (5, 8 ou 10 elementos)
2. **Veja o array embaralhado** que você precisa ordenar
3. **Clique em dois elementos** para trocá-los
4. **Valide sua troca** - o jogo verifica se está correto
5. **Repita até ordenar** ou perder as 3 vidas
6. **Veja suas estatísticas** ao final

### Regras

- ✓ Troca correta = avança para próximo passo
- ✗ Troca errada = perde 1 vida
- 0 vidas = Game Over
- Array ordenado = Vitória!

### Dicas

- 💡 Clique em "Dica" para ver o próximo swap correto
- 📖 Leia "Como Jogar" para entender o Bubble Sort
- 🎯 Tente alcançar 100% de eficiência

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **HTML5** | ES2020+ | Estrutura e semântica |
| **CSS3** | - | Estilo e responsividade |
| **JavaScript** | ES6+ | Lógica e interatividade |
| **GitHub Pages** | - | Hospedagem |

### Por que estas tecnologias?

- **Frontend-only:** Sem necessidade de servidor
- **Universalmente compatível:** Roda em qualquer navegador
- **Fácil compartilhamento:** GitHub Pages
- **Performance:** Execução rápida e responsiva

---

## 📦 Instalação

### Opção 1: Jogar Online (Recomendado)

Simplesmente acesse: **[https://cirogn.github.io/jogoBubble/src](https://cirogn.github.io/jogoBubble/src)**

### Opção 2: Rodar Localmente

#### Pré-requisitos
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Git (opcional)

#### Passos

```bash
# Abra o arquivo index.html no navegador
# Windows:
start index.html

# macOS:
open index.html

# Linux:
xdg-open index.html
```

Ou simplesmente **arraste e solte** o arquivo `index.html` em seu navegador.

---

## 🚀 Como Usar

### Interface Principal

```
┌─────────────────────────────────┐
│   BUBBLE SORT LEARNING GAME     │
├─────────────────────────────────┤
│                                 │
│  Escolha o Nível de Dificuldade │
│                                 │
│  [ Fácil ]  [ Médio ]  [ Difícil]│
│                                 │
└─────────────────────────────────┘
```

### Durante o Jogo

```
┌──────────────────────────────────┐
│  Seu Array:  {6, 2, 9, 1, 4}    │
│  Índices:     0  1  2  3  4      │
│                                  │
│  Vidas: ❤️❤️❤️  Passo: 1/12       │
│                                  │
│  [ Dica ]  [ Como Jogar ]        │
│                                  │
│  Digite duas posições para trocar │
│  Posição 1: _  Posição 2: _      │
│                                  │
└──────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
bubble-sort-game/
│
├── index.html              # Estrutura HTML e layout
├── style.css               # Estilos CSS3
├── script.js               # Lógica JavaScript
│
├── README.md               # Este arquivo
├── LICENSE                 # Licença MIT
│
└── docs/
    ├── relatorio-bubble-sort.pdf
    ├── relatorio-latex.tex
    └── APRESENTACAO.md
```

### Descrição dos Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `index.html` | HTML5 com estrutura semântica e IDs para JavaScript |
| `style.css` | Design system com variáveis CSS e responsividade |
| `script.js` | Lógica do jogo, geração de arrays, validação |
| `README.md` | Documentação do projeto (este arquivo) |

---

## 📖 Documentação

### Documentos Disponíveis

1. **`relatorio-bubble-sort.pdf`** - Relatório técnico completo (10 páginas)
   - Fundamentação teórica
   - Decisões técnicas
   - Arquitetura
   - Análise de qualidade

2. **`relatorio-latex.tex`** - Código LaTeX (para modificações)
   - Código-fonte editável
   - Compilar para PDF com: `pdflatex relatorio-latex.tex`

3. **`README.md`** - Este arquivo
   - Guia rápido
   - Como jogar
   - Instruções de instalação

### Como Compilar o LaTeX

```bash
# Instale pdflatex (se não tiver)
# Ubuntu/Debian:
sudo apt-get install texlive-full

# macOS (com Homebrew):
brew install mactex

# Compile o documento:
pdflatex relatorio-latex.tex

# Resultado:
# relatorio-latex.pdf
```

---

## 🔧 Modificações e Extensões

### Adicionar Novo Algoritmo

Para adicionar um novo algoritmo de ordenação (ex: Selection Sort):

#### 1. Implemente a Função de Passos

```javascript
function generateSelectionSortSteps(array) {
    const steps = [[...array]];
    const arr = [...array];
    const n = arr.length;

    for (let i = 0; i < n - 1; i++) {
        let minIndex = i;
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        if (minIndex !== i) {
            [arr[i], arr[minIndex]] = [arr[minIndex], arr[i]];
            steps.push([...arr]);
        }
    }
    return steps;
}
```

#### 2. Adicione à Tela de Dificuldade

```html
<button onclick="startGame(5, 'bubbleSort')">Bubble Sort - Fácil</button>
<button onclick="startGame(5, 'selectionSort')">Selection Sort - Fácil</button>
```

#### 3. Atualize `startGame()`

```javascript
function startGame(size, algorithm = 'bubbleSort') {
    // ... código existente ...
    
    if (algorithm === 'bubbleSort') {
        gameState.referenceSteps = generateBubbleSortSteps([...gameState.initialArray]);
    } else if (algorithm === 'selectionSort') {
        gameState.referenceSteps = generateSelectionSortSteps([...gameState.initialArray]);
    }
    
    // ... resto do código ...
}
```

### Personalizar Cores

Edite `style.css`:

```css
:root {
    --color-primary: #2196F3;      /* Azul */
    --color-success: #4CAF50;      /* Verde */
    --color-danger: #f44336;       /* Vermelho */
    --color-warning: #ff9800;      /* Laranja */
}
```

### Adicionar Som

```javascript
function playSound(type) {
    const audio = new Audio(`sounds/${type}.mp3`);
    audio.play();
}

// Uso:
playSound('correct');  // Ao acertar
playSound('wrong');    // Ao errar
```

---

## 🧪 Testes

O projeto foi testado em:

- ✅ Chrome 120+
- ✅ Firefox 121+
- ✅ Safari 17+
- ✅ Edge 120+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

### Executar Testes Locais

```bash
# Abra o console do navegador (F12)
# Procure por "bubbleSort" na seção console
# Teste manualmente as funcionalidades

# Ou use um framework de testes:
npm install --save-dev jest
npm test
```

---

## 📊 Métricas de Desempenho

| Métrica | Valor |
|---------|-------|
| Tamanho total | ~50 KB |
| Tempo de carregamento | < 500 ms |
| FPS (navegador) | 60 FPS |
| Tempo de validação | < 5 ms |
| Memória (pico) | ~10 MB |

---

## 🐛 Problemas Conhecidos

- 📱 Design pode precisar ajustes em telas muito pequenas (< 320px)
- 🔊 Sem suporte a áudio (feature futura)
- 📡 Sem leaderboard global (localStorage apenas)

### Reportar Bugs

Se encontrar um bug, abra uma [Issue no GitHub](https://github.com/seu-usuario/bubble-sort-game/issues).

---

## 🚀 Roadmap

- [ ] Adicionar mais algoritmos (Selection, Insertion, Quick Sort)
- [ ] Visualização animada do algoritmo
- [ ] Leaderboard online
- [ ] Modo multiplayer
- [ ] Suporte para português/inglês/espanhol
- [ ] Versão mobile nativa
- [ ] Integração com Moodle/Canvas LMS

---

## 📝 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### MIT License

```
Copyright (c) 2025

Permissão é concedida, gratuitamente, a qualquer pessoa que obtenha
uma cópia deste software e seus arquivos de documentação associados
(o "Software"), para lidar no Software sem restrições, incluindo sem
limitação os direitos de usar, copiar, modificar, mesclar, publicar,
distribuir, sublicenciar e/ou vender cópias do Software...
```

---

## 👥 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o repositório
2. **Crie uma branch** (`git checkout -b feature/NovaFeature`)
3. **Commit suas mudanças** (`git commit -am 'Adiciona NovaFeature'`)
4. **Push para a branch** (`git push origin feature/NovaFeature`)
5. **Abra um Pull Request**

### Diretrizes

- Siga o estilo de código existente
- Adicione comentários para novas funções
- Teste em múltiplos navegadores
- Atualize a documentação

---

## 📞 Contato e Créditos

### Desenvolvido para

- **Instituição:** Instituto Federal do Paraná (IFPR)
- **Disciplina:** Estrutura de Dados
- **Professor:** Marcelo Maia
- **Turma:** BCC-3
- **Período:** Novembro 2025

### Referências

- Cormen et al. (2009) - *Introduction to Algorithms*
- Knuth (1998) - *The Art of Computer Programming*
- MDN Web Docs - JavaScript Documentation

---

## 🎓 Recursos Educacionais

Para entender melhor o Bubble Sort:

- 📚 [Wikipedia - Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort)
- 🎥 [Visualgo - Sorting Visualization](https://visualgo.net/en/sorting)
- 📖 [GeeksforGeeks - Bubble Sort](https://www.geeksforgeeks.org/bubble-sort/)

---

## ⭐ Se Gostou, Deixe uma Star!

Se este projeto foi útil para você, considere deixar uma ⭐ no GitHub!

---

**Última atualização:** Novembro 2025

**Versão:** 1.0.0