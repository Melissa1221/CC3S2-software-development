"""Property-based tests usando Hypothesis para PaymentService."""

import pytest
from decimal import Decimal
from hypothesis import given, strategies as st
from devops_testing.models import User
from devops_testing.repositories import InMemoryPaymentRepository, InMemoryUserRepository
from devops_testing.services import PaymentService
from tests.fakes import DummyGateway

@pytest.fixture
def property_service():
    """Fixture específico para property testing con componentes limpios."""
    gateway = DummyGateway(succeed=True)
    payment_repo = InMemoryPaymentRepository()
    user_repo = InMemoryUserRepository()
    
    # Crear un usuario de prueba
    user = User(username="property_user", email="property@example.com")
    user_repo.add(user)
    
    return PaymentService(gateway, payment_repo, user_repo), user, payment_repo

@given(amount=st.decimals(min_value="0.01", max_value="1000000.00"))
def test_payment_persists_with_random_amounts(property_service):
    """
    Verifica que cualquier monto positivo válido genere un pago persistido.
    Usamos la estrategia decimals para generar montos aleatorios.
    """
    service, user, payment_repo = property_service
    
    # Procesamos el pago con el monto generado por Hypothesis
    payment_id = service.process_payment(user.username, amount, "USD")
    
    # Verificamos que se generó un ID
    assert payment_id
    
    # Verificamos que el pago se persistió en el repositorio
    payments = payment_repo.list_by_user(user.id)
    assert len(payments) == 1
    assert payments[0].id == payment_id
    assert payments[0].amount == amount
    assert payments[0].currency == "USD"

@given(
    amounts=st.lists(
        st.decimals(min_value="0.01", max_value="1000.00"),
        min_size=1,
        max_size=10
    )
)
def test_multiple_payments_persist_correctly(property_service):
    """
    Verifica que múltiples pagos con montos aleatorios se persistan correctamente.
    """
    service, user, payment_repo = property_service
    
    payment_ids = []
    # Procesamos múltiples pagos
    for amount in amounts:
        payment_id = service.process_payment(user.username, amount, "USD")
        payment_ids.append(payment_id)
    
    # Verificamos que todos los pagos se persistieron
    payments = payment_repo.list_by_user(user.id)
    assert len(payments) == len(amounts)
    
    # Verificamos que las sumas coincidan
    total_processed = sum(amounts)
    total_stored = sum(payment.amount for payment in payments)
    assert total_processed == total_stored 