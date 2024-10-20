document.addEventListener("DOMContentLoaded", function() {
    const inputField = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatContainer = document.getElementById("chat-container");

    function sendMessage() {
        const userMessage = inputField.value;
        if (!userMessage.trim()) return;

        // Add user message to chat
        const userBubble = document.createElement('div');
        userBubble.classList.add('chat-bubble', 'user-message', 'message-box');
        userBubble.innerHTML = `<span class="user-icon"><img src="static/images/passenger-icon.png" class="icon"></span>${userMessage}`;
        chatContainer.appendChild(userBubble);

        // Clear input field
        inputField.value = '';

        // Scroll to the bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Simulate bot response
        setTimeout(() => {
            const botBubble = document.createElement('div');
            botBubble.classList.add('chat-bubble', 'bot-message', 'message-box');
            botBubble.innerHTML = `<img src="static/images/plane-icon.png" class="icon">Processing your request...`;
            chatContainer.appendChild(botBubble);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 1000);

        // Send user message to server (API call)
        fetch('/webhooks/rest/webhook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            const botBubble = document.createElement('div');
            botBubble.classList.add('chat-bubble', 'bot-message', 'message-box');
            const botReply = data[0]?.text || "I'm sorry, I didn't understand that.";
            botBubble.innerHTML = `<img src="static/images/plane-icon.png" class="icon">${botReply}`;
            chatContainer.appendChild(botBubble);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        })
        .catch(() => {
            const botBubble = document.createElement('div');
            botBubble.classList.add('chat-bubble', 'bot-message', 'message-box');
            botBubble.innerHTML = `<img src="static/images/plane-icon.png" class="icon">Error occurred while connecting to the bot.`;
            chatContainer.appendChild(botBubble);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        });
    }

    // Send message on Enter key press
    inputField.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Send message on button click
    sendButton.addEventListener("click", sendMessage);
});
