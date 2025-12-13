# Guía de Implementación - Barcelona Metropolitan

## 🎯 Resumen Ejecutivo

Este documento describe cómo integrar el **Expat Assistant Widget** en el sitio web de Barcelona Metropolitan (https://www.barcelona-metropolitan.com/).

**Tiempo estimado de integración:** 15 minutos
**Complejidad técnica:** Baja (solo copiar/pegar código)
**Cambios requeridos:** Agregar 2 líneas de código HTML

---

## 📦 ¿Qué incluye esta integración?

✅ **Widget flotante** profesional en esquina inferior derecha
✅ **Asistente inteligente** con IA para responder preguntas de expatriados
✅ **Contenido editorial** prioritario (guías propias de la revista)
✅ **Anunciantes destacados** con badges de "PATROCINADO"
✅ **Analytics integrado** para medir engagement y ROI
✅ **Responsive design** funciona perfecto en móvil
✅ **Cero mantenimiento** - actualizaciones automáticas desde nuestro servidor

---

## 🚀 Instrucción de Instalación (SIMPLE)

### Opción 1: Instalación Básica (Recomendado)

Agregar **una sola línea** en el `<head>` de tu sitio:

```html
<!-- Expat Assistant Widget -->
<script src="https://api.barcelona-expats.com/widget/embed.js"></script>
```

**¡Eso es todo!** El widget aparecerá automáticamente en todas las páginas.

---

### Opción 2: Instalación con Personalización

Si deseas personalizar colores, posición o mensajes:

```html
<!-- Configuración del widget (ANTES de cargar embed.js) -->
<script>
  window.ExpatAssistantConfig = {
    apiUrl: 'https://api.barcelona-expats.com',
    primaryColor: '#0066cc',        // Color principal (azul de Barcelona Metropolitan)
    position: 'bottom-right',        // O 'bottom-left'
    greeting: '¡Hola! ¿En qué puedo ayudarte hoy?',
    placeholder: 'Pregunta sobre Barcelona...',
    suggestions: [
      '¿Cómo obtener el NIE?',
      'Busco dentista en Barcelona',
      'Quiero aprender español',
      'Colegios internacionales'
    ]
  };
</script>

<!-- Widget de Expat Assistant -->
<script src="https://api.barcelona-expats.com/widget/embed.js"></script>
```

---

## 🎨 Vista Previa

### Desktop
```
┌─────────────────────────────────────────┐
│  barcelona-metropolitan.com             │
│                                          │
│  [Contenido de la revista]              │
│                                          │
│                                   [💬]  │◄─── Botón flotante
└─────────────────────────────────────────┘
```

### Al hacer clic en el botón:
```
┌─────────────────────────────────────────┐
│  barcelona-metropolitan.com             │
│                                          │
│  [Contenido]                ┌─────────┐ │
│                              │ Chat    │ │
│                              │ Window  │ │
│                              │         │ │
│                              └─────────┘ │
└─────────────────────────────────────────┘
```

---

## 📊 Funcionalidades del Widget

### 1. Respuestas Inteligentes
- Clasificación automática de intenciones (salud, legal, educación, etc.)
- Respuestas contextuales basadas en IA
- Prioriza contenido editorial de Barcelona Metropolitan

### 2. Contenido Editorial (Guías)
El widget muestra primero las **guías editoriales** de la revista:
- Guía del NIE completa
- Sistema de salud en Barcelona
- Educación (escuelas, universidades)
- Trabajo en Barcelona
- Barrios de Barcelona

### 3. Anunciantes Destacados
- Marcados con badge **"PATROCINADO"** en dorado
- Click tracking para medir ROI
- Información completa (contacto, precios, FAQs)

### 4. Datos Complementarios
Si no hay suficiente contenido editorial o anunciantes, el sistema busca automáticamente en OpenStreetMap.

---

## 💰 Modelo de Monetización

### Revenue Streams

1. **Pay-per-Click (PPC)**
   - Anunciantes pagan por cada click en su tarjeta
   - Tracking preciso de conversiones

2. **Featured Placement**
   - Posiciones destacadas en top results
   - Mayor visibilidad = mayor precio

3. **Lead Generation**
   - Formularios de contacto integrados
   - Leads cualificados para sponsors

4. **Sponsored Content**
   - Guías patrocinadas por marcas
   - Native advertising

### Métricas de Éxito Trackeadas

```
📊 Dashboard de Analytics incluye:
├── Queries por categoría
├── Click-through rate de anunciantes
├── Conversion rate a leads
├── Tiempo de respuesta promedio
├── Satisfacción de usuarios
└── Revenue por query
```

---

## 🔧 Especificaciones Técnicas

### Backend
- **Framework:** FastAPI (Python)
- **ML Model:** sentence-transformers (multilingual)
- **APIs:** OpenStreetMap/Nominatim (gratis)
- **Hosting:** Compatible con cualquier servidor Python

### Frontend (Widget)
- **Tamaño:** ~45KB (CSS + JS minificado)
- **Dependencias:** Cero - vanilla JavaScript
- **Compatibilidad:**
  - ✅ Chrome, Firefox, Safari, Edge (últimas 2 versiones)
  - ✅ iOS Safari, Android Chrome
  - ✅ IE11 (con polyfills opcionales)

### Performance
- **Tiempo de carga:** < 500ms
- **Tiempo de respuesta API:** ~800ms promedio
- **Uso de red:** ~2KB por query
- **No bloquea:** Carga asíncrona, no afecta página principal

### Seguridad
- ✅ HTTPS obligatorio en producción
- ✅ CORS configurado solo para barcelona-metropolitan.com
- ✅ Rate limiting (10 queries/minuto por usuario)
- ✅ Input sanitization
- ✅ GDPR compliant

---

## 📱 Responsive Design

### Desktop (> 768px)
- Widget: 380px × 600px
- Posición: Esquina inferior derecha
- Animación suave al abrir/cerrar

### Tablet (481px - 768px)
- Widget: 90% ancho × 80% altura
- Centrado en pantalla

### Mobile (≤ 480px)
- Widget: 100% ancho × 100% altura
- Fullscreen overlay
- Optimizado para touch

---

## 🧪 Testing

### Test en Localhost PRIMERO

Antes de implementar en producción, prueba en tu entorno local:

```html
<!-- Para testing en localhost -->
<script>
  window.ExpatAssistantConfig = {
    apiUrl: 'http://localhost:8000',  // ← Cambiar a producción después
    primaryColor: '#0066cc'
  };
</script>
<script src="http://localhost:8000/widget/embed.js"></script>
```

### Queries de Prueba Recomendadas

```
✅ "¿Cómo obtener el NIE?"          → Debe mostrar guía del NIE
✅ "Busco dentista en Barcelona"    → Debe mostrar anunciantes de salud
✅ "Quiero aprender español"        → Debe mostrar escuelas de idiomas
✅ "Colegios internacionales"       → Debe mostrar colegios + guía educación
✅ "Abogado para extranjeros"       → Debe mostrar abogados
✅ "Información sobre salud"        → Debe mostrar guía sistema salud
```

---

## 🔐 Configuración de Producción

### 1. Backend Deployment

Opciones recomendadas:

**A. VPS/Dedicated Server**
```bash
# Nginx como reverse proxy
server {
    listen 443 ssl;
    server_name api.barcelona-expats.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**B. Docker + Cloud Run (Google Cloud)**
```bash
# Deploy en un comando
gcloud run deploy expat-assistant \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated
```

**C. AWS Lambda + API Gateway**
- Serverless deployment
- Escalado automático
- Pago por uso

### 2. Variables de Entorno

Crear archivo `.env`:
```bash
# Producción
API_URL=https://api.barcelona-expats.com
ALLOWED_ORIGINS=https://www.barcelona-metropolitan.com,https://barcelona-metropolitan.com
RATE_LIMIT=10/minute

# Analytics (opcional)
GOOGLE_ANALYTICS_ID=UA-XXXXXXX-X
GOOGLE_PLACES_API_KEY=your_key_here
```

### 3. Monitoreo

Configurar alertas para:
- ❌ API response time > 2s
- ❌ Error rate > 5%
- ❌ Server downtime
- 📊 Daily usage reports

---

## 📞 Soporte Técnico

### Durante Implementación
- **Email:** support@barcelona-expats.com
- **Tiempo de respuesta:** < 4 horas laborables

### Issues Comunes

#### 1. Widget no aparece
```
Verificar:
□ Script cargado correctamente (ver Network tab)
□ CORS configurado en API
□ No hay errores de JavaScript en consola
□ apiUrl apunta al dominio correcto
```

#### 2. Queries no funcionan
```
Verificar:
□ API backend está running
□ /api/health retorna {"status": "healthy"}
□ Network tab muestra respuesta 200 OK
□ Revisar logs del servidor
```

#### 3. Widget muy lento
```
Soluciones:
□ Habilitar caché de respuestas frecuentes
□ Optimizar tamaño de respuestas
□ CDN para assets estáticos
□ Upgrade plan de hosting
```

---

## 🎓 Recursos Adicionales

### Documentación API
- **Swagger UI:** https://api.barcelona-expats.com/docs
- **ReDoc:** https://api.barcelona-expats.com/redoc

### Ejemplos de Código
```
/examples
├── integration-wordpress.php
├── integration-drupal.module
├── integration-react.jsx
└── integration-vanilla.html
```

### Analytics Dashboard
- **URL:** https://api.barcelona-expats.com/admin/analytics
- **Login:** Se proporciona credenciales privadas

---

## ✅ Checklist de Go-Live

```
□ Widget probado en localhost
□ Queries de prueba funcionan correctamente
□ Analytics configurado y tracking
□ Backend desplegado en servidor de producción
□ SSL/HTTPS habilitado
□ CORS configurado para barcelona-metropolitan.com
□ Variables de entorno de producción configuradas
□ Monitoreo y alertas activos
□ Equipo de soporte notificado
□ Documentación técnica compartida con equipo
```

---

## 📅 Roadmap Post-Launch

### Mes 1-2: Optimización
- [ ] A/B testing de mensajes de greeting
- [ ] Optimización de respuestas basada en analytics
- [ ] Agregar más guías editoriales
- [ ] Expandir base de anunciantes

### Mes 3-4: Features Avanzadas
- [ ] Multiidioma (inglés/español/catalán)
- [ ] Integración con CRM de Barcelona Metropolitan
- [ ] Sistema de feedback de usuarios
- [ ] Guided conversations (wizards)

### Mes 5-6: Expansión
- [ ] Chatbot en WhatsApp/Telegram
- [ ] Email digest semanal personalizado
- [ ] Programa de referidos
- [ ] Marketplace de servicios

---

## 💡 Tips para Maximizar ROI

1. **Promoción del Widget**
   - Mencionar en newsletter
   - Banner en homepage primeros 30 días
   - Social media posts

2. **Contenido Editorial**
   - Crear 2-3 guías nuevas/mes
   - Actualizar guías existentes
   - Promover guías en artículos relacionados

3. **Gestión de Anunciantes**
   - Dashboard de analytics para sponsors
   - Reportes mensuales de performance
   - Paquetes de "Featured Placement"

4. **Engagement**
   - Quick actions contextuales por sección
   - Personalización basada en historial
   - Gamification (badges, achievements)

---

## 📧 Contacto

**Equipo de Desarrollo:**
Email: dev@barcelona-expats.com

**Equipo Comercial:**
Email: sales@barcelona-metropolitan.com

**Emergencias (24/7):**
Tel: +34 XXX XXX XXX

---

## 📄 Licencia y SLA

### Service Level Agreement (SLA)
- **Uptime:** 99.5% mensual
- **Response Time:** < 1s (p95)
- **Support Response:** < 4h laborables

### Licencia
- Código propietario
- Uso exclusivo para Barcelona Metropolitan
- Actualizaciones incluidas sin costo adicional

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Autor:** Equipo Barcelona Expats AI
