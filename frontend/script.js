document.addEventListener('DOMContentLoaded', () => {
    // --- Elementos del DOM ---
    const chatInput = document.getElementById('chat-input'); // Input en el Hero
    const sendBtn = document.getElementById('send-btn');
    const chatInput2 = document.getElementById('chat-input2'); // Input en el chat
    const sendBtn2 = document.getElementById('send-btn2');
    const messagesContainer = document.getElementById('chat-messages');
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.getElementById('sidebar');
    const serviceCards = document.querySelectorAll('.service-card');

    const API_URL = 'http://127.0.0.1:8000/api/query';

    // --- Lógica del Chat ---

    const handleSendMessage = async () => {
        // Usar el valor de cualquiera de los dos inputs que tenga texto
        let question = chatInput.value.trim() || chatInput2.value.trim();
        if (!question) return;

        // Añadir mensaje del usuario a la interfaz
        addMessage(question, 'user');

        // Limpiar ambos inputs
        chatInput.value = '';
        chatInput2.value = '';

        // Mostrar indicador de "escribiendo..."
        const thinkingMessage = addMessage('...', 'bot');

        try {
            // Detecta el idioma del navegador (ej. "es-ES", "en-US") y toma solo las dos primeras letras.
            const lang = navigator.language.split('-')[0];

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Enviamos la pregunta y el idioma detectado
                body: JSON.stringify({ question, language: lang }),
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const data = await response.json();
            updateBotMessage(thinkingMessage, data);

        } catch (error) {
            // --- DIAGNÓSTICO MEJORADO ---
            // Muestra el error técnico real en la consola del navegador (F12 -> Consola)
            console.error('--- ERROR DE CONEXIÓN DETALLADO ---');
            console.error(error);
            console.error('------------------------------------');
            const errorData = {
                respuesta: "Lo siento, ha ocurrido un error de conexión. Asegúrate de que el servidor esté funcionando y vuelve a intentarlo.",
                json: []
            };
            updateBotMessage(thinkingMessage, errorData);
        }
    };

    const addMessage = (text, type) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        if (type === 'bot' && text === '...') {
            messageDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        } else {
            messageDiv.textContent = text;
        }

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return messageDiv;
    };

    const updateBotMessage = (messageDiv, data) => {
        messageDiv.innerHTML = ''; // Limpiar el indicador de "escribiendo"

        // Mensaje amigable del orquestador
        if (data.friendly) {
            const friendlyDiv = document.createElement('div');
            friendlyDiv.className = 'friendly-text';
            friendlyDiv.textContent = data.friendly;
            messageDiv.appendChild(friendlyDiv);
        }

        // Resultados en formato de tarjeta
        if (Array.isArray(data.json) && data.json.length > 0) { // Ahora data.json es directamente el array
            const resultsContainer = document.createElement('div');
            resultsContainer.className = 'results-container';
            data.json.forEach(item => {
                const card = document.createElement('div');
                card.className = 'result-card';
                let cardHTML = `<h3>${item.nombre}</h3><p>${item.descripcion}</p>`;
                if (item.contacto) cardHTML += `<p><strong>Contacto:</strong> ${item.contacto}</p>`;
                if (item.precio) cardHTML += `<p><strong>Precio:</strong> ${item.precio}</p>`;
                if (item.ubicacion) cardHTML += `<p><strong>Ubicación:</strong> ${item.ubicacion}</p>`;
                if (item.beneficios && item.beneficios.length > 0) {
                    cardHTML += `<strong>Beneficios:</strong><ul>${item.beneficios.map(b => `<li>${b}</li>`).join('')}</ul>`;
                }
                card.innerHTML = cardHTML;
                resultsContainer.appendChild(card);
            });
            messageDiv.appendChild(resultsContainer);
        } else {
            // Si no hay JSON, mostrar la respuesta de texto plano
            const textResponse = document.createElement('p');
            textResponse.textContent = data.respuesta || "No he encontrado información sobre eso, ¿puedes ser más específico?";
            messageDiv.appendChild(textResponse);
        }

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    // --- Event Listeners ---

    // Botones de enviar
    sendBtn.addEventListener('click', handleSendMessage);
    sendBtn2.addEventListener('click', handleSendMessage);

    // Enviar con la tecla Enter
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    });
    chatInput2.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    });

    // Menú hamburguesa
    hamburger.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Clic en tarjetas de servicio
    serviceCards.forEach(card => {
        card.addEventListener('click', () => {
            const service = card.dataset.service;
            const question = `Quiero información sobre ${service}`;
            chatInput2.value = question; // Poner la pregunta en el input del chat

            // Scroll hacia la sección de chat
            document.getElementById('chat').scrollIntoView({ behavior: 'smooth' });

            // Enviar el mensaje
            handleSendMessage();
        });
    });

    // Mensaje de bienvenida
    setTimeout(() => {
        addMessage('¡Hola! Soy tu asistente para la vida en Barcelona. Pregúntame sobre alojamiento, trámites legales, salud y más.', 'bot');
    }, 500);
});
