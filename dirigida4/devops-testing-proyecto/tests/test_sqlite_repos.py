"""Pruebas para los repositorios SQLite."""

import pytest
from decimal import Decimal
from devops_testing.models import User, Payment

# Tests de SQLiteUserRepository
def test_sqlite_user_repo_add_get(sqlite_user_repo):
    """Prueba añadir y obtener usuarios en SQLite."""
    user = User(username="test_user", email="test@example.com")
    sqlite_user_repo.add(user)
    
    # Obtener el usuario
    retrieved = sqlite_user_repo.get("test_user")
    
    # Verificar que es el mismo
    assert retrieved.id == user.id
    assert retrieved.username == user.username
    assert retrieved.email == user.email

def test_sqlite_user_repo_duplicate(sqlite_user_repo):
    """Prueba que no se pueden añadir usuarios duplicados."""
    user = User(username="duplicate", email="duplicate@example.com")
    sqlite_user_repo.add(user)
    
    # Intentar añadir de nuevo
    with pytest.raises(KeyError):
        sqlite_user_repo.add(User(username="duplicate", email="another@example.com"))

def test_sqlite_user_repo_nonexistent(sqlite_user_repo):
    """Prueba que se lanza KeyError para usuarios inexistentes."""
    with pytest.raises(KeyError):
        sqlite_user_repo.get("nonexistent")

# Tests de SQLitePaymentRepository
def test_sqlite_payment_repo_add_list(sqlite_payment_repo, sqlite_test_user):
    """Prueba añadir y listar pagos en SQLite."""
    payment = Payment(
        amount=Decimal("100.50"),
        currency="USD",
        user_id=sqlite_test_user.id
    )
    sqlite_payment_repo.add(payment)
    
    # Listar pagos del usuario
    payments = sqlite_payment_repo.list_by_user(sqlite_test_user.id)
    
    # Verificar que hay un solo pago y es el correcto
    assert len(payments) == 1
    assert payments[0].id == payment.id
    assert payments[0].amount == payment.amount
    assert payments[0].currency == payment.currency
    assert payments[0].user_id == sqlite_test_user.id

def test_sqlite_payment_repo_multiple_payments(sqlite_payment_repo, sqlite_test_user):
    """Prueba añadir múltiples pagos al mismo usuario."""
    # Crear varios pagos
    payment1 = Payment(amount=Decimal("10"), currency="USD", user_id=sqlite_test_user.id)
    payment2 = Payment(amount=Decimal("20"), currency="USD", user_id=sqlite_test_user.id)
    payment3 = Payment(amount=Decimal("30"), currency="EUR", user_id=sqlite_test_user.id)
    
    # Añadir pagos
    sqlite_payment_repo.add(payment1)
    sqlite_payment_repo.add(payment2)
    sqlite_payment_repo.add(payment3)
    
    # Listar pagos
    payments = sqlite_payment_repo.list_by_user(sqlite_test_user.id)
    
    # Verificar cantidad
    assert len(payments) == 3
    
    # Verificar que están todos
    payment_ids = {p.id for p in payments}
    assert payment1.id in payment_ids
    assert payment2.id in payment_ids
    assert payment3.id in payment_ids
    
    # Verificar suma total
    total = sum(p.amount for p in payments)
    assert total == Decimal("60")

# Tests parametrizados que funcionan con ambos tipos de repositorios
@pytest.mark.parametrize(
    "user_repo_fixture,payment_repo_fixture,test_user_fixture",
    [
        ("user_repo", "payment_repo", "test_user"),  # In-Memory
        ("sqlite_user_repo", "sqlite_payment_repo", "sqlite_test_user"),  # SQLite
    ],
    indirect=True
)
def test_repo_agnostic_payment_flow(user_repo_fixture, payment_repo_fixture, 
                                   test_user_fixture, dummy_gateway):
    """
    Test parametrizado que demuestra que PaymentService funciona
    con cualquier implementación de repositorio.
    """
    # Crear servicio
    service = PaymentService(
        dummy_gateway,
        payment_repo_fixture,
        user_repo_fixture
    )
    
    # Procesar pago
    payment_id = service.process_payment(
        test_user_fixture.username,
        Decimal("75.99"),
        "USD"
    )
    
    # Verificar que se creó
    assert payment_id
    
    # Verificar que se puede recuperar
    payments = payment_repo_fixture.list_by_user(test_user_fixture.id)
    assert len(payments) == 1
    assert payments[0].id == payment_id 