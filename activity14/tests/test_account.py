import pytest
from models import db
from models.account import Account, DataValidationError
from factories import AccountFactory
from flask import Flask

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

class TestAccountModel:
    """Test Cases for Account Model"""

    def test_crear_todas_las_cuentas(self, app):
        """Prueba la creación de múltiples Cuentas"""
        with app.app_context():
            for _ in range(10):
                account = AccountFactory()
                account.create()
            assert len(Account.all()) == 10

    def test_crear_una_cuenta(self, app):
        """Prueba la creación de una Cuenta"""
        with app.app_context():
            account = AccountFactory()
            account.create()
            assert len(Account.all()) == 1

    def test_repr(self, app):
        """Prueba la representación como string"""
        with app.app_context():
            account = AccountFactory()
            assert account.name in repr(account)

    def test_to_dict(self):
        """Prueba la serialización de una cuenta a un diccionario"""
        account = AccountFactory()
        result = account.to_dict()
        assert account.name == result["name"]
        assert account.email == result["email"]
        assert account.phone_number == result["phone_number"]
        assert account.disabled == result["disabled"]
        assert account.date_joined == result["date_joined"]

    def test_from_dict(self):
        """Prueba la deserialización de una cuenta desde un diccionario"""
        data = AccountFactory().to_dict()
        account = Account()
        account.from_dict(data)
        assert account.name == data["name"]
        assert account.email == data["email"]
        assert account.phone_number == data["phone_number"]
        assert account.disabled == data["disabled"]

    def test_actualizar_una_cuenta(self, app):
        """Prueba la actualización de una Cuenta"""
        with app.app_context():
            account = AccountFactory()
            account.create()
            assert account.id is not None
            account.name = "Rumpelstiltskin"
            account.update()
            found = Account.find(account.id)
            assert found.name == account.name

    def test_id_invalido_al_actualizar(self):
        """Prueba la actualización con un ID inválido"""
        account = AccountFactory()
        account.id = None
        with pytest.raises(DataValidationError):
            account.update()

    def test_eliminar_una_cuenta(self, app):
        """Prueba la eliminación de una Cuenta"""
        with app.app_context():
            account = AccountFactory()
            account.create()
            assert len(Account.all()) == 1
            account.delete()
            assert len(Account.all()) == 0