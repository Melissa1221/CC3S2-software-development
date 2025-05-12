# Actividad: Cobertura de pruebas

Esta actividad se centra en la implementación y mejora de la cobertura de pruebas en un modelo SQLAlchemy para una aplicación Flask. A través de diferentes ejercicios, se aprende a utilizar herramientas de cobertura de código y a optimizar el proceso de pruebas con Makefiles.

## Paso 1: Preparación del entorno y diagnóstico inicial

Lo primero que hice fue examinar la estructura del proyecto y ejecutar las pruebas para entender el estado actual:

```bash
pytest
```

Sin embargo, encontré un error 

```
RuntimeError: Working outside of application context.
```

Este error ocurre porque las pruebas estaban intentando acceder a la base de datos sin un contexto de aplicación Flask activo.

## Paso 2: Corregir el error del contexto de aplicación

Para solucionar este problema, modifiqué el archivo `tests/test_account.py` para incluir el contexto de aplicación en cada prueba:

1. Importé la aplicación Flask desde el módulo models:
   ```python
   from models import db, app
   ```

2. Actualicé el fixture de configuración de base de datos para usar un contexto de aplicación:
   ```python
   @pytest.fixture(scope="module", autouse=True)
   def setup_database():
       """Configura la base de datos antes y después de todas las pruebas"""
       with app.app_context():
           db.create_all()   # Crea las tablas según los modelos
           yield
           # Se ejecuta después de todas las pruebas
           db.session.close()
   ```

3. Añadí el contexto de aplicación a todos los métodos de prueba:
   ```python
   def test_create_an_account(self):
       """Probar la creación de una sola cuenta"""
       with app.app_context():
           data = ACCOUNT_DATA[0]  # obtener la primera cuenta
           account = Account(**data)
           account.create()
           assert len(Account.all()) == 1
   ```

## Paso 3: Solucionar el error de formato de fecha

Después de arreglar el contexto de aplicación, surgió un nuevo error al ejecutar las pruebas:

```
ValueError: Invalid isoformat string: '2025-05-11 21:44:33'
```

El problema estaba en el tipo de campo de la columna `date_joined` en el modelo Account. SQLAlchemy esperaba un formato ISO para el tipo Date, pero estaba recibiendo un string con fecha y hora.

Para solucionar esto, modifiqué el modelo `models/account.py`:

1. Cambié el tipo de columna de Date a DateTime:
   ```python
   from sqlalchemy import Column, Integer, String, Boolean, DateTime
   # ...
   date_joined = Column(DateTime, nullable=False, server_default=func.now())
   ```

## Paso 4: Ejecutar las pruebas con éxito

Una vez solucionados todos los problemas, ejecuté las pruebas de nuevo:

```bash
pytest
```

Esta vez todas las pruebas pasaron correctamente, lo que indica que el modelo Account está funcionando como se espera.

## Paso 5: Adaptar el Makefile al proyecto

El último problema estaba en el Makefile, configurado para buscar los proyectos en una carpeta `Actividades/`, pero en este caso la actividad estaba directamente en la raíz del proyecto.

Modifiqué el Makefile para adaptarlo a la estructura del proyecto:

1. Actualicé el comando `test`:
   ```make
   .PHONY: test
   test:
   	@echo "Ejecutando pruebas en la actividad: $(ACTIVITY)"
   	PYTHONWARNINGS="ignore::DeprecationWarning" pytest . --ignore=venv
   ```

2. Simplifiqué el comando `coverage_individual`:
   ```make
   .PHONY: coverage_individual
   coverage_individual:
   	@echo "Ejecutando cobertura individual para cada actividad..."
   	@echo "=========================================="; \
   	echo "Generando cobertura para $(ACTIVITY)"; \
   	echo "=========================================="; \
   	coverage erase && \
   	PYTHONWARNINGS="ignore::DeprecationWarning" coverage run --source=models,tests --omit="venv/*" -m pytest . && \
   	coverage report -m && \
   	coverage html -d htmlcov_$(ACTIVITY)
   ```

3. Actualicé el comando `lint` para excluir directorios innecesarios:
   ```make
   .PHONY: lint
   lint:
   	@echo "Ejecutando flake8..."
   	flake8 . --exclude=venv,htmlcov_*,.pytest_cache,__pycache__
   ```

Finalmente, ejecuté el comando de cobertura individual para verificar la calidad de las pruebas:

```bash
make coverage_individual
```

