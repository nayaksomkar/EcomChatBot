const chatBox = document.getElementById('chat-box');
        const chatInput = document.getElementById('chat-input');
        const chatButton = document.getElementById('chat-button');

        function addMessage(content, isUser) {
            const bubble = document.createElement('div');
            bubble.className = `chat-bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`;
            bubble.innerHTML = `<strong>${isUser ? 'You' : 'Bot'}:</strong> ${content}`;
            chatBox.appendChild(bubble);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function showTypingIndicator() {
            const indicator = document.createElement('div');
            indicator.className = 'chat-bubble bot-bubble typing-indicator';
            indicator.innerHTML = '<span></span><span></span><span></span>';
            chatBox.appendChild(indicator);
            chatBox.scrollTop = chatBox.scrollHeight;
            return indicator;
        }

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

        chatButton.addEventListener('click', sendMessage);

        chatInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });