# ✅ CHECKLIST - Activación API Barcelona Metropolitan

**Usa esto cuando Barcelona Metropolitan te dé los datos**

---

## 📋 FASE 1: Recibir Información (cuando contacten)

### Datos necesarios:
- [ ] URL de la API del directorio
  ```
  Ejemplo: https://api.barcelona-metropolitan.com/advertisers
  Recibido: ________________________
  ```

- [ ] API Key (si es necesaria)
  ```
  Ejemplo: sk_live_xxxxx
  Recibido: ________________________
  ```

- [ ] Estructura de respuesta (JSON sample)
  ```
  Pegarlo aquí:
  ```

- [ ] Categorías disponibles
  ```
  Ejemplo: Accommodation, Healthcare, Legal, etc.
  Disponibles: ________________________
  ```

### Verificación:
- [ ] Contacto: Responsable en BM para soporte
- [ ] Documentación: Acceso a docs de API
- [ ] Límites: Rate limiting, máximo de requests

---

## 🔧 FASE 2: Configuración (5 minutos)

### Paso 1: Actualizar `.env`

```bash
# Abrir o crear archivo .env en raíz del proyecto
nano .env

# Agregar:
BM_DIRECTORY_API_URL=https://url_aqui/advertisers
BM_API_KEY=api_key_aqui

# Guardar: Ctrl+O, Enter, Ctrl+X
```

- [ ] `.env` actualizado con URL
- [ ] `.env` actualizado con API Key
- [ ] Archivos guardados

### Paso 2: Verificar estructura de datos

Si respuesta tiene estructura diferente a:
```python
{
  "advertisers": [
    {
      "id": "...",
      "nombre": "...",
      "categoria": "...",
      ...
    }
  ]
}
```

Entonces editar: `bots/directory_connector.py` línea ~65
- [ ] Estructura validada
- [ ] Mapping de campos (si es necesario)

---

## 🧪 FASE 3: Testing (2 minutos)

### Test automatizado:
```bash
cd /home/fleet/Escritorio/Revista-expats-ai
python test_directory_integration.py
```

Debe mostrar:
```
✅ PASÓ DirectoryConnector
✅ PASÓ Orchestrator
✅ PASÓ Consulta
✅ PASÓ Búsqueda

🎉 ¡TODAS LAS PRUEBAS PASARON!
```

- [ ] Test DirectoryConnector pasó
- [ ] Test Orchestrator pasó
- [ ] Test Consulta pasó
- [ ] Test Búsqueda pasó
- [ ] Todos los tests pasaron

### Test manual (Python):
```python
from bots.directory_connector import get_directory_connector

connector = get_directory_connector()
anunciantes = connector.get_all_advertisers(limit=5)
print(f"✅ Cargados {len(anunciantes)} anunciantes")

# Debe devolver > 0
```

- [ ] Test manual ejecutado
- [ ] Anunciantes cargados correctamente

---

## 📊 FASE 4: Validación de Datos

### Verificar anunciantes cargados:
```python
from bots.directory_connector import get_directory_connector

connector = get_directory_connector()

# 1. Total de anunciantes
all_ads = connector.get_all_advertisers(limit=500)
print(f"Total: {len(all_ads)}")

# 2. Por categoría
for category in ["Accommodation", "Healthcare", "Legal"]:
    cat_ads = connector.get_by_category(category)
    print(f"{category}: {len(cat_ads)} anunciantes")

# 3. Búsqueda
results = connector.search_advertisers("hotel", limit=5)
print(f"Búsqueda 'hotel': {len(results)} resultados")
```

- [ ] Total de anunciantes verificado
- [ ] Categorías principales tienen datos
- [ ] Búsqueda funciona
- [ ] Datos son coherentes

---

## 🚀 FASE 5: Integración con Bot

### Prueba consulta completa:
```python
from bots.orchestrator import Orchestrator

orch = Orchestrator()

# Test español
response_es = orch.process_query("Necesito hotel en Barcelona", language="es")
print(f"ES: {len(response_es['json'])} resultados")

# Test inglés
response_en = orch.process_query("Need hotel in Barcelona", language="en")
print(f"EN: {len(response_en['json'])} resultados")
```

- [ ] Bot carga datos del directorio (no JSON)
- [ ] Consultas en español funcionan
- [ ] Consultas en inglés funcionan
- [ ] Resultados relevantes

### Verificar tracking:
```bash
# Revisar logs
tail -f logs/bot.log | grep "track"

# Debe mostrar:
# "✅ Recomendación tracked: advertiser_id"
```

- [ ] Tracking de recomendaciones funciona
- [ ] Logs muestran actividad

---

## 📈 FASE 6: Performance

### Prueba de carga:
```python
import time
from bots.orchestrator import Orchestrator

orch = Orchestrator()
start = time.time()

for i in range(10):
    orch.process_query("hotel barcelona")

elapsed = time.time() - start
print(f"10 consultas en {elapsed:.2f}s")
# Debe ser < 5 segundos
```

- [ ] Tiempo de respuesta aceptable (< 0.5s por consulta)
- [ ] No hay memory leaks
- [ ] CPU usage normal

---

## ✅ FASE 7: Deploy a Producción

### Pre-deploy checklist:
- [ ] Todos los tests pasaron
- [ ] `.env` configurado correctamente
- [ ] No hay datos sensibles en código
- [ ] Logs activos
- [ ] Fallback a JSON funciona

### Deploy:
```bash
# 1. Commit cambios
git add .env
git commit -m "Configure Barcelona Metropolitan API"

# 2. Deploy a producción
# (tu proceso habitual de deploy)

# 3. Verificar en producción
curl https://tu-api.com/api/v1/query -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "hotel barcelona", "language": "en"}'

# Debe devolver anunciantes del directorio real
```

- [ ] Cambios commiteados
- [ ] Deployed a producción
- [ ] Verificado en producción
- [ ] ¡Activo en vivo!

---

## 🎯 Post-Launch

### Monitoreo:
- [ ] Logs sin errores
- [ ] Recomendaciones siendo trackeadas
- [ ] Analytics en Barcelona Metropolitan actualizándose
- [ ] Performance dentro de límites

### Optimizaciones futuras:
- [ ] Análisis de qué se vende más
- [ ] A/B testing de categorías
- [ ] Mejora de búsqueda semántica
- [ ] Integración con landing page

---

## 📞 Soporte

### Si algo falla:

1. **Conectividad API**:
   ```bash
   curl BM_DIRECTORY_API_URL -H "Authorization: Bearer $BM_API_KEY"
   ```

2. **Estructura de datos**:
   - Revisar JSON response real vs esperado
   - Ajustar mapping en `directory_connector.py` si es necesario

3. **Performance**:
   - Activar mode debug: `DEBUG=true` en .env
   - Revisar logs para bottlenecks

4. **Contactar Barcelona Metropolitan**:
   - Responsable: ___________________
   - Email: ________________________
   - Teléfono: ____________________

---

## 📝 Notas

Espacio para tomar notas durante la integración:

```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

## ✨ Resultado Final

Cuando completes esta checklist:

✅ Bot conectado con directorio REAL de Barcelona Metropolitan
✅ Datos siempre actualizados
✅ Analytics integrado
✅ Todo probado y validado
✅ Listo para producción

---

**Fecha de inicio**: ____________
**Fecha de completación**: ____________
**Responsable**: ________________
