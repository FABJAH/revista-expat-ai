/**
 * Barcelona Metropolitan - Expat Assistant Widget
 * Widget flotante profesional para integración en sitio web
 * @version 1.0.0
 */

class ExpatAssistantWidget {
  constructor(config = {}) {
    this.config = {
      apiUrl: config.apiUrl || 'http://localhost:8000',
      position: config.position || 'bottom-right',
      primaryColor: config.primaryColor || '#0066cc',
      greeting: config.greeting || '¡Hola! ¿En qué puedo ayudarte?',
      placeholder: config.placeholder || 'Escribe tu pregunta...',
      suggestions: config.suggestions || [
        '¿Cómo obtener el NIE?',
        'Busco dentista en Barcelona',
        'Quiero aprender español',
        'Colegios internacionales'
      ],
      ...config
    };

    this.isOpen = false;
    this.messages = [];
    this.sessionId = this.generateSessionId();

    this.init();
  }

  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  init() {
    this.injectStyles();
    this.createWidget();
    this.attachEventListeners();
    this.addWelcomeMessage();
  }

  injectStyles() {
    // Los estilos ya están cargados desde widget.css
    // Aquí podríamos inyectar custom properties
    const root = document.documentElement;
    root.style.setProperty('--primary-color', this.config.primaryColor);
  }

