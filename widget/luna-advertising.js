/**
 * Widget de Ventas Dinámico - Luna (Mascota 🦉)
 *
 * Características:
 * - Avatar animado de búho curioso
 * - Burbujas de diálogo que se abren proactivamente
 * - Bilingual (ES/EN)
 * - Responde y captura leads
 * - Integración con bot_advertising_sales.py
 */

class LunaAdvertisingWidget {
  constructor(config = {}) {
    this.config = {
      position: config.position || 'bottom-right',
      language: config.language || 'es',
      autoOpen: config.autoOpen !== false,
      autoOpenDelay: config.autoOpenDelay || 3000,
      ...config
    };

    this.isOpen = false;
    this.messageQueue = [];
    this.conversationHistory = [];
    this.init();
  }

  init() {
    this.createWidgetHTML();
    this.attachEventListeners();
    this.setupProactiveMessages();
    console.log('🦉 Luna Advertising Widget inicializado');
  }

  // ===================================================================
  // HTML STRUCTURE
  // ===================================================================

  createWidgetHTML() {
    // Widget container
    const container = document.createElement('div');
    container.id = 'luna-widget-container';
    container.className = `luna-widget ${this.config.position}`;
    container.innerHTML = `
      <!-- Bubble Button (Mascota) -->
      <div class="luna-bubble-button" id="lunaButton">
        <div class="luna-mascot">
          🦉
        </div>
        <span class="luna-label" data-label-es="¡Hola!" data-label-en="Hello!">
          ¡Hola!
        </span>
        <span class="luna-notification-badge" id="lunaBadge" style="display:none;">1</span>
      </div>

      <!-- Chat Window -->
      <div class="luna-chat-window" id="lunaChatWindow">
        <!-- Header -->
        <div class="luna-chat-header">
          <div class="luna-header-left">
            <div class="luna-mascot-large">🦉</div>
            <div class="luna-header-text">
              <h3 data-title-es="Luna" data-title-en="Luna">Luna</h3>
              <p data-subtitle-es="Experta en publicidad" data-subtitle-en="Advertising Expert">
                Experta en publicidad
              </p>
            </div>
          </div>
          <button class="luna-close-btn" id="lunaCloseBtn">×</button>
        </div>

        <!-- Messages Area -->
        <div class="luna-messages-container" id="lunaMessages">
          <!-- Messages appear here -->
        </div>

        <!-- Quick Replies -->
        <div class="luna-quick-replies" id="lunaQuickReplies">
          <!-- Quick reply buttons appear here -->
        </div>

        <!-- Input Area -->
        <div class="luna-input-area">
          <input
            type="text"
            id="lunaInput"
            class="luna-input"
            placeholder="Escribe tu pregunta..."
            data-placeholder-es="Escribe tu pregunta..."
            data-placeholder-en="Type your question..."
          />
          <button class="luna-send-btn" id="lunaSendBtn">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M17 10L3 2V7H8V13H3V18L17 10Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(container);
  }

  // ===================================================================
  // EVENT LISTENERS
  // ===================================================================

  attachEventListeners() {
    const button = document.getElementById('lunaButton');
    const closeBtn = document.getElementById('lunaCloseBtn');
    const sendBtn = document.getElementById('lunaSendBtn');
    const input = document.getElementById('lunaInput');

    button.addEventListener('click', () => this.toggleChat());
    closeBtn.addEventListener('click', () => this.closeChat());
    sendBtn.addEventListener('click', () => this.sendMessage());

    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Actualizar placeholder si cambia idioma
    input.addEventListener('change', () => this.updateLanguage());
  }

  // ===================================================================
  // CHAT INTERACTION
  // ===================================================================

  toggleChat() {
    if (this.isOpen) {
      this.closeChat();
    } else {
      this.openChat();
    }
  }

  openChat() {
    const window = document.getElementById('lunaChatWindow');
    const button = document.getElementById('lunaButton');

    window.classList.add('open');
    button.classList.add('open');
    this.isOpen = true;

    // Hide notification badge
    document.getElementById('lunaBadge').style.display = 'none';

    // Focus input
    setTimeout(() => {
      document.getElementById('lunaInput').focus();
    }, 300);

    // Log interaction
    this.logInteraction('chat_opened');
  }

  closeChat() {
    const window = document.getElementById('lunaChatWindow');
    const button = document.getElementById('lunaButton');

    window.classList.remove('open');
    button.classList.remove('open');
    this.isOpen = false;
  }

  addMessage(text, sender = 'luna', options = {}) {
    const container = document.getElementById('lunaMessages');
    const messageEl = document.createElement('div');
    messageEl.className = `luna-message luna-message-${sender}`;

    // Parse HTML if needed (for formatted responses)
    messageEl.innerHTML = `
      <div class="luna-message-content">
        ${sender === 'luna' ? '<div class="luna-mascot-small">🦉</div>' : ''}
        <div class="luna-message-text">${this.escapeHtml(text)}</div>
      </div>
    `;

    container.appendChild(messageEl);

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;

    // Add to history
    this.conversationHistory.push({
      sender,
      text,
      timestamp: new Date().toISOString()
    });
  }

  async sendMessage() {
    const input = document.getElementById('lunaInput');
    const text = input.value.trim();

    if (!text) return;

    // Add user message
    this.addMessage(text, 'user');
    input.value = '';

    // Show typing indicator
    this.showTypingIndicator();

    try {
      // Get response from backend
      const response = await this.getResponse(text);

      // Remove typing indicator
      this.removeTypingIndicator();

      // Add Luna's response
      this.displayResponse(response);

    } catch (error) {
      this.removeTypingIndicator();
      console.error('Error getting response:', error);

      const fallback = this.config.language === 'es'
        ? 'Disculpa, hay un error. Intenta de nuevo.'
        : 'Sorry, there was an error. Please try again.';

      this.addMessage(fallback, 'luna');
    }

    this.logInteraction('message_sent');
  }

  async getResponse(message) {
    /**
     * Llamar a backend para obtener respuesta
     *
     * POST /api/bot/advertising
     * {
     *   "message": string,
     *   "language": "es" | "en",
     *   "conversation_id": string (opcional)
     * }
     */

    const response = await fetch('/api/bot/advertising', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        language: this.config.language,
        conversation_id: this.getConversationId()
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  displayResponse(responseData) {
    const { type, message, quick_replies, next, plans, testimonials } = responseData;

    // Mensaje principal
    if (message) {
      this.addMessage(message, 'luna');
    }

    // Mostrar comparativa de planes si existe
    if (plans) {
      this.displayPlans(plans);
    }

    // Mostrar testimonios si existen
    if (testimonials) {
      this.displayTestimonials(testimonials);
    }

    // Mostrar quick replies si existen
    if (quick_replies) {
      this.displayQuickReplies(quick_replies);
    }

    // Mostrar siguiente paso si existe
    if (next) {
      setTimeout(() => this.displayResponse(next), 800);
    }
  }

  displayPlans(plans) {
    const container = document.getElementById('lunaMessages');
    const plansEl = document.createElement('div');
    plansEl.className = 'luna-plans-grid';

    plansEl.innerHTML = plans.map(plan => `
      <div class="luna-plan-card">
        <div class="luna-plan-name">${plan.nombre}</div>
        <div class="luna-plan-price">${plan.precio}</div>
        <div class="luna-plan-duration">${plan.duracion}</div>
        <div class="luna-plan-benefits">
          ${plan.beneficios.map(b => `<div class="luna-benefit">${b}</div>`).join('')}
        </div>
        <button class="luna-plan-btn" onclick="window.lunaWidget.selectPlan('${plan.id}')">
          ${plan.cta_text}
        </button>
      </div>
    `).join('');

    container.appendChild(plansEl);
    container.scrollTop = container.scrollHeight;
  }

  displayTestimonials(testimonials) {
    const container = document.getElementById('lunaMessages');
    const testEl = document.createElement('div');
    testEl.className = 'luna-testimonials';

    testEl.innerHTML = testimonials.map(t => `
      <div class="luna-testimonial-card">
        <div class="luna-testimonial-rating">${t.emoji}</div>
        <div class="luna-testimonial-text">"${t.testimonial}"</div>
        <div class="luna-testimonial-author">
          <strong>${t.nombre}</strong>
          <small>${t.negocio}</small>
        </div>
      </div>
    `).join('');

    container.appendChild(testEl);
    container.scrollTop = container.scrollHeight;
  }

  displayQuickReplies(replies) {
    const container = document.getElementById('lunaQuickReplies');
    container.innerHTML = '';

    replies.forEach(reply => {
      const btn = document.createElement('button');
      btn.className = 'luna-quick-reply';
      btn.textContent = reply.text;
      btn.onclick = () => this.handleQuickReply(reply);
      container.appendChild(btn);
    });
  }

  handleQuickReply(reply) {
    const input = document.getElementById('lunaInput');

    if (reply.action === 'show_plans') {
      input.value = this.config.language === 'es' ? 'Mostrar planes' : 'Show plans';
    } else if (reply.action === 'help') {
      input.value = this.config.language === 'es' ? '¿Cómo puedo anunciar?' : 'How can I advertise?';
    } else if (reply.action === 'business') {
      input.value = reply.text;
    }

    this.sendMessage();
  }

  selectPlan(planId) {
    this.logInteraction(`plan_selected:${planId}`);
    const input = document.getElementById('lunaInput');
    input.value = this.config.language === 'es'
      ? `Quiero el plan ${planId}`
      : `I want the ${planId} plan`;
    this.sendMessage();
  }

  // ===================================================================
  // PROACTIVE MESSAGES (Burbujas que se abren)
  // ===================================================================

  setupProactiveMessages() {
    if (!this.config.autoOpen) return;

    // Esperar un poco antes de mostrar el primer mensaje
    setTimeout(() => {
      this.showProactiveMessage();
    }, this.config.autoOpenDelay);

    // Mostrar nuevos mensajes cada cierto tiempo (si la ventana está cerrada)
    setInterval(() => {
      if (!this.isOpen) {
        this.showProactiveNotification();
      }
    }, 30000); // Cada 30 segundos
  }

  showProactiveMessage() {
    const messages = {
      'es': [
        '¡Hola! 👋 ¿Es tu primer día en Barcelona? Tengo recursos que necesitas.',
        '¿Eres una empresa? 💼 Nos encantaría que te unas a nuestro directorio.',
        '😊 Mira cómo otros negocios han crecido con nosotros...',
      ],
      'en': [
        'Hello! 👋 Is this your first day in Barcelona? I have resources you need.',
        'Are you a business? 💼 We\'d love to have you in our directory.',
        'See how other businesses have grown with us... 😊',
      ]
    };

    const langMessages = messages[this.config.language] || messages['es'];
    const randomMessage = langMessages[Math.floor(Math.random() * langMessages.length)];

    this.openChat();
    this.addMessage(randomMessage, 'luna');
  }

  showProactiveNotification() {
    const badge = document.getElementById('lunaBadge');
    badge.style.display = 'flex';
    badge.textContent = '1';

    // Animate
    this.animateBounce();
  }

  animateBounce() {
    const button = document.getElementById('lunaButton');
    button.classList.add('bounce');
    setTimeout(() => button.classList.remove('bounce'), 600);
  }

  showTypingIndicator() {
    const container = document.getElementById('lunaMessages');
    const typingEl = document.createElement('div');
    typingEl.className = 'luna-message luna-message-luna luna-typing';
    typingEl.id = 'lunaTyping';
    typingEl.innerHTML = `
      <div class="luna-message-content">
        <div class="luna-mascot-small">🦉</div>
        <div class="luna-typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
    `;
    container.appendChild(typingEl);
    container.scrollTop = container.scrollHeight;
  }

  removeTypingIndicator() {
    const typing = document.getElementById('lunaTyping');
    if (typing) typing.remove();
  }

  // ===================================================================
  // UTILITIES
  // ===================================================================

  getConversationId() {
    if (!window.lunaConversationId) {
      window.lunaConversationId = `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    return window.lunaConversationId;
  }

  logInteraction(action) {
    console.log(`[Luna Analytics] ${action}`, {
      timestamp: new Date().toISOString(),
      conversationId: this.getConversationId(),
      language: this.config.language
    });

    // TODO: Enviar a analytics backend
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  updateLanguage() {
    // Actualizar placeholders, labels, etc. según idioma
    const input = document.getElementById('lunaInput');
    const placeholder = input.getAttribute(`data-placeholder-${this.config.language}`);
    if (placeholder) input.placeholder = placeholder;
  }
}

// ===================================================================
// INICIALIZACIÓN GLOBAL
// ===================================================================

// Inicializar cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
  // Detectar idioma del navegador
  const browserLang = navigator.language.startsWith('es') ? 'es' : 'en';

  window.lunaWidget = new LunaAdvertisingWidget({
    language: window.lunaLanguage || browserLang,
    autoOpen: true,
    autoOpenDelay: 2500,
    position: 'bottom-right'
  });
});
