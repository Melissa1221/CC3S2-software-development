# Actividad: Factory y Fakes

Esta actividad se centra en el uso de FactoryBoy y Faker para generar datos de prueba realistas y dinámicos. El objetivo es reemplazar datos estáticos con factories que puedan generar datos de prueba ilimitados.

## Paso 1: Ejecutar pytest para verificar el estado inicial

Primero verifico que todas las pruebas estén pasando antes de realizar cualquier cambio. Ejecuto:

```bash
pytest --cov=models
```

Sin embargo, encontré un error: "Working outside of application context". Este error ocurre porque Flask-SQLAlchemy necesita un contexto de aplicación para acceder a la base de datos.

## Paso 2: Instalar las dependencias necesarias

Necesitamos instalar las siguientes dependencias:

```bash
pip install flask-sqlalchemy factory-boy faker pytest pytest-cov
```

## Paso 3: Arreglar el contexto de aplicación Flask

Para solucionar el error del contexto de aplicación, modificamos el archivo `tests/test_account.py` agregando fixtures de pytest para crear y gestionar la aplicación Flask:

```python
@pytest.fixture(scope="session")
def app():
    """Crea una aplicación Flask para las pruebas"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function", autouse=True)
def session(app):
    """Crea una sesión nueva para cada prueba"""
    with app.app_context():
        db.session.query(Account).delete()
        db.session.commit()
        yield db.session
        db.session.close()
```

Luego, modificamos cada método de prueba que interactúa con la base de datos para usar el contexto de aplicación:

```python
def test_crear_una_cuenta(self, app):
    """Prueba la creación de una Cuenta"""
    with app.app_context():
        account = AccountFactory()
        account.create()
        assert len(Account.all()) == 1
```

## Paso 4: Crear una clase AccountFactory

Creamos el archivo `tests/factories.py` e implementamos la clase AccountFactory usando FactoryBoy con proveedores Faker y atributos Fuzzy:

```python
import factory
from datetime import date
from factory.fuzzy import FuzzyChoice, FuzzyDate
from models.account import Account

class AccountFactory(factory.Factory):
    """Crea cuentas falsas"""

    class Meta:
        model = Account

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    disabled = FuzzyChoice(choices=[True, False])
    date_joined = FuzzyDate(date(2005, 7, 6))
```

Esta factory genera datos falsos para cada atributo de manera realista:
- id: secuencia incremental
- name: nombres aleatorios
- email: correos electrónicos aleatorios
- phone_number: números telefónicos aleatorios
- disabled: valor booleano aleatorio
- date_joined: fecha aleatoria a partir de 2005-07-06

## Paso 5: Actualizar las pruebas para usar AccountFactory

Modificamos todos los métodos de prueba para usar AccountFactory en lugar de datos estáticos. Por ejemplo:

```python
def test_to_dict(self):
    """Prueba la serialización de una cuenta a un diccionario"""
    account = AccountFactory()
    result = account.to_dict()
    assert account.name == result["name"]
    assert account.email == result["email"]
    assert account.phone_number == result["phone_number"]
    assert account.disabled == result["disabled"]
    assert account.date_joined == result["date_joined"]
```

## Paso 6: Ejecutar las pruebas

Una vez implementados todos los cambios, ejecutamos las pruebas de nuevo:

```bash
pytest --cov=models
```

Ahora todas las pruebas pasan satisfactoriamente con una cobertura del 100%.

![](https://i.imgur.com/7FduJyg.png)
