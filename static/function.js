let totalMessages = 0;
let offensiveCount = 0;

// Theme handling
const themeToggle = document.getElementById('theme-toggle');
let isDarkMode = false;

themeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    document.body.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
    themeToggle.textContent = isDarkMode ? '☀️' : '🌙';
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
});

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    isDarkMode = savedTheme === 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    themeToggle.textContent = isDarkMode ? '☀️' : '🌙';
}

// Input handling
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

userInput.addEventListener('input', () => {
    sendButton.disabled = !userInput.value.trim();
});

function createMessageElement(text, sender, isOffensive = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    if (sender === 'bot') {
        messageDiv.classList.add(isOffensive ? 'offensive' : 'safe');
    }

    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;

    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();

    messageDiv.appendChild(content);
    messageDiv.appendChild(timestamp);

    return messageDiv;
}

function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message bot typing-indicator';
    indicator.innerHTML = `
        <div class="message-content">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    return indicator;
}

function updateStats() {
    document.getElementById('total-messages').textContent = totalMessages;
    document.getElementById('offensive-count').textContent = offensiveCount;
    
    // Calculate sentiment score as the percentage of non-offensive messages
    const sentimentScore = ((totalMessages - offensiveCount) / totalMessages) * 100;
    document.getElementById('sentiment-score').textContent = 
        totalMessages === 0 ? '0%' : `${Math.round(sentimentScore)}%`;
}

// Sentiment analysis is now handled through the backend response and detectedWords count

function updateAnalysisPanel(text, detectedWords = []) {
    // Calculate toxicity score based on number of detected offensive words
    let toxicityScore = 0;
    let sentimentValue = 'Positive';
    
    if (detectedWords.length === 1) {
        toxicityScore = 60; // 80% for 1 abusive word
        sentimentValue = 'Neutral';
    } else if (detectedWords.length === 2) {
        toxicityScore = 90; // 90% for 2 abusive words
        sentimentValue = 'Negative';
    } else if (detectedWords.length > 2) {
        toxicityScore = 100; // 100% for more than 2 abusive words
        sentimentValue = 'Negative';
    } else {
        toxicityScore = 0; // Default for non-abusive content
        sentimentValue = 'Positive';
    }
    
    const panel = document.getElementById('analysis-panel');
    
    document.getElementById('toxicity-progress').style.width = `${toxicityScore}%`;
    document.getElementById('toxicity-value').textContent = `${toxicityScore}%`;
    
    document.getElementById('sentiment-progress').style.width = `${toxicityScore}%`;
    document.getElementById('sentiment-value').textContent = sentimentValue;
    
    const keywordsContainer = document.getElementById('detected-keywords');
    if (detectedWords && detectedWords.length > 0) {
        keywordsContainer.innerHTML = detectedWords
            .map(word => `<span class="keyword">${word}</span>`)
            .join('');
    } else {
        keywordsContainer.innerHTML = '<span class="no-keywords">No offensive words detected</span>';
    }
    
    panel.classList.add('active');
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    const chatBox = document.getElementById('chat-box');

    // Add user message
    chatBox.appendChild(createMessageElement(text, 'user'));
    userInput.value = '';
    sendButton.disabled = true;
    totalMessages++;

    // Show typing indicator
    const typingIndicator = showTypingIndicator();
    chatBox.appendChild(typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Send message to backend
        const response = await fetch('/get-response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text }),
        });

        const data = await response.json();

        // Remove typing indicator
        typingIndicator.remove();

        // Add bot response
        const isOffensive = data.color === 'red' || data.color === 'orange';
        if (isOffensive) offensiveCount++;

        chatBox.appendChild(createMessageElement(data.response, 'bot', isOffensive));
        chatBox.scrollTop = chatBox.scrollHeight;

        // Update statistics and analysis
        updateStats();
        
        // If backend detected words, use those for visualization
        if (data.detected_words) {
            updateAnalysisPanel(text, data.detected_words);
        } else {
            updateAnalysisPanel(text);
        }

        // Save chat history
        saveChatHistory();
    } catch (error) {
        console.error('Error sending message:', error);
        typingIndicator.remove();
        chatBox.appendChild(createMessageElement('Error processing your message. Please try again.', 'bot', false));
    }
}

function saveChatHistory() {
    // We don't want to save chat history since we're clearing it on page load
    // This function is kept for potential future use if needed
}

function loadChatHistory() {
    const chatBox = document.getElementById('chat-box');

    // Clear localStorage on page load to ensure chat history is not persisted
    localStorage.clear();

    // Initialize with welcome message
    chatBox.innerHTML = `
        <div class="welcome-message">
            <div class="avatar">🤖</div>
            <p>Hello! I'm your AI assistant. I can help analyze messages for abusive language and provide sentiment analysis. How can I assist you today?</p>
        </div>
    `;

    totalMessages = 0;
    offensiveCount = 0;
    updateStats();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    sendButton.disabled = true;
    loadChatHistory();
    updateStats();
    
    // Add event listener for close panel button
    const closeButton = document.querySelector('.close-panel');
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            const panel = document.getElementById('analysis-panel');
            panel.classList.remove('active');
        });
    }
});