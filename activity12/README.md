# Actividad: Revisión de fixtures en pruebas

Esta actividad se centra en aprender a utilizar los diferentes fixtures de prueba disponibles en el paquete `pytest` para establecer y limpiar el estado antes y después de las pruebas.

## Paso 1: Inicializar la base de datos

En este paso, configuré un fixture de prueba para conectar y desconectar de la base de datos. Esto se realiza una vez antes de todas las pruebas y una vez después de todas las pruebas.

Para implementar esto, utilicé un fixture a nivel de módulo con `scope="module"` y `autouse=True` para que se ejecute automáticamente:

```python
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    # Se ejecuta antes de todas las pruebas
    with app.app_context():
        db.create_all()
        yield
        # Se ejecuta después de todas las pruebas
        db.session.close()
```

Este fixture crea todas las tablas en la base de datos antes de ejecutar las pruebas y cierra la conexión después de que todas las pruebas han finalizado.

![](https://i.imgur.com/W03kkdd.png)

## Paso 2: Cargar datos de prueba

En este paso, implementé la carga de datos de prueba desde un archivo JSON. Esto solo necesita hacerse una vez antes de todas las pruebas de la clase.

Agregué el método `setup_class` que se ejecuta una vez antes de todas las pruebas de la clase:

```python
@classmethod
def setup_class(cls):
    """Conectar y cargar los datos necesarios para las pruebas"""
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)
    print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")
```

Este método carga los datos del archivo `account_data.json` en una variable global `ACCOUNT_DATA` que será utilizada por todas las pruebas de la clase.

![](https://i.imgur.com/W03kkdd.png)

## Paso 3: Escribir un caso de prueba para crear una cuenta

Después de configurar los fixtures, implementé un caso de prueba para crear una sola cuenta utilizando los datos cargados en el paso anterior:

```python
def test_create_an_account(self):
    """Probar la creación de una sola cuenta"""
    with app.app_context():
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1
```

Este test toma el primer registro de los datos de prueba, crea una instancia de `Account` con esos datos, la guarda en la base de datos y verifica que exista exactamente una cuenta en la base de datos.

![](https://i.imgur.com/XBuEFHA.png)

## Paso 4: Escribir un caso de prueba para crear todas las cuentas

A continuación, implementé un caso de prueba que crea todas las cuentas definidas en los datos de prueba:

```python
def test_create_all_accounts(self):
    """Probar la creación de múltiples cuentas"""
    with app.app_context():
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        assert len(Account.all()) == len(ACCOUNT_DATA)
```

Este test itera a través de todos los registros en los datos de prueba, crea una instancia de `Account` para cada uno y verifica que el número de cuentas en la base de datos sea igual al número de registros en los datos de prueba.

![](https://i.imgur.com/cvMfxB5.png)

## Paso 5: Limpiar las tablas antes y después de cada prueba

Finalmente, implementé los métodos `setup_method` y `teardown_method` para limpiar la base de datos antes y después de cada prueba:

```python
def setup_method(self):
    """Truncar las tablas antes de cada prueba"""
    with app.app_context():
        db.session.query(Account).delete()
        db.session.commit()

def teardown_method(self):
    """Eliminar la sesión después de cada prueba"""
    with app.app_context():
        db.session.remove()
```

El método `setup_method` elimina todos los registros de la tabla `Account` antes de cada prueba, mientras que `teardown_method` elimina la sesión de la base de datos después de cada prueba. Esto garantiza que cada prueba se ejecute en un entorno limpio y predecible.


