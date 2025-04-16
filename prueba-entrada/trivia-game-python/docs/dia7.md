# Día 7 - Gestión de configuración, seguridad y pruebas de rendimiento

## Tareas Realizadas

### 1. Gestión de Variables de Entorno
- Añadimos `SECRET_KEY` al archivo `.env` para almacenar de forma segura la clave secreta
- Verificamos que `python-dotenv` esté cargando correctamente las variables de entorno en los módulos clave
- Configuramos la API para utilizar la clave secreta desde el entorno

Archivo `.env` actualizado:


### 2. Implementación de Seguridad
- Agregamos Bandit al archivo `requirements.txt` para análisis de seguridad del código
- Configuramos el flujo de trabajo de GitHub Actions para ejecutar escaneos de seguridad automáticamente
- Configuramos el análisis para generar resultados en formato JSON para integración con herramientas de monitoreo

Paso añadido al archivo de CI de GitHub Actions:
```yaml
- name: Run Security Scan
  run: |
    pip install bandit
    bandit -r app/ -f json -o bandit-results.json
```

### 3. Mejora de Seguridad en la Generación de Números Aleatorios
- Importamos el módulo `secrets` en `api.py` para generación segura de números aleatorios
- Reemplazamos el uso de `random.sample()` con el siguiente algoritmo más seguro:

```python
indices = set()
while len(indices) < count:
    indices.add(secrets.randbelow(len(all_questions)))
    
selected_questions = [all_questions[i] for i in indices]
all_questions = selected_questions
```

### 4. Implementación de Pruebas de Carga
- Agregamos Locust al archivo `requirements.txt` para pruebas de rendimiento
- Creamos un archivo `locustfile.py` con escenarios de prueba completos:
  - Obtención de preguntas aleatorias (peso 3)
  - Filtrado de preguntas por dificultad (peso 1)
  - Respuesta a preguntas (peso 2)
  - Obtención de estadísticas de quiz (peso 1)
  - Reinicio del quiz (peso 1)
- Configuramos tiempos de espera aleatorios entre 1 y 5 segundos para simular comportamiento real de usuarios

