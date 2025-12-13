/**
 * Script de integración para Barcelona Metropolitan
 * Este script se carga en el sitio de Barcelona Metropolitan
 * y automáticamente inicializa el widget del asistente
 */

(function() {
  'use strict';

  // Configuración por defecto
  const defaultConfig = {
    apiUrl: 'https://api.barcelona-expats.com', // Cambiar a tu dominio en producción
    position: 'bottom-right',
    primaryColor: '#0066cc',
    greeting: '¡Hola! ¿En qué puedo ayudarte?',
    placeholder: 'Escribe tu pregunta...',
    suggestions: [
      '¿Cómo obtener el NIE?',
      'Busco dentista en Barcelona',
      'Quiero aprender español',
      'Colegios internacionales'
    ]
  };

  // Obtener configuración personalizada si existe
  const userConfig = window.ExpatAssistantConfig || {};
  const config = { ...defaultConfig, ...userConfig };

  // Función para cargar un script de forma asíncrona
  function loadScript(src, callback) {
    const script = document.createElement('script');
    script.src = src;
    script.async = true;
    script.onload = callback;
    script.onerror = function() {
      console.error('Failed to load Expat Assistant script:', src);
    };
    document.head.appendChild(script);
  }

  // Función para cargar CSS
  function loadCSS(href) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    link.onerror = function() {
      console.error('Failed to load Expat Assistant styles:', href);
    };
    document.head.appendChild(link);
  }

  // Función de inicialización
  function initWidget() {
    // Cargar estilos
    loadCSS(config.apiUrl + '/widget/widget.css');

    // Cargar script principal
    loadScript(config.apiUrl + '/widget/widget.js', function() {
      // Una vez cargado el script, inicializar el widget
      if (typeof ExpatAssistantWidget !== 'undefined') {
        window.ExpatAssistant = new ExpatAssistantWidget(config);
        console.log('✅ Expat Assistant widget initialized successfully');
      } else {
        console.error('ExpatAssistantWidget not found after loading script');
      }
    });
  }

  // Inicializar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWidget);
  } else {
    // El DOM ya está listo
    initWidget();
  }
})();
