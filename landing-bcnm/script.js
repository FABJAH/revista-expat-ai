// Configuracion
const API_URL = 'http://127.0.0.1:8000/consulta';

// Estado de la aplicacion
let currentLanguage = 'es';
let currentService = null; // Guardar el servicio actual para respuestas

// Elementos DOM - se inicializaran despues de que el DOM este listo
let serviceCards, serviceLinks, langButtons, chatInput, sendButton, chatMessages, quickButtons, globalSearchInput;

// Inicializacion
document.addEventListener('DOMContentLoaded', function() {
    // Elementos DOM - inicializar cuando el DOM este listo
    serviceCards = document.querySelectorAll('.service-card');
    serviceLinks = document.querySelectorAll('[data-service]');
    langButtons = document.querySelectorAll('.lang-btn');
    chatInput = document.getElementById('chat-input');
    sendButton = document.getElementById('send-btn');
    chatMessages = document.getElementById('chat-messages');
    quickButtons = document.querySelectorAll('.quick-btn');
    globalSearchInput = document.getElementById('global-search');

    initEventListeners();
    console.log('✅ BCN Metropolitan Landing Page cargada');
});

// Configurar event listeners
function initEventListeners() {
    // Servicios - Cards
    if (serviceCards) {
        serviceCards.forEach(card => {
            card.addEventListener('click', function() {
                const service = this.getAttribute('data-service');
                openServiceChat(service);
            });
        });
    }

    // Servicios - Links
    if (serviceLinks) {
        serviceLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const service = this.getAttribute('data-service');
                openServiceChat(service);
            });
        });
    }

    // Cambio de idioma
    if (langButtons) {
        langButtons.forEach(button => {
            button.addEventListener('click', function() {
                const lang = this.getAttribute('data-lang');
                switchLanguage(lang);
            });
        });
    }

    // Chat
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Botones rapidos
    if (quickButtons) {
        quickButtons.forEach(button => {
            button.addEventListener('click', function() {
                const question = this.getAttribute('data-question');
                if (chatInput) {
                    chatInput.value = question;
                    sendMessage();
                }
            });
        });
    }

    // Busqueda global
    if (globalSearchInput) {
        globalSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchGlobal();
            }
        });
    }
}

