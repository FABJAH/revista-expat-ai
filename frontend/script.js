document.addEventListener('DOMContentLoaded', () => {
    // --- Elementos del DOM ---
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('close-sidebar');
    const serviceCards = document.querySelectorAll('.service-card');
    const guideButtons = document.querySelectorAll('.guide-btn');
    const advertiserButtons = document.querySelectorAll('.advertiser-btn');

    // Elementos del Widget de Chat
    const chatBubble = document.getElementById('chat-bubble');
    const chatWindow = document.getElementById('chat-window');
    const closeChatBtn = document.getElementById('close-chat-btn');
    const messagesContainer = document.getElementById('chat-messages');
    const chatInputWidget = document.getElementById('chat-input-widget');
    const sendBtnWidget = document.getElementById('send-btn-widget');

    // Carrusel
    const carousel = document.getElementById('carousel');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    const apiBase = (window.location.protocol === 'file:' || window.location.origin === 'null')
        ? 'http://127.0.0.1:8000'
        : window.location.origin;
    const API_URL = `${apiBase}/api/query`;
    const API_URL_ADS = `${apiBase}/api/bot/advertising`;

    // --- Lógica del Chat ---

    // Estado de paginación por sesión
    let lastQuery = null;
    let lastAgent = null;
    let nextOffset = 0;
    const pageSize = 5;

    const sendQuery = async (queryText, opts = {}) => {
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

            const useAds = opts.advertising === true;
            const endpoint = useAds ? API_URL_ADS : API_URL;

            const payload = useAds
                ? { message: queryText, language: lang }
                : {
                    question: queryText,
                    language: lang,
                    limit: opts.limit ?? pageSize,
                    offset: opts.offset ?? 0,
                };

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const data = await response.json();

            // Normalizar respuesta para el bot de anuncios
            const normalized = opts.advertising
                ? {
                    respuesta: data.message || data.respuesta,
                    json: [],
                    tips: [],
                    guias: [],
                    articulos: [],
                }
                : data;

            // Guardar estado para "Mostrar más" solo en el bot principal
            if (!opts.advertising) {
                lastQuery = queryText;
                lastAgent = data.agente;
                nextOffset = data.next_offset ?? 0;
            }

            updateBotMessage(thinkingMessage, normalized);

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

        // --- NUEVO: Mostrar consejos rápidos ---
        if (data.tips && data.tips.length > 0) {
            const tipsContainer = document.createElement('div');
            tipsContainer.className = 'guias-container';
            tipsContainer.innerHTML = '<h4 class="guias-title">💡 Consejos rápidos</h4>' +
                `<ul style="list-style:disc;padding-left:20px">${data.tips.map(t => `<li>${t}</li>`).join('')}</ul>`;
            messageDiv.appendChild(tipsContainer);
        }

        // --- NUEVO: Mostrar guías de la revista ---
        if (data.guias && data.guias.length > 0) {
            const guiasContainer = document.createElement('div');
            guiasContainer.className = 'guias-container';
            guiasContainer.innerHTML = '<h4 class="guias-title">📖 Guías de la Revista</h4>';

            data.guias.forEach(guia => {
                const guiaCard = document.createElement('div');
                guiaCard.className = 'guia-card';
                guiaCard.innerHTML = `
                    <div class="guia-icon">📚</div>
                    <div class="guia-content">
                        <h5>${guia.titulo}</h5>
                        <p>${guia.resumen}</p>
                        <a href="${guia.url}" class="guia-link" target="_blank">Leer guía completa →</a>
                    </div>
                `;
                guiasContainer.appendChild(guiaCard);
            });

            messageDiv.appendChild(guiasContainer);
        }

        // --- NUEVO: Mostrar artículos de la revista (RSS) ---
        if (data.articulos && data.articulos.length > 0) {
            const articulosContainer = document.createElement('div');
            articulosContainer.className = 'guias-container';
            articulosContainer.innerHTML = '<h4 class="guias-title">✨ Artículos de Barcelona Metropolitan</h4>';

            data.articulos.forEach(articulo => {
                const articuloCard = document.createElement('div');
                articuloCard.className = 'guia-card';
                articuloCard.innerHTML = `
                    <div class="guia-icon">📰</div>
                    <div class="guia-content">
                        <h5>${articulo.title || 'Sin título'}</h5>
                        <p>${articulo.description || 'Sin descripción'}</p>
                        ${articulo.url ? `<a href="${articulo.url}" class="guia-link" target="_blank">Leer artículo →</a>` : ''}
                    </div>
                `;
                articulosContainer.appendChild(articuloCard);
            });

            messageDiv.appendChild(articulosContainer);
        }

        // Resultados en formato de tarjeta
        if (Array.isArray(data.json) && data.json.length > 0) {
            const resultsContainer = document.createElement('div');
            resultsContainer.className = 'results-container';
            data.json.forEach(item => {
                const card = document.createElement('div');
                card.className = 'result-card';

                // Marcar anunciantes con badge
                if (item.es_anunciante) {
                    card.classList.add('anunciante-destacado');
                }

                // Estructura mejorada para más control con CSS
                let cardHTML = '';

                // Badge para anunciantes
                if (item.es_anunciante) {
                    cardHTML += '<span class="badge-anunciante">⭐ Anunciante</span>';
                }

                cardHTML += `<h3>${item.nombre}</h3><p class="card-description">${item.descripcion}</p>`;

                // Contenedor para los detalles (contacto, precio, etc.)
                const details = `
                    ${item.contacto ? `<p><strong>Contacto:</strong> ${item.contacto}</p>` : ''}
                    ${item.precio ? `<p><strong>Precio:</strong> ${item.precio}</p>` : ''}
                    ${item.ubicacion ? `<p><strong>Ubicación:</strong> ${item.ubicacion}</p>` : ''}
                `;
                if (details.trim()) {
                    cardHTML += `<div class="card-details">${details}</div>`;
                }

                // CTA a ficha del directorio si existe URL
                if (item.url) {
                    cardHTML += `<p><a href="${item.url}" target="_blank" rel="noopener" class="guia-link">Ver ficha en el directorio →</a></p>`;
                }

                if (item.beneficios && item.beneficios.length > 0) {
                    cardHTML += `<div class="card-benefits"><strong>Beneficios:</strong><ul>${item.beneficios.map(b => `<li>${b}</li>`).join('')}</ul></div>`;
                }

                // --- INICIO: Añadir sección de FAQ desplegable ---
                if (item.faq && item.faq.length > 0) {
                    cardHTML += `
                        <div class="faq-container">
                            <button class="faq-toggle">
                                Preguntas Frecuentes
                                <i class="fas fa-chevron-down"></i>
                            </button>
                            <div class="faq-content">
                                <ul>
                                    ${item.faq.map(f => `<li><strong>${f.q}</strong><p>${f.a}</p></li>`).join('')}
                                </ul>
                            </div>
                        </div>`;
                }
                // --- FIN: Añadir sección de FAQ desplegable ---

                card.innerHTML = cardHTML;
                resultsContainer.appendChild(card);
            });
            messageDiv.appendChild(resultsContainer);

            // Botón "Mostrar más"
            if (data.has_more) {
                const moreBtn = document.createElement('button');
                moreBtn.className = 'show-more-btn';
                moreBtn.textContent = 'Mostrar más resultados';
                moreBtn.addEventListener('click', async () => {
                    const loading = addMessage('...', 'bot');
                    try {
                        const lang = navigator.language.split('-')[0];
                        const resp = await fetch(API_URL, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                question: lastQuery,
                                language: lang,
                                limit: pageSize,
                                offset: nextOffset,
                            }),
                        });
                        const nextData = await resp.json();
                        // Actualizar offset para futuras cargas
                        nextOffset = nextData.next_offset ?? 0;
                        updateBotMessage(loading, nextData);
                    } catch (e) {
                        updateBotMessage(loading, { respuesta: 'No pude cargar más resultados.', json: [] });
                    }
                });
                messageDiv.appendChild(moreBtn);
            }

            // Añadir event listener para los acordeones de FAQ y tracking de CTA usando delegación de eventos
            resultsContainer.addEventListener('click', (e) => {
                handleFaqToggle(e);
                const link = e.target.closest('a.guia-link');
                if (link) {
                    try {
                        fetch('/api/analytics', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                event: 'directory_click',
                                data: { url: link.href, text: link.textContent },
                                timestamp: new Date().toISOString()
                            })
                        }).catch(()=>{});
                    } catch (err) {}
                }
            });

        } else if (!data.respuesta) {
            // Si no hay resultados ni texto amigable, mostrar un mensaje genérico
            const textResponse = document.createElement('p');
            textResponse.textContent = "No he encontrado información sobre eso, ¿puedes ser más específico?";
            messageDiv.appendChild(textResponse);
        }

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    const handleFaqToggle = (e) => {
        const faqToggle = e.target.closest('.faq-toggle');
        if (!faqToggle) return;

        const faqContent = faqToggle.nextElementSibling;
        const icon = faqToggle.querySelector('i');

        faqToggle.classList.toggle('active');
        icon.classList.toggle('fa-chevron-up');
        icon.classList.toggle('fa-chevron-down');
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
            { text: '📢 Anúnciate', query: 'Quiero anunciarme', advertising: true }
        ];

        actions.forEach(action => {
            const button = document.createElement('button');
            button.className = 'quick-action-btn';
            button.textContent = action.text;
            button.onclick = () => {
                sendQuery(action.query, { advertising: action.advertising === true });
            };
            actionsContainer.appendChild(button);
        });

        messageDiv.appendChild(actionsContainer);
    };
    // --- Lógica del Carrusel ---
    if (carousel) {
        prevBtn?.addEventListener('click', () => {
            carousel.scrollBy({ left: -350, behavior: 'smooth' });
        });
        nextBtn?.addEventListener('click', () => {
            carousel.scrollBy({ left: 350, behavior: 'smooth' });
        });
    }

    // --- Event Listeners ---

    // Botones de enviar
    sendBtn?.addEventListener('click', handleSendMessage);
    sendBtnWidget.addEventListener('click', handleSendMessage);

    // Enviar con la tecla Enter
    [chatInput, chatInputWidget].forEach(input => input?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    }));

    // Menú hamburguesa
    hamburger.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    closeSidebar.addEventListener('click', () => {
        sidebar.classList.remove('open');
    });

    // Cerrar sidebar al hacer clic en un link
    sidebar.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            sidebar.classList.remove('open');
        });
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
            const serviceName = card.dataset.service;
            toggleChatWindow(true);
            sendQuery(serviceName);
        });
    });

    // Botones de guías
    guideButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const guide = btn.dataset.guide;
            toggleChatWindow(true);
            sendQuery(`Información sobre ${guide}`);
        });
    });

    // Botones de anunciantes
    advertiserButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const advertiserName = btn.dataset.name;
            toggleChatWindow(true);
            sendQuery(`Información sobre ${advertiserName}`);
            e.stopPropagation();
        });
    });

    // Mensaje de bienvenida
    setTimeout(() => {
        addWelcomeMessageWithActions();
    }, 500);

});
