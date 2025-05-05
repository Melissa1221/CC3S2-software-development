# Actividad: Escribir aserciones en pruebas con pytest

Esta actividad se centra en el aprendizaje de pytest como herramienta para ejecutar pruebas unitarias en Python, específicamente para una implementación de la estructura de datos Stack (Pila). 

## Paso 1: Instalando pytest y pytest-cov

Primero creé la carpeta correspondiente a la actividad (activity11), luego creé y activé el entorno virtual en el cual se instalarán las dependencias requeridas, para este caso `pytest` y `pytest-cov`:

```bash
python -m venv venv
source venv/bin/activate # En mi caso uso wsl de arch linux
pip install pytest pytest-cov
```

## Paso 2: Estructura de la implementación Stack

La actividad consiste en probar una implementación de Stack (Pila) con los siguientes métodos:

- `push()`: Añade un elemento a la parte superior de la pila.
- `pop()`: Elimina y devuelve el elemento en la parte superior de la pila.
- `peek()`: Devuelve el valor del elemento en la parte superior de la pila sin eliminarlo.
- `is_empty()`: Devuelve True si la pila está vacía y False si no lo está.

## Paso 3: Corrigiendo errores en las pruebas existentes

Al ejecutar las pruebas inicialmente, encontré un error en la función `test_is_empty()` que carecía del parámetro `self` requerido. Corregí esto al añadir el parámetro y además mejoré la implementación utilizando los métodos de aserción de unittest en lugar de assertions simples:

```python
def test_is_empty(self) -> None:
    """Prueba de si la pila está vacía."""
    stack = Stack()
    self.assertTrue(
        stack.is_empty(),
        "La pila recién creada debe estar vacía"
    )
    stack.push(5)
    self.assertFalse(
        stack.is_empty(),
        "Después de agregar un elemento, la pila no debe estar vacía"
    )
```

## Paso 4: Verificando las pruebas con pytest

Ejecuté las pruebas usando el comando `pytest -v` para verificar si todas las pruebas pasan correctamente:

![](https://i.imgur.com/wq6G3va.png)

Las cuatro pruebas (`test_push`, `test_pop`, `test_peek` y `test_is_empty`) pasaron correctamente, lo que indica que la implementación de Stack funciona como se espera.

## Paso 5: Añadiendo cobertura de pruebas con pytest-cov

Para asegurarme de que mis pruebas cubren suficiente código, utilicé pytest-cov para generar informes de cobertura:

```bash
pytest --cov=stack --cov-report=term-missing
```

El resultado mostró una cobertura del 100% para `stack.py`, indicando que todas las líneas de código están siendo probadas:

![](https://i.imgur.com/Hsv4Asf.png)

## Paso 6: Generando reportes HTML para mejor visualización

También generé un informe de cobertura en formato HTML para una revisión más detallada:

```bash
pytest --cov=stack --cov-report=html
```

Este comando genera un directorio `htmlcov` con un informe interactivo que permite ver exactamente qué líneas de código están siendo cubiertas.

![](https://i.imgur.com/IVlaF0x.png)

## Paso 7: Automatizando la configuración con setup.cfg

Para facilitar la ejecución de pruebas con configuraciones específicas, se puede utilizar un archivo `setup.cfg` con configuraciones predefinidas. Esto permite ejecutar simplemente `pytest` y obtener automáticamente informes de cobertura y salida detallada:

```
[tool:pytest]
addopts = -v --tb=short --cov=stack --cov-report=term-missing

[coverage:run]
branch = True
omit =
    */tests/*
    */test_*

[coverage:report]
show_missing = True

```
Con esto como se mencionó al ejecutar `pytest` ya contiene las configuraciones deseadas
![](https://i.imgur.com/8JhsncP.png)