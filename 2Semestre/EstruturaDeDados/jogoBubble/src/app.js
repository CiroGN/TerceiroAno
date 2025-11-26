// Game State
let gameState = {
    initialArray: [],
    playerArray: [],
    referenceArray: [],
    referenceSteps: [],
    currentStep: 0,
    lives: 3,
    arraySize: 5,
    isGameOver: false,
    isWon: false,
    totalMoves: 0,
    correctMoves: 0,
    hintsUsed: 0,
    selectedIndices: [],
    currentReferenceStep: 0
};

// Initialize game with selected difficulty
function startGame(size) {
    gameState.arraySize = size;
    gameState.lives = 3;
    gameState.currentStep = 0;
    gameState.totalMoves = 0;
    gameState.correctMoves = 0;
    gameState.hintsUsed = 0;
    gameState.isGameOver = false;
    gameState.isWon = false;
    gameState.selectedIndices = [];
    gameState.currentReferenceStep = 0;
    
    // Generate shuffled array
    gameState.initialArray = generateShuffledArray(size);
    gameState.playerArray = [...gameState.initialArray];
    
    // Generate reference solution with all intermediate steps
    gameState.referenceSteps = generateBubbleSortSteps([...gameState.initialArray]);
    gameState.referenceArray = gameState.referenceSteps[gameState.referenceSteps.length - 1];
    
    // Show game screen
    document.getElementById('difficultyScreen').classList.add('hidden');
    document.getElementById('gameScreen').classList.remove('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
    
    updateDisplay();
}

// Generate shuffled array with unique values
function generateShuffledArray(size) {
    const array = [];
    const maxValue = 10;
    
    // Generate unique random values
    while (array.length < size) {
        const value = Math.floor(Math.random() * (maxValue + 1));
        if (!array.includes(value)) {
            array.push(value);
        }
    }
    
    // Shuffle using Fisher-Yates algorithm
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    
    return array;
}

// Generate all steps of bubble sort algorithm
function generateBubbleSortSteps(arr) {
    const steps = [];
    const array = [...arr];
    const n = array.length;
    
    // Add initial state
    steps.push([...array]);
    
    // Bubble sort with tracking each swap
    for (let i = 0; i < n - 1; i++) {
        let swapped = false;
        for (let j = 0; j < n - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                // Swap
                [array[j], array[j + 1]] = [array[j + 1], array[j]];
                steps.push([...array]);
                swapped = true;
            }
        }
        // If no swaps were made, array is sorted
        if (!swapped) break;
    }
    
    return steps;
}

// Update display
function updateDisplay() {
    // Update status
    const hearts = '❤️'.repeat(gameState.lives);
    document.getElementById('livesDisplay').textContent = hearts || '💀';
    document.getElementById('stepDisplay').textContent = gameState.currentReferenceStep;
    document.getElementById('movesDisplay').textContent = gameState.totalMoves;
    
    // Display player array
    displayArray('playerArray', gameState.playerArray, true);
    
    // Display reference array (final sorted)
    displayArray('referenceArray', gameState.referenceArray, false);
}

// Display array with interactive cards
function displayArray(containerId, array, isClickable) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    array.forEach((value, index) => {
        const item = document.createElement('div');
        item.className = 'array-item';
        
        const indexLabel = document.createElement('div');
        indexLabel.className = 'array-index';
        indexLabel.textContent = index;
        
        const valueBox = document.createElement('div');
        valueBox.className = 'array-value';
        valueBox.textContent = value;
        
        // Check if this position is correctly sorted
        if (gameState.playerArray[index] === gameState.referenceArray[index]) {
            valueBox.classList.add('correct');
        }
        
        // Check if selected
        if (isClickable && gameState.selectedIndices.includes(index)) {
            valueBox.classList.add('selected');
        }
        
        if (isClickable) {
            valueBox.onclick = () => selectCard(index);
        }
        
        item.appendChild(indexLabel);
        item.appendChild(valueBox);
        container.appendChild(item);
    });
}

// Handle card selection
function selectCard(index) {
    if (gameState.isGameOver) return;
    
    const selectedIdx = gameState.selectedIndices.indexOf(index);
    
    if (selectedIdx > -1) {
        // Deselect
        gameState.selectedIndices.splice(selectedIdx, 1);
    } else {
        // Select
        if (gameState.selectedIndices.length < 2) {
            gameState.selectedIndices.push(index);
        } else {
            // Replace first selection
            gameState.selectedIndices = [gameState.selectedIndices[1], index];
        }
    }
    
    // Enable swap button if two cards selected
    document.getElementById('swapBtn').disabled = gameState.selectedIndices.length !== 2;
    
    updateDisplay();
}

