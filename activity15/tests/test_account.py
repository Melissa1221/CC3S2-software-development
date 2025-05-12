import json
import pytest
import sys
import os

# Establecer variable de entorno para usar base de datos en memoria
os.environ['TESTING'] = '1'

# Ajustamos el path para que 'models' sea importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db, app
from models.account import Account, DataValidationError

# Variable global para almacenar los datos del fixture
ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    with app.app_context():
        db.create_all()   # Crea las tablas según los modelos
        yield
        # Se ejecuta después de todas las pruebas
        db.session.close()


class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos (si fuera necesario limpiar algo adicional)"""
        pass

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        with app.app_context():
            db.session.query(Account).delete()
            db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        with app.app_context():
            db.session.remove()

    ######################################################################
    # Casos de prueba básicos
    ######################################################################

    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        with app.app_context():
            data = ACCOUNT_DATA[0]  # obtener la primera cuenta
            account = Account(**data)
            account.create()
            assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        with app.app_context():
            for data in ACCOUNT_DATA:
                account = Account(**data)
                account.create()
            assert len(Account.all()) == len(ACCOUNT_DATA)

    ######################################################################
    #  Nuevos casos de prueba para cobertura
    ######################################################################

    def test_to_dict(self):
        """Probar la serialización de Account a diccionario."""
        with app.app_context():
            data = ACCOUNT_DATA[0]
            account = Account(**data)
            account.create()  # Se crea en la BD para tener un 'id'

            result = account.to_dict()
            assert isinstance(result, dict)
            assert result["name"] == data["name"]
            assert result["email"] == data["email"]
            # Chequear que 'id' y 'date_joined' existan en el dict
            assert "id" in result
            assert "date_joined" in result

    def test_from_dict(self):
        """Probar la deserialización de un diccionario a una instancia de Account."""
        with app.app_context():
            data = {
                "name": "Nuevo Usuario",
                "email": "nuevo@example.com",
                "phone_number": "1234567890",
                "disabled": True
            }
            account = Account()  # Instancia vacía
            account.from_dict(data)

            # Verificamos que los atributos hayan sido asignados
            assert account.name == data["name"]
            assert account.email == data["email"]
            assert account.phone_number == data["phone_number"]
            assert account.disabled == data["disabled"]

    def test_update_account_success(self):
        """Probar actualizar una cuenta existente."""
        with app.app_context():
            data = ACCOUNT_DATA[0]
            account = Account(**data)
            account.create()  # al crear se asigna un ID en la BD

            # Cambiamos un atributo
            account.name = "Nombre Actualizado"
            account.update()  # Debe funcionar sin error

            # Recuperamos de la BD para verificar cambios
            updated_account = Account.find(account.id)
            assert updated_account.name == "Nombre Actualizado"

    def test_update_account_no_id_error(self):
        """Probar que update lance DataValidationError si no hay ID."""
        with app.app_context():
            # Creamos una cuenta *sin* guardarla en la BD
            account = Account(name="Usuario Sin ID", email="sinid@example.com")

            # update() debería lanzar excepción
            with pytest.raises(DataValidationError) as excinfo:
                account.update()
            assert "Actualización llamada con campo ID vacío" in str(excinfo.value)

    def test_delete_account(self):
        """Probar la eliminación de una cuenta existente."""
        with app.app_context():
            data = ACCOUNT_DATA[0]
            account = Account(**data)
            account.create()

            assert len(Account.all()) == 1  # Comprobación preliminar
            account.delete()
            assert len(Account.all()) == 0  # Debe haberse eliminado

    def test_find_account_exists(self):
        """Probar que find retorne la cuenta correcta si existe."""
        with app.app_context():
            data = ACCOUNT_DATA[0]
            account = Account(**data)
            account.create()

            found_account = Account.find(account.id)
            assert found_account is not None
            assert found_account.id == account.id
            assert found_account.name == account.name

    def test_find_account_not_exists(self):
        """Probar que find devuelva None cuando la cuenta no existe."""
        with app.app_context():
            found_account = Account.find(999999)  # ID que no existe
            assert found_account is None

    # << NUEVO TEST PARA __repr__ >>
    def test_repr_account(self):
        """Probar la salida del método __repr__ de Account."""
        with app.app_context():
            data = ACCOUNT_DATA[0]
            account = Account(**data)
            # No es necesario crear en BD para probar __repr__ (pero se puede si se desea)
            representation = repr(account)
            expected = f"<Account '{data['name']}'>"
            assert representation == expected
            
    # Pruebas adicionales para casos límite y comportamientos específicos
    def test_account_has_id_after_create(self):
        """Verifica que se asigne un ID después de crear una cuenta"""
        with app.app_context():
            account = Account(name="Test ID", email="testid@example.com")
            assert account.id is None  # No tiene ID antes de crear
            account.create()
            assert account.id is not None  # Debe tener ID después de crear

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
            
    def test_all_empty_database(self):
        """Prueba el método all cuando la base de datos está vacía"""
        with app.app_context():
            # Asegurarse de que la base de datos esté vacía
            db.session.query(Account).delete()
            db.session.commit()
            
            # Verificar que all() devuelve una lista vacía
            accounts = Account.all()
            assert isinstance(accounts, list)
            assert len(accounts) == 0
            
    def test_from_dict_incomplete(self):
        """Prueba from_dict con un diccionario incompleto"""
        with app.app_context():
            account = Account()
            # Diccionario con solo algunos campos
            data = {"name": "Incompleto"}
            account.from_dict(data)
            
            # Verificar que solo se actualizó el nombre
            assert account.name == "Incompleto"
            assert account.email is None  # No debería tener email
            
    # Pruebas para el nuevo método de validación
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
            
    def test_create_with_invalid_data_fails(self):
        """Prueba que create valida los datos antes de guardar"""
        with app.app_context():
            account = Account(name="", email="invalid")
            with pytest.raises(DataValidationError):
                account.create()
                
    def test_update_with_invalid_data_fails(self):
        """Prueba que update valida los datos antes de actualizar"""
        with app.app_context():
            # Primero crear una cuenta válida
            account = Account(name="Valid Update", email="valid@update.com")
            account.create()
            
            # Luego intentar actualizarla con datos inválidos
            account.email = "invalid"
            with pytest.raises(DataValidationError):
                account.update()
