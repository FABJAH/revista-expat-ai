document.addEventListener('DOMContentLoaded', () => {
    // --- Elementos del DOM ---
    const chatInput = document.getElementById('chat-input'); // Input en el Hero
    const sendBtn = document.getElementById('send-btn');
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.getElementById('sidebar');
    const serviceCards = document.querySelectorAll('.service-card');

    // Elementos del Widget de Chat
    const chatWidgetContainer = document.getElementById('chat-widget-container');
    const chatBubble = document.getElementById('chat-bubble');
    const chatWindow = document.getElementById('chat-window');
    const closeChatBtn = document.getElementById('close-chat-btn');
    const messagesContainer = document.getElementById('chat-messages');
    const chatInputWidget = document.getElementById('chat-input-widget');
    const sendBtnWidget = document.getElementById('send-btn-widget');

    // Como el frontend y el backend ahora se sirven desde el mismo lugar,
    // podemos usar una ruta relativa. Esto elimina los problemas de CORS.
    const API_URL = '/api/query';

    // --- Lógica del Chat ---

    const sendQuery = async (queryText) => {
        if (!queryText) return;

        // Añadir mensaje del usuario a la interfaz
        addMessage(queryText, 'user');

        // Limpiar inputs
        chatInput.value = '';
        chatInputWidget.value = '';

        // Mostrar indicador de "escribiendo..."
        const thinkingMessage = addMessage('...', 'bot');

        try {
            // Detecta el idioma del navegador (ej. "es-ES", "en-US") y toma solo las dos primeras letras.
            const lang = navigator.language.split('-')[0];

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Enviamos la pregunta y el idioma detectado
                body: JSON.stringify({ question: queryText, language: lang }),
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

    const handleSendMessage = () => {
        // Usar el valor de cualquiera de los dos inputs que tenga texto
        const question = chatInput.value.trim() || chatInputWidget.value.trim();

        // Si la pregunta viene del input principal (hero), hacer scroll al chat
        if (chatInput.value.trim()) {
            toggleChatWindow(true); // Abrir el widget de chat
        }

        sendQuery(question);
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
        if (data.respuesta) {
            const friendlyDiv = document.createElement('div');
            friendlyDiv.className = 'friendly-text';
            friendlyDiv.textContent = data.respuesta;
            messageDiv.appendChild(friendlyDiv);
        }

        // Resultados en formato de tarjeta
        if (Array.isArray(data.json) && data.json.length > 0) {
            const resultsContainer = document.createElement('div');
            resultsContainer.className = 'results-container';
            data.json.forEach(item => {
                const card = document.createElement('div');
                card.className = 'result-card';

                // Estructura mejorada para más control con CSS
                let cardHTML = `<h3>${item.nombre}</h3><p class="card-description">${item.descripcion}</p>`;

                // Contenedor para los detalles (contacto, precio, etc.)
                const details = `
                    ${item.contacto ? `<p><strong>Contacto:</strong> ${item.contacto}</p>` : ''}
                    ${item.precio ? `<p><strong>Precio:</strong> ${item.precio}</p>` : ''}
                    ${item.ubicacion ? `<p><strong>Ubicación:</strong> ${item.ubicacion}</p>` : ''}
                `;
                if (details.trim()) {
                    cardHTML += `<div class="card-details">${details}</div>`;
                }

                if (item.beneficios && item.beneficios.length > 0) {
                    cardHTML += `<div class="card-benefits"><strong>Beneficios:</strong><ul>${item.beneficios.map(b => `<li>${b}</li>`).join('')}</ul></div>`;
                }
                card.innerHTML = cardHTML;
                resultsContainer.appendChild(card);
            });
            messageDiv.appendChild(resultsContainer);
        } else if (!data.respuesta) {
            // Si no hay resultados ni texto amigable, mostrar un mensaje genérico
            const textResponse = document.createElement('p');
            textResponse.textContent = "No he encontrado información sobre eso, ¿puedes ser más específico?";
            messageDiv.appendChild(textResponse);
        }

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    const addWelcomeMessageWithActions = () => {
        const welcomeText = '¡Hola! Soy tu asistente para la vida en Barcelona. ¿Cómo puedo ayudarte hoy?';
        const messageDiv = addMessage(welcomeText, 'bot');

        // Contenedor para los botones de acción
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'quick-actions-container';

        // Definimos las acciones rápidas
        const actions = [
            { text: '🏨 Alojamiento', query: 'Accommodation' },
            { text: '⚕️ Salud', query: 'Healthcare' },
            { text: '🎓 Educación', query: 'Education' },
            { text: '⚖️ Legal y Finanzas', query: 'Legal and Financial' },
            { text: '🍽️ Restaurantes', query: 'Restaurants' },
            { text: '📢 Anúnciate', query: 'Comercial' }
        ];

        actions.forEach(action => {
            const button = document.createElement('button');
            button.className = 'quick-action-btn';
            button.textContent = action.text;
            button.onclick = () => {
                sendQuery(action.query);
            };
            actionsContainer.appendChild(button);
        });

        messageDiv.appendChild(actionsContainer);
    };
    // --- Event Listeners ---

    // Botones de enviar
    sendBtn?.addEventListener('click', handleSendMessage); // El del hero
    sendBtnWidget.addEventListener('click', handleSendMessage); // El del widget

    // Enviar con la tecla Enter
    [chatInput, chatInputWidget].forEach(input => input?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    });

    // Menú hamburguesa
    hamburger.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Lógica del widget de chat
    const toggleChatWindow = (forceOpen = null) => {
        const isHidden = chatWindow.classList.contains('hidden');
        if (forceOpen === true || isHidden) {
            chatWindow.classList.remove('hidden');
            chatBubble.classList.add('hidden');
        } else if (forceOpen === false || !isHidden) {
            chatWindow.classList.add('hidden');
            chatBubble.classList.remove('hidden');
        }
    };

    chatBubble.addEventListener('click', () => toggleChatWindow(true));
    closeChatBtn.addEventListener('click', () => toggleChatWindow(false));

    // Clic en tarjetas de servicio
    serviceCards.forEach(card => {
        card.addEventListener('click', () => {
            // Obtiene el valor del atributo data-service, que ya coincide
            // con las claves del JSON (ej: "Accommodation", "Healthcare").
            const serviceName = card.dataset.service;

            toggleChatWindow(true); // Abrir el widget de chat
            // Envía la consulta directamente sin usar los inputs de texto
            sendQuery(serviceName);
        });
    });

    // Mensaje de bienvenida
    setTimeout(() => {
        addWelcomeMessageWithActions();
    }, 500);

});