// Cambiar idioma
function switchLanguage(lang) {
    currentLanguage = lang;

    // Actualizar botones de idioma
    if (langButtons) {
        langButtons.forEach(button => {
            if (button.getAttribute('data-lang') === lang) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
    }

    console.log('Idioma cambiado a: ' + lang);
}

// Abrir chat con servicio especifico
function openServiceChat(service) {
    let message = '';

    // Mapeo de servicios a preguntas
    const serviceQuestions = {
        "Accommodation": "Busco alojamiento en Barcelona",
        "Arts and Culture": "Informacion sobre arte y cultura en Barcelona",
        "Bars and Clubs": "Bares y vida nocturna en Barcelona",
        "Beauty and Well-Being": "Servicios de belleza y bienestar",
        "Business Services": "Servicios para negocios en Barcelona",
        "Education": "Opciones de educacion en Barcelona",
        "Healthcare": "Servicios de salud y medicos",
        "Home Services": "Servicios para el hogar",
        "Legal and Financial": "Asesoria legal y financiera para expatriados",
        "Recreation and Leisure": "Actividades de ocio y recreacion",
        "Restaurants": "Recomendaciones de restaurantes en Barcelona",
        "Retail": "Compras y tiendas en Barcelona"
    };

    message = serviceQuestions[service] || "Informacion sobre " + service;

    if (chatInput) {
        chatInput.value = message;
        sendMessage();
    }

    // Scroll al chat
    const chatSection = document.querySelector('.chat-section');
    if (chatSection) {
        chatSection.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

// Busqueda global
function searchGlobal() {
    if (!globalSearchInput) return;

    const query = globalSearchInput.value.trim();
    if (!query) return;

    if (chatInput) {
        chatInput.value = query;
        sendMessage();
    }
    globalSearchInput.value = '';

    // Scroll al chat
    const chatSection = document.querySelector('.chat-section');
    if (chatSection) {
        chatSection.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

// Enviar mensaje al backend
async function sendMessage() {
    if (!chatInput) return;

    const question = chatInput.value.trim();

    if (!question) {
        showError('Por favor, escribe una pregunta');
        return;
    }

    // Aniadir mensaje del usuario al chat
    addMessageToChat(question, 'user-message');
    chatInput.value = '';

    try {
        // Mostrar indicador de carga
        const loadingId = showLoadingMessage();

        // Llamar a la API
        console.log('Enviando peticion a: ' + API_URL);
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pregunta: question,
                language: currentLanguage
            })
        });

        console.log('Response status: ' + response.status);

        if (!response.ok) {
            throw new Error('Error HTTP! estado: ' + response.status);
        }

        const data = await response.json();

        // Remover mensaje de carga
        removeLoadingMessage(loadingId);

        // Mostrar respuesta formateada
        if (data.json && data.json.opciones && data.json.opciones.length > 0) {
            // Respuesta con opciones
            let responseHtml = '<div style="margin-bottom:12px;"><strong>Agente:</strong> ' + data.agente + ' | <strong>Confianza:</strong> ' + Math.round(data.confidence * 100) + '%</div>';
            responseHtml += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;">';

            for (const opt of data.json.opciones) {
                responseHtml += '<div style="border:1px solid #ddd;padding:12px;border-radius:8px;background:white;box-shadow:0 2px 4px rgba(0,0,0,0.05)">';
                responseHtml += '<div style="font-weight:600;color:#2563eb;margin-bottom:4px">' + opt.nombre + '</div>';
                responseHtml += '<div style="font-size:0.9rem;color:#555;margin-bottom:8px">' + (opt.descripcion || '') + '</div>';
                responseHtml += '<div style="font-size:0.85rem;">Contacto: ' + (opt.contacto || 'N/A') + '</div>';

                if (opt.faq && opt.faq.length > 0) {
                    responseHtml += '<div style="margin-top:8px;border-top:1px solid #eee;padding-top:8px;"><em>FAQ:</em>';
                    for (const q of opt.faq) {
                        responseHtml += '<div style="margin-top:4px;font-size:0.85rem;"><strong>Q:</strong> ' + q.q + '<br/><strong>A:</strong> ' + q.a + '</div>';
                    }
                    responseHtml += '</div>';
                }

                responseHtml += '</div>';
            }
            responseHtml += '</div>';

            addMessageToChat(responseHtml, 'bot-message', true);
        } else {
            // Respuesta de texto plano
            addMessageToChat(data.respuesta || 'Respuesta recibida', 'bot-message');
        }

        console.log('Respuesta recibida. Agente: ' + data.agente + ', Confidence: ' + data.confidence);

    } catch (error) {
        console.error('Error: ' + error);
        removeLoadingMessage();

        const errorMessage = 'Lo siento, hubo un error al conectar con el servidor. Por favor, intenta de nuevo.';
        addMessageToChat(errorMessage, 'bot-message');
    }
}

// Aniadir mensaje al chat
function addMessageToChat(message, className, isHtml) {
    if (!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + className;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    if (isHtml) {
        messageContent.innerHTML = message;
    } else {
        // Formatear mensajes multilinea
        const formattedMessage = message.replace(/\n/g, '<br>');
        messageContent.innerHTML = formattedMessage;
    }

    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);

    // Scroll al final
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv;
}

// Mostrar mensaje de carga
function showLoadingMessage() {
    if (!chatMessages) return null;

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.id = 'loading-message';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = 'Pensando...';

    loadingDiv.appendChild(messageContent);
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return 'loading-message';
}

// Remover mensaje de carga
function removeLoadingMessage(id) {
    if (!id) id = 'loading-message';
    const loadingMessage = document.getElementById(id);
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Mostrar error
function showError(message) {
    if (!chatMessages) return;

    const errorDiv = document.createElement('div');
    errorDiv.className = 'message bot-message';
    errorDiv.style.backgroundColor = '#e74c3c';
    errorDiv.style.color = 'white';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;

    errorDiv.appendChild(messageContent);
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Auto-remover despues de 5 segundos
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Smooth scroll para enlaces de navegacion
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Mostrar respuestas de servicios en la sección de respuestas
function showServiceResponses(data) {
    const responseSection = document.getElementById('service-responses');
    const responsesContent = document.getElementById('service-responses-content');

    if (!responseSection || !responsesContent) return;

    // Limpiar contenido anterior
    responsesContent.innerHTML = '';

    // Crear título con agente y confianza
    const header = document.createElement('div');
    header.style.cssText = 'grid-column: 1 / -1; margin-bottom: 1rem; padding: 1rem; background: white; border-radius: 8px; border-left: 4px solid #3498db;';
    header.innerHTML = '<h3 style="margin: 0 0 0.5rem 0; color: #2c3e50;">' + data.agente + '</h3>' +
                      '<p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">Confianza: ' + Math.round(data.confidence * 100) + '%</p>';
    responsesContent.appendChild(header);

    // Crear tarjetas de opciones
    if (data.json && data.json.opciones && data.json.opciones.length > 0) {
        for (const opt of data.json.opciones) {
            const card = document.createElement('div');
            card.className = 'response-card';

            let cardHTML = '<h3>' + (opt.nombre || 'Opción') + '</h3>';

            if (opt.descripcion) {
                cardHTML += '<p><strong>Descripción:</strong> ' + opt.descripcion + '</p>';
            }

            if (opt.contacto) {
                cardHTML += '<p><strong>Contacto:</strong> ' + opt.contacto + '</p>';
            }

            if (opt.faq && opt.faq.length > 0) {
                cardHTML += '<div style="margin-top: 1rem; border-top: 1px solid #eee; padding-top: 1rem;"><strong>Preguntas Frecuentes:</strong>';
                for (const q of opt.faq) {
                    cardHTML += '<div style="margin-top: 0.5rem; font-size: 0.9rem;"><em>P: ' + q.q + '</em><br/>R: ' + q.a + '</div>';
                }
                cardHTML += '</div>';
            }

            card.innerHTML = cardHTML;
            responsesContent.appendChild(card);
        }
    }

    // Mostrar la sección
    responseSection.style.display = 'block';
}
