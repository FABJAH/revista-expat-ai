# ⚡ GUÍA RÁPIDA - Conectar API Barcelona Metropolitan

**Tiempo estimado**: 5 minutos

---

## 📦 Qué está listo

✅ **Código**: DirectoryConnector creado
✅ **Integración**: Orchestrator actualizado
✅ **Tests**: Script de prueba incluido
✅ **Documentación**: Completa en `INTEGRACION_DIRECTORIO_BM.md`

---

## 🎯 Solo necesitas 2 cosas

Cuando Barcelona Metropolitan te dé:

### 1. **URL de la API**
```
Ejemplo: https://api.barcelona-metropolitan.com/advertisers
O: https://www.barcelona-metropolitan.com/api/advertisers
```

### 2. **API Key** (si es necesaria)
```
Ejemplo: sk_live_xxxxxxxxxxxxx
```

---

## 🔧 3 Pasos para conectar

### Paso 1: Actualiza `.env`

```bash
# Abre o crea archivo .env en la raíz del proyecto
nano .env

# Agrega o actualiza:
BM_DIRECTORY_API_URL=https://tu-api-aqui/advertisers
BM_API_KEY=tu_api_key_aqui
```

Guarda con `Ctrl+O`, `Enter`, `Ctrl+X`

### Paso 2: Prueba la conexión

```bash
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

### Paso 3: ¡Listo!

El bot ahora usa datos reales de Barcelona Metropolitan.

```python
# Internamente, automáticamente:
orchestrator.directory.get_all_advertisers()
# ↓ Obtiene datos actualizados de la API
```

---

## ❓ ¿Qué datos devuelve la API?

La API debe devolver estructura como esta:

```json
{
  "advertisers": [
    {
      "id": "123",
      "nombre": "Hotel ABC Barcelona",
      "categoria": "Accommodation",
      "descripcion": "Hotel de lujo en Paseo de Gracia",
      "contacto": "93 123 4567",
      "email": "info@hotelabcbcn.com",
      "website": "www.hotelabcbcn.com",
      "precio": "€150-300",
      "ubicacion": "Paseo de Gracia, Barcelona"
    }
  ]
}
```

Si tiene estructura diferente, se puede adaptar en 5 minutos.

---

## 🚨 Si falla la conexión

### Error: "404 - No encontrado"
```bash
# Verifica la URL
curl https://tu-url-api/advertisers
```

### Error: "401 - No autorizado"
```bash
# Verifica API_KEY en .env
# Debe ser exacto (sin espacios)
```

### Error: "Timeout"
```bash
# La API está lenta
# El bot automáticamente usa anunciantes.json como fallback
# No se rompe nada
```

---

## 📊 Después de conectar

Automáticamente sucede:

1. ✅ **Datos actualizados**: El bot siempre tiene datos frescos
2. ✅ **Análitica**: Se trackea cada recomendación
3. ✅ **Escalabilidad**: Funciona con cualquier cantidad de anunciantes
4. ✅ **Confiabilidad**: Si API falla, usa JSON local

---

## 🎓 Verificar que funciona

Abre Python y prueba:

```python
from bots.directory_connector import get_directory_connector

connector = get_directory_connector()

# Obtener anunciantes
anunciantes = connector.get_all_advertisers()
print(f"✅ Cargados {len(anunciantes)} anunciantes")

# Buscar
resultados = connector.search_advertisers("hotel")
print(f"✅ Encontrados {len(resultados)} hoteles")
```

Si ambos funcionan, ¡todo está correcto!

---

## 📞 Contacto si necesitas ayuda

Si algo no funciona:

1. Revisa el archivo `INTEGRACION_DIRECTORIO_BM.md` (documentación completa)
2. Ejecuta `python test_directory_integration.py`
3. Revisa los logs en los archivos de log

---

## 🎉 ¡Resumen!

| Paso | Acción | Tiempo |
|------|--------|--------|
| 1 | Recibir URL y API Key de BM | 0 min |
| 2 | Actualizar `.env` | 1 min |
| 3 | Ejecutar test | 1 min |
| 4 | ✅ ¡Listo! | 2 min |

**Total: 5 minutos** ⏱️

---

**¿Preguntas?** Revisa `INTEGRACION_DIRECTORIO_BM.md` para documentación completa.
