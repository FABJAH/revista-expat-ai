# 🦉 Luna Bot - Estructura Completa de Precios Actualizada

**Documentación de la estructura de dos niveles: Directorio + Campañas**

## 📋 Resumen Ejecutivo

La revista ofrece **dos servicios distintos**:

### 1️⃣ **DIRECTORIO** - 34€/mes
- Simple listado del negocio
- Visibilidad ante 12,000+ usuarios mensuales
- SIN marketing activo
- Flexible (puedes cancelar cuando quieras)

### 2️⃣ **CAMPAÑAS** - desde 159€/mes
- Marketing activo y estrategia personalizada
- Acompañamiento de la revista
- Mínimo 6 meses
- 10% descuento si pagas 12 meses completos
- **Precios negociables** según cliente

---

## 💰 Tabla de Precios

### DIRECTORIO
| Plan | Precio | Período | Características |
|------|--------|---------|-----------------|
| **Mensual** | 34€ | Mes | Perfil completo, visibilidad, analytics |
| **Anual** | 367€ | Año | TODO + 10% descuento + asesoramiento |

**Cálculo Anual:** 34€ × 12 = 408€ → Descuento 10% = **367€/año**

### CAMPAÑAS
| Plan | Precio/mes | Mínimo | Anual (10% OFF) | Mejor para |
|------|-----------|--------|-----------------|-----------|
| **Básica** 📢 | 159€ | 6 meses | 1.721€/año | Inicio |
| **Profesional** 🎯 | 199€ | 6 meses | 2.154€/año | MÁS POPULAR |
| **Premium** 👑 | 299€ | 6 meses | 3.240€/año | Máximo impacto |

**Nota:** Todos los precios de campaña son **negociables** según:
- Sector del negocio
- Tamaño de la empresa
- Presupuesto disponible
- Duración del contrato

---

## 🎯 Filosofía de Venta

**"La idea de la revista es ayudar al cliente a llegar a nuevos clientes"**

Esto significa:
- ✅ No vendemos solo visibilidad, vendemos **resultados**
- ✅ El equipo acompaña y ajusta la estrategia
- ✅ Se miden y reportan los resultados
- ✅ Los precios pueden ajustarse si el cliente lo necesita
- ✅ La relación es de **partnership**, no transacción

---

## 📁 Archivos Nuevos

### 1. `config/luna_config_v2.py`
Configuración centralizada con:
- `DIRECTORIO_PLANS`: 2 planes (mensual + anual)
- `CAMPANA_PLANS`: 3 planes (básica, profesional, premium)
- `DESCUENTOS_ANUALES`: Cálculos de ahorros
- `DYNAMIC_MESSAGES`: Mensajes proactivos
- `TESTIMONIOS`: Casos de éxito
- `FAQ`: Preguntas frecuentes

**Funciones útiles:**
```python
from config.luna_config_v2 import *

# Obtener planes
directorio = get_directorio_plans("es")
campanas = get_campana_plans("es")
todos = get_all_plans("es")

# Calcular descuentos
descuento = get_annual_discount("campana_profesional", "es")
precio_anual = calculate_annual_price("campana_profesional", 199)

# Formatear precio
formatted = format_price(1721.2)  # "1.721,20€"
```

### 2. `bots/bot_advertising_sales_v2.py`
Bot mejorado con:
- Detección de intención (saludo, planes, directorio, campaña, etc.)
- Respuestas contextuales según tipo de consulta
- Comparación directorio vs campaña
- Testimonios automáticos
- FAQ integrado
- Soporte bilingual ES/EN

**Uso:**
```python
from bots.bot_advertising_sales_v2 import AdvertisingSalesBot

bot = AdvertisingSalesBot("es")  # o "en"

# Saludar
print(bot.get_greeting())

# Mostrar planes
print(bot.get_plans_comparison())

# Responder pregunta
respuesta = bot.get_response("¿Cuál es el precio del directorio?")

# Crear lead
lead = bot.create_inquiry(
    contact="empresa@example.com",
    plan_type="campana_profesional",
    message="Interesado en campaña"
)
```

---

## 🔄 Diferencias Directorio vs Campaña

### DIRECTORIO (34€/mes)
```
👥 Usuario busca en directorio
📍 Encuentra tu negocio
📞 Te llama si le interesa
```

**Mejor para:** Negocios que buscan visibilidad pasiva

### CAMPAÑA (159€+/mes)
```
👥 Luna promociona tu negocio
📢 Te traemos clientes nuevos
📊 Medimos resultados
👨‍💼 Equipo te acompaña
```

**Mejor para:** Negocios que quieren crecer activamente

---

## 📊 Descuentos y Promociones