  createWidget() {
    const container = document.createElement('div');
    container.className = 'expat-assistant-widget';
    container.innerHTML = `
      <!-- Botón flotante -->
      <button class="expat-assistant-button" aria-label="Abrir asistente" title="Expat Assistant">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      </button>

      <!-- Ventana de chat -->
      <div class="expat-assistant-window">
        <!-- Header -->
        <div class="expat-assistant-header">
          <div class="expat-assistant-header-content">
            <div class="expat-assistant-header-icon">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div class="expat-assistant-header-text">
              <h3>Expat Assistant</h3>
              <p>Siempre disponible para ayudarte</p>
            </div>
          </div>
          <button class="expat-assistant-close" aria-label="Cerrar" title="Cerrar">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Quick actions -->
        <div class="expat-quick-actions">
          ${this.config.suggestions.map(s => `
            <button class="expat-quick-action" data-query="${s}">${s}</button>
          `).join('')}
        </div>

        <!-- Messages -->
        <div class="expat-assistant-messages" id="expat-messages">
          <div class="expat-welcome">
            <div class="expat-welcome-icon">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
            </div>
            <div>
              <h4>¡Bienvenido!</h4>
              <p>Soy tu asistente virtual. Puedo ayudarte con información sobre vivienda, salud, educación, trámites y más en Barcelona.</p>
            </div>
            <div class="expat-welcome-suggestions">
              ${this.config.suggestions.slice(0, 3).map(s => `
                <button class="expat-welcome-suggestion" data-query="${s}">💡 ${s}</button>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="expat-assistant-input">
          <input
            type="text"
            placeholder="${this.config.placeholder}"
            id="expat-input"
            aria-label="Escribe tu pregunta"
            autocomplete="off"
          />
          <button id="expat-send-btn" aria-label="Enviar" title="Enviar">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>

        <!-- Powered by -->
        <div class="expat-powered-by">
          Powered by <a href="https://www.barcelona-metropolitan.com" target="_blank">Barcelona Metropolitan</a>
        </div>
      </div>
    `;

    document.body.appendChild(container);

    // Referencias a elementos
    this.elements = {
      button: container.querySelector('.expat-assistant-button'),
      window: container.querySelector('.expat-assistant-window'),
      closeBtn: container.querySelector('.expat-assistant-close'),
      messagesContainer: container.querySelector('#expat-messages'),
      input: container.querySelector('#expat-input'),
      sendBtn: container.querySelector('#expat-send-btn')
    };
  }

  attachEventListeners() {
    // Abrir/cerrar widget
    this.elements.button.addEventListener('click', () => this.toggle());
    this.elements.closeBtn.addEventListener('click', () => this.close());

    // Enviar mensaje
    this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
    this.elements.input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });

    // Quick actions
    document.querySelectorAll('.expat-quick-action, .expat-welcome-suggestion').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const query = e.target.dataset.query;
        this.elements.input.value = query;
        this.sendMessage();
      });
    });

    // Cerrar con ESC
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) this.close();
    });
  }

  toggle() {
    this.isOpen ? this.close() : this.open();
  }

  open() {
    this.isOpen = true;
    this.elements.window.classList.add('active');
    this.elements.input.focus();
    this.trackEvent('widget_opened');
  }

  close() {
    this.isOpen = false;
    this.elements.window.classList.remove('active');
    this.trackEvent('widget_closed');
  }

  addWelcomeMessage() {
    // El mensaje de bienvenida está en el HTML estático
  }

  async sendMessage() {
    const message = this.elements.input.value.trim();
    if (!message) return;

    // Limpiar input
    this.elements.input.value = '';

    // Agregar mensaje del usuario
    this.addMessage(message, 'user');

    // Mostrar indicador de escritura
    this.showTyping();

    try {
      const startTime = Date.now();

      // Llamar a la API
      const response = await fetch(`${this.config.apiUrl}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          pregunta: message,
          session_id: this.sessionId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      const responseTime = Date.now() - startTime;

      // Ocultar indicador de escritura
      this.hideTyping();

      // Agregar respuesta del bot
      this.addMessage(data.respuesta, 'bot');

      // Agregar guías si existen
      if (data.guias && data.guias.length > 0) {
        this.addGuides(data.guias);
      }

      // Agregar anunciantes si existen en JSON
      if (data.json && data.json.length > 0) {
        this.addAdvertisers(data.json);
      }

      // Track analytics
      this.trackEvent('query_sent', {
        query: message,
        category: data.categoria || 'general',
        response_time: responseTime,
        guides_count: data.guias?.length || 0,
        advertisers_count: data.json?.length || 0
      });

    } catch (error) {
      console.error('Error sending message:', error);
      this.hideTyping();
      this.showError('Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.');
      this.trackEvent('query_error', { error: error.message });
    }
  }

  addMessage(text, sender = 'bot') {
    const isUser = sender === 'user';
    const time = new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });

    // Remover pantalla de bienvenida si existe
    const welcome = this.elements.messagesContainer.querySelector('.expat-welcome');
    if (welcome) welcome.remove();

    const messageEl = document.createElement('div');
    messageEl.className = `expat-message ${isUser ? 'user' : 'bot'}`;
    messageEl.innerHTML = `
      <div class="expat-message-avatar">${isUser ? 'TÚ' : 'AI'}</div>
      <div class="expat-message-content">
        <div class="expat-message-bubble">${this.formatText(text)}</div>
        <div class="expat-message-time">${time}</div>
      </div>
    `;

    this.elements.messagesContainer.appendChild(messageEl);
    this.scrollToBottom();
  }

  addGuides(guides) {
    guides.forEach(guide => {
      const cardEl = document.createElement('div');
      cardEl.className = 'expat-message bot';
      cardEl.innerHTML = `
        <div class="expat-message-avatar">📖</div>
        <div class="expat-message-content">
          <div class="expat-card">
            <div class="expat-card-header">
              <div class="expat-card-title">${guide.titulo}</div>
              <span class="expat-card-badge guia">GUÍA</span>
            </div>
            <div class="expat-card-description">${guide.resumen}</div>
            <div class="expat-card-footer">
              <span class="expat-card-tag">📂 ${guide.categoria}</span>
            </div>
          </div>
        </div>
      `;

      // Click para mostrar más info
      cardEl.querySelector('.expat-card').addEventListener('click', () => {
        this.showGuideDetails(guide);
      });

      this.elements.messagesContainer.appendChild(cardEl);
    });

    this.scrollToBottom();
  }

  addAdvertisers(advertisers) {
    advertisers.forEach(advertiser => {
      const isSponsored = advertiser.es_anunciante === true;
      const cardEl = document.createElement('div');
      cardEl.className = 'expat-message bot';
      cardEl.innerHTML = `
        <div class="expat-message-avatar">${isSponsored ? '⭐' : '📍'}</div>
        <div class="expat-message-content">
          <div class="expat-card">
            <div class="expat-card-header">
              <div class="expat-card-title">${advertiser.nombre}</div>
              ${isSponsored ? '<span class="expat-card-badge anunciante">PATROCINADO</span>' : ''}
            </div>
            <div class="expat-card-description">${advertiser.descripcion}</div>
            <div class="expat-card-footer">
              ${advertiser.ubicacion ? `<span class="expat-card-tag">📍 ${advertiser.ubicacion}</span>` : ''}
              ${advertiser.precio ? `<span class="expat-card-tag">💰 ${advertiser.precio}</span>` : ''}
              ${advertiser.idiomas ? `<span class="expat-card-tag">🌐 ${advertiser.idiomas.join(', ')}</span>` : ''}
            </div>
          </div>
        </div>
      `;

      // Click para mostrar más info
      cardEl.querySelector('.expat-card').addEventListener('click', () => {
        this.showAdvertiserDetails(advertiser);
        this.trackEvent('advertiser_clicked', {
          advertiser_id: advertiser.nombre,
          is_sponsored: isSponsored
        });
      });

      this.elements.messagesContainer.appendChild(cardEl);
    });

    this.scrollToBottom();
  }

  showGuideDetails(guide) {
    const modal = `
      <div class="expat-modal-overlay" onclick="this.remove()">
        <div class="expat-modal" onclick="event.stopPropagation()">
          <div class="expat-modal-header">
            <h3>${guide.titulo}</h3>
            <button onclick="this.closest('.expat-modal-overlay').remove()">✕</button>
          </div>
          <div class="expat-modal-body">
            <p><strong>Categoría:</strong> ${guide.categoria}</p>
            <p>${guide.resumen}</p>
            ${guide.contenido ? `<div>${guide.contenido}</div>` : ''}
          </div>
        </div>
      </div>
    `;
    // Por ahora solo mostramos en consola
    console.log('Guide details:', guide);
    alert(`📖 ${guide.titulo}\n\n${guide.resumen}`);
  }

  showAdvertiserDetails(advertiser) {
    let details = `⭐ ${advertiser.nombre}\n\n`;
    details += `${advertiser.descripcion}\n\n`;

    if (advertiser.contacto) {
      details += `📞 Contacto:\n`;
      if (advertiser.contacto.telefono) details += `Tel: ${advertiser.contacto.telefono}\n`;
      if (advertiser.contacto.email) details += `Email: ${advertiser.contacto.email}\n`;
      if (advertiser.contacto.web) details += `Web: ${advertiser.contacto.web}\n`;
    }

    if (advertiser.ubicacion) {
      details += `\n📍 ${advertiser.ubicacion}`;
    }

    if (advertiser.precio) {
      details += `\n💰 ${advertiser.precio}`;
    }

    alert(details);
  }

  showTyping() {
    const typingEl = document.createElement('div');
    typingEl.className = 'expat-message bot';
    typingEl.id = 'expat-typing-indicator';
    typingEl.innerHTML = `
      <div class="expat-message-avatar">AI</div>
      <div class="expat-message-content">
        <div class="expat-message-bubble">
          <div class="expat-typing">
            <div class="expat-typing-dot"></div>
            <div class="expat-typing-dot"></div>
            <div class="expat-typing-dot"></div>
          </div>
        </div>
      </div>
    `;

    this.elements.messagesContainer.appendChild(typingEl);
    this.scrollToBottom();
  }

  hideTyping() {
    const typingEl = document.getElementById('expat-typing-indicator');
    if (typingEl) typingEl.remove();
  }

  showError(message) {
    const errorEl = document.createElement('div');
    errorEl.className = 'expat-message bot';
    errorEl.innerHTML = `
      <div class="expat-message-avatar">⚠️</div>
      <div class="expat-message-content">
        <div class="expat-error">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          ${message}
        </div>
      </div>
    `;

    this.elements.messagesContainer.appendChild(errorEl);
    this.scrollToBottom();
  }

  formatText(text) {
    // Convertir URLs a links
    text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');

    // Convertir saltos de línea a <br>
    text = text.replace(/\n/g, '<br>');

    return text;
  }

  scrollToBottom() {
    setTimeout(() => {
      this.elements.messagesContainer.scrollTop = this.elements.messagesContainer.scrollHeight;
    }, 100);
  }

  trackEvent(eventName, data = {}) {
    // Analytics tracking
    console.log('📊 Track event:', eventName, data);

    // Si hay Google Analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', eventName, {
        event_category: 'Expat Assistant',
        event_label: JSON.stringify(data),
        ...data
      });
    }

    // Si hay Meta Pixel
    if (typeof fbq !== 'undefined') {
      fbq('trackCustom', eventName, data);
    }

    // Enviar a nuestro propio backend
    fetch(`${this.config.apiUrl}/api/analytics`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: eventName,
        data: data,
        session_id: this.sessionId,
        timestamp: new Date().toISOString()
      })
    }).catch(err => console.warn('Analytics error:', err));
  }
}

// Auto-inicializar si hay configuración en window
if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', () => {
    const config = window.ExpatAssistantConfig || {};
    window.ExpatAssistant = new ExpatAssistantWidget(config);
  });
}

// Exportar para uso como módulo
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ExpatAssistantWidget;
}