// Perform swap
function performSwap() {
    if (gameState.selectedIndices.length !== 2) return;
    
    const [idx1, idx2] = gameState.selectedIndices.sort((a, b) => a - b);
    
    // Perform swap
    [gameState.playerArray[idx1], gameState.playerArray[idx2]] = 
        [gameState.playerArray[idx2], gameState.playerArray[idx1]];
    
    gameState.totalMoves++;
    
    // Check if this matches the next step in reference
    const isCorrectMove = checkIfCorrectMove();
    
    if (isCorrectMove) {
        gameState.correctMoves++;
        gameState.currentReferenceStep++;
        showMessage('✓ Movimento correto! Continue assim.', 'success');
        
        // Check if player won
        if (arraysEqual(gameState.playerArray, gameState.referenceArray)) {
            gameState.isWon = true;
            endGame();
        }
    } else {
        gameState.lives--;
        showMessage(`✗ Movimento incorreto! Você perdeu uma vida. A troca correta seria entre as posições ${getCorrectSwap()}.`, 'error');
        
        // Undo the swap
        [gameState.playerArray[idx1], gameState.playerArray[idx2]] = 
            [gameState.playerArray[idx2], gameState.playerArray[idx1]];
        
        if (gameState.lives <= 0) {
            gameState.isGameOver = true;
            endGame();
        }
    }
    
    // Clear selection
    gameState.selectedIndices = [];
    document.getElementById('swapBtn').disabled = true;
    
    updateDisplay();
    clearHint();
}

// Check if current move matches any valid next step
function checkIfCorrectMove() {
    // Get the next possible steps from current position
    const nextStepIndex = gameState.currentReferenceStep + 1;
    
    if (nextStepIndex >= gameState.referenceSteps.length) {
        return arraysEqual(gameState.playerArray, gameState.referenceArray);
    }
    
    const nextStep = gameState.referenceSteps[nextStepIndex];
    return arraysEqual(gameState.playerArray, nextStep);
}

// Get the correct swap positions
function getCorrectSwap() {
    const nextStepIndex = gameState.currentReferenceStep + 1;
    
    if (nextStepIndex >= gameState.referenceSteps.length) {
        return 'nenhuma (já está ordenado)';
    }
    
    const currentStep = gameState.referenceSteps[gameState.currentReferenceStep];
    const nextStep = gameState.referenceSteps[nextStepIndex];
    
    // Find which positions differ
    for (let i = 0; i < currentStep.length - 1; i++) {
        if (currentStep[i] !== nextStep[i] && currentStep[i + 1] !== nextStep[i + 1]) {
            return `${i} e ${i + 1}`;
        }
    }
    
    return 'desconhecida';
}

// Compare two arrays
function arraysEqual(arr1, arr2) {
    if (arr1.length !== arr2.length) return false;
    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] !== arr2[i]) return false;
    }
    return true;
}

// Show hint
function showHint() {
    if (gameState.isGameOver) return;
    
    gameState.hintsUsed++;
    const swap = getCorrectSwap();
    
    const hintArea = document.getElementById('hintArea');
    hintArea.innerHTML = `
        <div class="hint-box">
            <strong>💡 Dica:</strong> A próxima troca correta é entre as posições ${swap}.
            <br>
            <small>Lembre-se: no Bubble Sort, comparamos elementos adjacentes e trocamos se o da esquerda for maior que o da direita.</small>
        </div>
    `;
}

// Clear hint
function clearHint() {
    document.getElementById('hintArea').innerHTML = '';
}

// Show message
function showMessage(text, type) {
    const messageArea = document.getElementById('messageArea');
    messageArea.innerHTML = `<div class="message ${type}">${text}</div>`;
    
    // Auto-clear after 3 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            messageArea.innerHTML = '';
        }, 3000);
    }
}

// End game
function endGame() {
    gameState.isGameOver = true;
    
    document.getElementById('gameScreen').classList.add('hidden');
    document.getElementById('gameOverScreen').classList.remove('hidden');
    
    // Calculate efficiency
    const optimalMoves = gameState.referenceSteps.length - 1;
    const efficiency = Math.round((gameState.correctMoves / gameState.totalMoves) * 100) || 0;
    
    // Update stats
    if (gameState.isWon) {
        document.getElementById('gameOverTitle').textContent = '🎉 Parabéns! Você ordenou o array!';
    } else {
        document.getElementById('gameOverTitle').textContent = '💀 Game Over! Suas vidas acabaram.';
    }
    
    document.getElementById('totalMoves').textContent = gameState.totalMoves;
    document.getElementById('correctMoves').textContent = gameState.correctMoves;
    document.getElementById('efficiency').textContent = efficiency + '%';
    document.getElementById('hintsUsed').textContent = gameState.hintsUsed;
}

// Reset game to difficulty selection
function resetGame() {
    document.getElementById('gameScreen').classList.add('hidden');
    document.getElementById('difficultyScreen').classList.remove('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
}