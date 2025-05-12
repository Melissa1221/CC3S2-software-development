# tests/conftest.py
import pytest
import os
import threading
import socket
import time
import uvicorn
from unittest.mock import Mock
from devops_testing.models import User
from devops_testing.repositories import (
    InMemoryUserRepository,
    InMemoryPaymentRepository,
)
from devops_testing.persistence.sqlite_repo import (
    SQLiteUserRepository,
    SQLitePaymentRepository,
)
from devops_testing.services import PaymentService
from devops_testing.config import Config
from tests.fakes import DummyGateway, RealGateway
from external_gateway.client import HttpPaymentGateway

#  Fixtures de repositorios y entidades básicas

@pytest.fixture
def user_repo():
    """Repositorio de usuarios (nuevo en cada test)."""
    return InMemoryUserRepository()

@pytest.fixture
def payment_repo():
    """Repositorio de pagos (nuevo en cada test)."""
    return InMemoryPaymentRepository()

@pytest.fixture
def test_user(user_repo):
    """Usuario de prueba inyectado en varios escenarios."""
    user = User(username="kapumota", email="kapumota@example.com")
    user_repo.add(user)
    return user

#  Fakes y servicios
@pytest.fixture
def fake_gateway():
    """Fake simple con Mock de unittest (éxito por defecto)."""
    gw = Mock()
    gw.charge.return_value = True
    return gw

@pytest.fixture
def conditional_gateway():
    """
    Gateway condicional por entorno. Si USE_REAL_GATEWAY está activo,
    usa el gateway real con latencia. Caso contrario usa DummyGateway.
    """
    use_real = os.environ.get("USE_REAL_GATEWAY", "").lower() in ("1", "true", "yes")
    
    if use_real:
        # Marcamos estos tests como lentos
        pytest.mark.slow
        return RealGateway(latency=0.5)
    else:
        return DummyGateway()

@pytest.fixture
def payment_service(conditional_gateway, payment_repo, user_repo):
    """
    Servicio principal construido con DI a partir de otros fixtures.
    Representa la variante 'interface-driven' + 'constructor standard'.
    """
    return PaymentService(conditional_gateway, payment_repo, user_repo)

# Versión original
@pytest.fixture
def original_payment_service(fake_gateway, payment_repo, user_repo):
    """
    Servicio original construido con DI a partir de otros fixtures.
    """
    return PaymentService(fake_gateway, payment_repo, user_repo)

#  Variantes de DI

@pytest.fixture
def payment_service_factory():
    """
    Constructor-like: devuelve una función que fabrica PaymentService
    con un gateway fake parametrizable (Mock) y repos in-memory frescos.
    """
    def _make(gateway_success: bool = True):
        gw = Mock()
        gw.charge.return_value = gateway_success

        user_repo_local = InMemoryUserRepository()
        pay_repo_local = InMemoryPaymentRepository()

        service = PaymentService(gw, pay_repo_local, user_repo_local)
        return service, user_repo_local  # repo para poblar en el test

    return _make


@pytest.fixture
def dummy_gateway():
    """
    Interface-driven fake importado de tests/fakes.py
    Cumple estrictamente la interfaz PaymentGateway.
    """
    return DummyGateway()

#  Fixture-as-config (Config global inyectable)

@pytest.fixture(scope="session")
def app_config():
    """
    Config inmutable disponible en toda la sesión; ejemplo fixture-as-config.
    """
    return Config(currency_default="EUR", retries=1)

# Nuevo fixture para el servidor FastAPI
@pytest.fixture(scope="session")
def free_port():
    """Encuentra un puerto libre para el servidor FastAPI."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]

class UvicornTestServer(uvicorn.Server):
    """Wrapper para servidor Uvicorn con métodos para iniciar/detener."""
    def install_signal_handlers(self):
        # Desactivamos para evitar conflictos con pytest
        pass
    
    @property
    def should_exit(self):
        return self._should_exit
    
    @should_exit.setter
    def should_exit(self, value):
        self._should_exit = value

@pytest.fixture(scope="session")
def gateway_server(free_port):
    """
    Levanta el servidor FastAPI en un thread separado.
    Retorna la URL base del servidor.
    """
    from external_gateway.app import app
    
    config = uvicorn.Config(app, host="127.0.0.1", port=free_port, log_level="error")
    server = UvicornTestServer(config=config)
    
    thread = threading.Thread(target=server.run)
    thread.start()
    
    # Esperar a que el servidor esté listo
    time.sleep(1)
    
    # Retornar URL base para el cliente
    base_url = f"http://127.0.0.1:{free_port}"
    
    yield base_url
    
    # Limpiar al finalizar
    server.should_exit = True
    thread.join()

@pytest.fixture
def http_gateway(gateway_server):
    """Cliente HTTP para el gateway simulado."""
    return HttpPaymentGateway(base_url=gateway_server)

@pytest.fixture
def http_payment_service(http_gateway, payment_repo, user_repo):
    """Servicio de pagos que usa el gateway HTTP."""
    return PaymentService(http_gateway, payment_repo, user_repo)

# Fixtures para SQLite
@pytest.fixture
def sqlite_db_path(tmp_path):
    """
    Genera una ruta temporal para la base de datos SQLite.
    """
    return str(tmp_path / "test.db")

@pytest.fixture
def sqlite_user_repo(sqlite_db_path):
    """Repositorio de usuarios SQLite."""
    return SQLiteUserRepository(sqlite_db_path)

@pytest.fixture
def sqlite_payment_repo(sqlite_db_path):
    """Repositorio de pagos SQLite."""
    return SQLitePaymentRepository(sqlite_db_path)

@pytest.fixture
def sqlite_test_user(sqlite_user_repo):
    """Usuario de prueba en la base de datos SQLite."""
    user = User(username="sqlite_user", email="sqlite@example.com")
    sqlite_user_repo.add(user)
    return user

@pytest.fixture
def sqlite_payment_service(dummy_gateway, sqlite_payment_repo, sqlite_user_repo):
    """Servicio de pagos que usa repositorios SQLite."""
    return PaymentService(
        dummy_gateway, sqlite_payment_repo, sqlite_user_repo
    )
