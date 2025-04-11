# Juego de Trivia

Un juego de trivia simple construido con Python que prueba tus conocimientos en varias categorías.

## Instrucciones de Juego

El juego consiste en responder correctamente 10 preguntas de trivia. El jugador recibirá una pregunta a la vez y deberá elegir una de las cuatro opciones disponibles.

- Al iniciar el juego, se mostrará un mensaje de bienvenida con instrucciones.
- Para responder, el jugador debe ingresar el número correspondiente a la opción elegida (1-4).
- Por cada respuesta correcta, el jugador recibirá 1 punto.
- Al finalizar las 10 preguntas, se mostrará un resumen con el total de respuestas correctas e incorrectas.


## Clases Principales

- **Question**: Representa una pregunta con opciones y respuesta correcta
- **Quiz**: Gestiona una colección de preguntas y el flujo de avance 
- **GameManager**: Maneja la lógica del juego y el seguimiento de puntuación
- **ConsoleInterface**: Gestiona la interacción con el usuario en la consola

## Cómo ejecutar el juego

Para jugar, asegúrate de estar en el directorio raíz del proyecto y ejecuta:

```bash
python -m app.main
```

## Instrucciones de Configuración

### Configuración Local

1. Clonar el repositorio:
```bash
cd trivia-game-python
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Copiar el archivo de entorno:
```bash
cp .env.example .env
```

6. Ejecutar la aplicación:
```bash
python -m app.main
```

### Configuración con Docker

1. Construir y ejecutar con Docker Compose:
```bash
docker-compose up --build
```

Para ejecutar los contenedores en segundo plano (modo detached), usa:
```bash
docker-compose up -d --build
```
El flag `-d` (detached) permite que los contenedores se ejecuten en segundo plano, liberando tu terminal para otros comandos.

## Desarrollo

### Ejecución de Pruebas


Para ejecutar todas las pruebas:
```bash
python -m pytest
```

Para ejecutar pruebas con detalles:
```bash
python -m pytest -v
```

> Nota: Ejecutar solo `pytest` directamente puede causar errores de importación de módulos.

## Documentación

La documentación detallada del proceso de desarrollo se encuentra en la carpeta `docs/`:
- `dia1.md`: Configuración inicial del proyecto
- `dia2.md`: Implementación de la clase Question y pruebas básicas
- `dia3.md`: Implementación de la clase Quiz, refactorización y flujo del juego