### 10% Descuento Anual
- Se aplica a todos los planes de CAMPAÑA
- Aplica si contratas 12 meses completos
- Automáticamente se descuenta del precio

**Ejemplo - Campaña Profesional:**
- Mensual: 199€ × 12 = 2.388€/año
- Anual: 2.388€ × 0.9 = **2.154€/año**
- **Ahorros: 234€**

### Negociación de Precios
Los precios de campaña son **negociables** si:
- Cliente quiere contrato > 6 meses
- Cliente quiere múltiples servicios
- Cliente es referido o retornado
- Presupuesto específico del cliente

---

## 🤖 Mensajes del Bot

El bot enviará automáticamente:

### Saludos Contextuales
- **Mañana:** "¡Buenos días! Soy Luna..."
- **Tarde:** "¡Buenas tardes!..."
- **Noche:** "¡Buenas noches!..."

### Preguntas Proactivas
```
💼 ¿Buscas aumentar visibilidad? Únete a 280+ negocios
📢 ¿Quieres hacer una campaña? Tenemos planes de 159€, 199€, 299€
🚀 ¿Buscas llegar a nuevos clientes? Nuestras campañas te ayudan
🎁 Anual: 10% descuento = Ahorras mucho dinero
```

### Preguntas Frecuentes
- ¿Cuál es la diferencia entre directorio y campaña?
- ¿Son negociables los precios?
- ¿Cuál es el mínimo para campañas?
- ¿Hay descuento anual?
- ¿Cómo es el acompañamiento?

---

## 📈 Testimonios Incluidos

### Restaurante La Viña 🍽️
- Sector: Restaurante
- Resultado: +800% clientes nuevos
- Testimonio: "Pasamos de 5 a 45 clientes nuevos/mes"

### Academia Idiomas Plus 📚
- Sector: Educación
- Resultado: +12 estudiantes nuevos
- Testimonio: "Directorio + campaña = Excelentes resultados"

### Clínica Dental Smile 😁
- Sector: Salud
- Resultado: +45 pacientes nuevos
- Testimonio: "Triplicamos nuestras llamadas"

---

## 🔧 Cómo Integrar

### Opción 1: Backend Python (FastAPI/Flask)
```python
from bots.bot_advertising_sales_v2 import AdvertisingSalesBot
from config.luna_config_v2 import get_all_plans

app.py:
    bot = AdvertisingSalesBot("es")

    @app.post("/api/chat")
    def chat(message: str):
        respuesta = bot.get_response(message)
        return {"response": respuesta}

    @app.get("/api/planes")
    def planes(lang: str = "es"):
        return get_all_plans(lang)
```

### Opción 2: Widget JavaScript
```html
<script src="luna-advertising.js"></script>
<script>
    const widget = new LunaAdvertisingWidget({
        apiEndpoint: '/api/bot/advertising',
        language: 'es',
        theme: 'dark'
    });
</script>
```

---

## ✅ Checklist de Implementación

- [ ] Copiar `config/luna_config_v2.py`
- [ ] Copiar `bots/bot_advertising_sales_v2.py`
- [ ] Importar en rutas/API
- [ ] Probar saludos en ES/EN
- [ ] Probar respuestas de precios
- [ ] Probar detección de intención
- [ ] Probar testimonios
- [ ] Probar FAQ
- [ ] Integrar con widget
- [ ] Validar en `setup_luna.py`

---

## 📞 Contacto y Negociación

Para planes de campaña:
1. Bot detecta interés
2. Bot recopila información del cliente
3. Equipo de ventas se contacta
4. Se valida presupuesto y necesidades
5. Se ajusta precio si es necesario
6. Se formaliza contrato

**Lead Template:**
```json
{
  "timestamp": "2024-01-15T14:30:00",
  "empresa": "Mi Negocio SL",
  "sector": "Restaurante",
  "contacto": "info@minegocio.com",
  "plan_interes": "campana_profesional",
  "presupuesto": "200€ máximo",
  "mensaje": "Interesado en aumentar clientes",
  "status": "nuevo"
}
```

---

## 🎓 Notas Importantes

1. **Directorio es la puerta de entrada** - Muchos clientes pequeños empiezan aquí
2. **Campaña es el crecimiento** - Clientes que quieren resultados
3. **Los precios son claros pero negociables** - No es un "precio fijo" sino una oferta base
4. **El equipo de ventas es importante** - Luna abre la puerta, pero humanos cierran
5. **ROI es la métrica clave** - "¿Cuántos clientes nuevos obtuve?"

---

**Última actualización:** Enero 2024
**Versión:** Luna Bot 2.0 - Estructura de Dos Niveles
**Responsable:** Equipo de Marketing Revista-Expats
