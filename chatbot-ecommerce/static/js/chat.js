const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');

userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

function addMessage(content, role) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = `<div class="bubble">${content}</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';

    const typing = document.createElement('div');
    typing.className = 'typing';
    typing.id = 'typing';
    typing.textContent = 'Kai réfléchit...';
    chatMessages.appendChild(typing);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });

    document.getElementById('typing')?.remove();

    const data = await response.json();
    addMessage(data.response, 'assistant');
}