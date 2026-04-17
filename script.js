/**
 * EcomChatBot - Frontend JavaScript
 * Handles user interactions and communicates with the backend API.
 */

// DOM element references
const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');
const chatButton = document.getElementById('chat-button');

/**
 * Add a message bubble to the chat interface.
 * 
 * @param {string} content - The message text to display.
 * @param {boolean} isUser - Whether the message is from the user (true) or bot (false).
 */
function addMessage(content, isUser) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`;
    bubble.innerHTML = `<strong>${isUser ? 'You' : 'Bot'}:</strong> ${content}`;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Display a typing indicator animation while waiting for bot response.
 * 
 * @returns {HTMLElement} The typing indicator element.
 */
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'chat-bubble bot-bubble typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    chatBox.appendChild(indicator);
    chatBox.scrollTop = chatBox.scrollHeight;
    return indicator;
}

/**
 * Send user message to the backend and display the response.
 */
function sendMessage() {
    const message = chatInput.value.trim();

    if (message) {
        addMessage(message, true);
        chatInput.value = '';

        const typingIndicator = showTypingIndicator();

        fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            typingIndicator.remove();
            addMessage(data.response, false);
        })
        .catch(error => {
            console.error('Error:', error);
            typingIndicator.remove();
            addMessage('Sorry, an error occurred.', false);
        });
    }
}

// Event listener for send button click
chatButton.addEventListener('click', sendMessage);

// Event listener for Enter key in input field
chatInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});