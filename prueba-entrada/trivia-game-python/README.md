# Trivia Game


Un juego de trivia simple construido con Python que prueba tus conocimientos en varias categorías.

## Instrucciones de Configuración

### Configuración Local

1. Crear un entorno virtual:
```bash
python -m venv venv
```

2. Activar el entorno virtual:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Copiar el archivo de entorno:
```bash
cp .env.example .env
```

5. Ejecutar la aplicación: (Aún no implementado)
```bash
python app/main.py
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

La aplicación estará disponible en:
http://localhost:8000
