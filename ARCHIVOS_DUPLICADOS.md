# ⚠️ ARCHIVOS DUPLICADOS - GUÍA DE LIMPIEZA

## 📋 SERVIDORES (HAY 3 VERSIONES)

### ✅ **USAR ESTE** (Optimizado):
```
main.py
```
- FastAPI con todas las optimizaciones
- GZip compression
- Rate limiting
- CORS seguro
- Buffer de analytics
- **ESTE ES EL ARCHIVO PRINCIPAL**

### ⚠️ OBSOLETOS (No usar):

1. **app.py** (Flask - versión antigua)
   - Servidor Flask sin optimizaciones
   - Reemplazado por main.py
   - **PUEDE ELIMINARSE**

2. **backend/app.py** (FastAPI básico)
   - Versión antigua de FastAPI
   - Sin optimizaciones
   - **PUEDE ELIMINARSE**

3. **backend/main.py**
   - Duplicado de configuración
   - **PUEDE ELIMINARSE**

---

## 🗂️ OTROS ARCHIVOS DUPLICADOS

### Config:
- `config.py` (raíz) - Obsoleto
- `config/settings.py` - ✅ Usar este
- `config/luna_config.py` - Para bot Luna
- `config/luna_config_v2.py` - Versión más reciente

### Documentación redundante:
- Múltiples archivos LUNA_*.md con información similar

---

## 🧹 RECOMENDACIÓN DE LIMPIEZA

### 1. Eliminar archivos obsoletos:
```bash
# CUIDADO: Hacer backup antes
rm app.py
rm app.py.save
rm config.py
rm backend/app.py
rm backend/main.py
```

### 2. Consolidar documentación Luna:
- Mantener solo `LUNA_README.md` actualizado
- Archivar el resto en carpeta `docs/archive/`

### 3. Limpiar scripts de test antiguos:
```bash
# Mantener solo test_performance.py (nuevo)
mv test_server.py docs/archive/
mv test_rss_integration.py docs/archive/
```

---

## ✅ ESTRUCTURA RECOMENDADA

```
Revista-expats-ai/
├── main.py                    # ✅ Servidor principal (optimizado)
├── requirements.txt           # ✅ Dependencias
├── config/
│   ├── settings.py           # ✅ Config principal
│   └── luna_config_v2.py     # ✅ Config Luna
├── bots/                      # ✅ Lógica de bots
├── routes/                    # ✅ APIs
├── data/                      # ✅ Datos JSON
├── frontend/                  # ✅ Frontend
├── widget/                    # ✅ Widget embebible
├── docs/                      # ✅ Documentación
│   ├── OPTIMIZACIONES_RENDIMIENTO.md
│   └── archive/              # Archivos antiguos
└── test_performance.py       # ✅ Tests
```

---

## 🚀 COMANDO PARA ARRANCAR EL SERVIDOR CORRECTO

```bash
# Desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Producción
export PRODUCTION=true
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## ❌ NO USAR ESTOS COMANDOS

```bash
# NO USAR: app.py es Flask antiguo
python app.py

# NO USAR: backend/app.py es versión antigua
uvicorn backend.app:app
```

---

**Última actualización**: 28 de diciembre de 2025
