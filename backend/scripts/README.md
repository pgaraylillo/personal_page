# Scripts de Automatización

## Investigación Médica Diaria

El script `daily_medical_research.py` investiga un tema médico relevante cada día, genera una imagen relacionada y crea un archivo markdown para publicación.

### Características

- 🔍 **Investigación automática**: Usa IA para seleccionar un tema médico relevante
- 📝 **Generación de contenido**: Crea artículos completos sobre el tema seleccionado
- 🎨 **Generación de imágenes**: Crea ilustraciones médicas profesionales con DALL-E
- 📄 **Archivos Markdown**: Guarda el contenido en `data/blog/` con formato correcto

### Requisitos

1. **Dependencias Python instaladas**:
   ```bash
   cd /root/personal_page/backend
   pip install -r requirements.txt
   ```
   
   O si usas Docker:
   ```bash
   docker-compose exec backend pip install -r requirements.txt
   ```

2. **Variables de entorno configuradas en `.env`**:
   - `OPENAI_API_KEY`: API key de OpenAI para generar contenido e imágenes

### Verificar Dependencias

Antes de ejecutar, verifica que todo esté instalado:
```bash
python3 backend/scripts/check_dependencies.py
```

### Uso Manual

**IMPORTANTE**: Usa el script `daily_medical_research.py`, NO ejecutes directamente `medical_research_service.py`

**Con entorno virtual (recomendado):**
```bash
cd /root/personal_page
source venv/bin/activate
python backend/scripts/daily_medical_research.py
```

**Si usas Docker:**
```bash
docker-compose exec backend python3 backend/scripts/daily_medical_research.py
```

### Programación Automática (Cron)

Para ejecutar diariamente a las 9:00 AM:

```bash
# Editar crontab
crontab -e

# Agregar esta línea (con entorno virtual):
0 9 * * * cd /root/personal_page && source venv/bin/activate && python backend/scripts/daily_medical_research.py >> /var/log/medical_research.log 2>&1
```

Para ejecutar diariamente a una hora específica, ajusta los valores:
```
minuto hora * * * comando
```

Ejemplos:
- `0 9 * * *` - Todos los días a las 9:00 AM
- `0 8 * * 1` - Todos los lunes a las 8:00 AM
- `30 14 * * *` - Todos los días a las 2:30 PM

### Archivos Generados

- **Markdown**: `data/blog/[tema]-[fecha].md`
- **Imagen**: `frontend/img/[tema]-[fecha].png`

### Notas

- El script verifica si ya existe un archivo con el mismo nombre para evitar sobrescrituras
- Los archivos se nombran automáticamente con fecha para facilitar el seguimiento
- Las imágenes se generan en formato PNG de 1024x1024 píxeles