El resultado generó un reporte HTML en el directorio `htmlcov_activity15` que muestra una cobertura del 100% para todos los archivos del proyecto:
![](https://i.imgur.com/xib060G.png)

El reporte HTML proporciona una interfaz interactiva para explorar la cobertura de código en detalle, permitiendo ver exactamente qué líneas de código están siendo ejecutadas durante las pruebas.

![](https://i.imgur.com/RwZj318.png)

El reporte fue generado por coverage.py v7.8.0, y confirma que todas las declaraciones en nuestro código están siendo probadas adecuadamente, lo que nos da confianza en la calidad y robustez de nuestras pruebas.

## Ejercicio 1: Análisis y evaluación de la cobertura actual

Analicé en detalle el reporte de cobertura HTML generado en `htmlcov_activity15`:

1. **Cobertura de models/account.py:**
   - Todos los métodos CRUD (`create`, `update`, `delete`) tienen una cobertura completa.
   - El método `update` tiene dos ramas condicionales (verificación de ID) y ambas están cubiertas.
   - Los métodos de clase `all` y `find` también tienen 100% de cobertura.

2. **Cobertura de models/__init__.py:**
   - Las 6 declaraciones en este archivo están completamente cubiertas, incluyendo la inicialización de la aplicación Flask y la configuración de la base de datos.

3. **Cobertura de tests/test_account.py:**
   - Aunque este archivo es de pruebas, es importante que también tenga cobertura completa para asegurar que todas las pruebas se ejecuten correctamente.

## Ejercicio 2: Ampliación de pruebas para mejorar la cobertura

Ahora debemos agregar pruebas adicionales para cubrir casos límite y comportamientos específicos:

1. **Prueba para verificar valores específicos al crear una cuenta:**
   ```python
   def test_account_has_id_after_create(self):
       """Verifica que se asigne un ID después de crear una cuenta"""
       with app.app_context():
           account = Account(name="Test ID", email="testid@example.com")
           assert account.id is None  # No tiene ID antes de crear
           account.create()
           assert account.id is not None  # Debe tener ID después de crear
   ```

2. **Prueba para verificar detalles del formato de to_dict:**
   ```python
   def test_to_dict_types(self):
       """Verifica que los tipos de datos en el diccionario sean correctos"""
       with app.app_context():
           account = Account(name="Type Test", email="type@test.com")
           account.create()
           data = account.to_dict()
           assert isinstance(data["id"], int)
           assert isinstance(data["name"], str)
           assert isinstance(data["email"], str)
           assert isinstance(data["disabled"], bool)
   ```

## Ejercicio 3: Optimización adicional del Makefile

Implementé un nuevo target en el Makefile para generar un reporte consolidado de cobertura:

```make
.PHONY: coverage_all
coverage_all:
	@echo "Generando reporte consolidado de cobertura..."
	coverage erase
	PYTHONWARNINGS="ignore::DeprecationWarning" coverage run --source=models,tests --omit="venv/*" -m pytest .
	coverage report -m
	coverage html -d htmlcov_consolidado
	@echo "Reporte consolidado generado en htmlcov_consolidado/index.html"
```

Este target permite generar un reporte único que consolida la cobertura de todo el proyecto, facilitando la visualización general del estado de las pruebas.
![](https://i.imgur.com/5VeCbyN.png)

## Ejercicio 4: Integración de base de datos temporal para pruebas

Para evitar que las pruebas modifiquen la base de datos principal, configuré una base de datos en memoria para las pruebas:

1. **Modificación del archivo `models/__init__.py`:**
   ```python
   import os
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy

   app = Flask(__name__)
   if os.environ.get('TESTING'):
       app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
   else:
       app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   db = SQLAlchemy(app)
   ```

2. **Configuración de la variable de entorno en las pruebas:**
   Modifiqué `tests/test_account.py` para establecer la variable de entorno:
   ```python
   import os
   os.environ['TESTING'] = '1'
   ```

3. **Verificación:**
   Ejecuté las pruebas nuevamente y confirmé que no se modificó la base de datos `test.db`, sino que se usó una base de datos en memoria que se destruye al finalizar las pruebas.

## Ejercicio 5: Implementación de nuevas funcionalidades

Para extender la funcionalidad del modelo, implementé un método de validación para verificar datos antes de guardarlos:

1. **Añadí el método `validate` a la clase Account:**
   ```python
   import re

   def validate(self):
       """Valida los datos de la cuenta antes de guardarlos"""
       if not self.name:
           raise DataValidationError("El nombre no puede estar vacío")
       if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
           raise DataValidationError("El email no es válido")
       return True
   ```

2. **Actualización del método `create` para validar antes de guardar:**
   ```python
   def create(self):
       """Crea una Cuenta en la base de datos"""
       logger.info(f"Creando {self.name}")
       self.validate()  # Validar antes de guardar
       db.session.add(self)
       db.session.commit()
   ```

3. **Nuevas pruebas para el método de validación:**
   ```python
   def test_validate_valid_account(self):
       """Prueba la validación con datos correctos"""
       with app.app_context():
           account = Account(name="Valid", email="valid@example.com")
           assert account.validate() is True

   def test_validate_empty_name(self):
       """Prueba la validación con nombre vacío"""
       with app.app_context():
           account = Account(name="", email="valid@example.com")
           with pytest.raises(DataValidationError) as excinfo:
               account.validate()
           assert "nombre no puede estar vacío" in str(excinfo.value)

   def test_validate_invalid_email(self):
       """Prueba la validación con email inválido"""
       with app.app_context():
           account = Account(name="Invalid", email="invalid-email")
           with pytest.raises(DataValidationError) as excinfo:
               account.validate()
           assert "email no es válido" in str(excinfo.value)
   ```
