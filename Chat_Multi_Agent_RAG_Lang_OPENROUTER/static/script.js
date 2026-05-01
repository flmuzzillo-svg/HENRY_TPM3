const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');

function appendMessage(text, type, intent = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}`;
    
    let content = `<div class="bubble">${text}</div>`;
    if (intent) {
        content += `<div class="intent-tag">Dominio: ${intent}</div>`;
    }
    
    msgDiv.innerHTML = content;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot loading-container';
    loadingDiv.id = 'loading-indicator';
    loadingDiv.innerHTML = `
        <div class="bubble loading">
            <span></span><span></span><span></span>
        </div>
    `;
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeLoading() {
    const indicator = document.getElementById('loading-indicator');
    if (indicator) indicator.remove();
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Agregar mensaje del usuario
    appendMessage(message, 'user');
    userInput.value = '';
    
    // Mostrar loading
    showLoading();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        
        removeLoading();
        
        if (data.status === 'success' || data.status === 'no_domain') {
            appendMessage(data.response, 'bot', data.intent);
        } else {
            appendMessage('Lo siento, hubo un error procesando tu solicitud.', 'bot');
        }
    } catch (error) {
        removeLoading();
        appendMessage('Error de conexión con el servidor.', 'bot');
        console.error(error);
    }
});
