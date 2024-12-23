async function sendMessage() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const userMessage = userInput.value.trim();

    if (userMessage) {
        // Display user message
        const userBubble = document.createElement('div');
        userBubble.classList.add('message', 'user');
        userBubble.textContent = `You: ${userMessage}`;
        chatBox.appendChild(userBubble);

        // Clear input field
        userInput.value = '';
        userInput.focus();

        // Scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        // Send message to the backend
        try {
            const response = await fetch('/get-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();

            // Display bot's response with background color styling
            const botBubble = document.createElement('div');
            botBubble.classList.add('message', 'bot');
            botBubble.textContent = `Bot: ${data.response}`;
            // Apply background color based on the response color
            if (data.color === 'red') {
                botBubble.classList.add('offensive');
            } else {
                botBubble.classList.add('non-offensive');
            }
            chatBox.appendChild(botBubble);

            // Scroll to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error('Error:', error);
        }
    }
}