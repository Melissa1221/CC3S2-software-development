"""Tests that verify domain invariants."""

import pytest
from decimal import Decimal
from devops_testing.models import User, Payment
from devops_testing.repositories import InMemoryPaymentRepository

@pytest.mark.contract
def test_payment_requires_valid_user(payment_service, test_user):
    """Verifica que no se puede procesar un pago sin un usuario válido."""
    # Intento de pago con un usuario inexistente
    with pytest.raises(KeyError):
        payment_service.process_payment("usuario_inexistente", Decimal("50"), "USD")

@pytest.mark.contract
def test_payment_requires_positive_amount(payment_service, test_user):
    """Verifica que el monto del pago debe ser positivo."""
    # Intento de pago con monto negativo
    with pytest.raises(ValueError):
        payment_service.process_payment(test_user.username, Decimal("-10"), "USD")

# Este test no está marcado como contrato, no debería aparecer con -m contract
def test_normal_payment_flow(payment_service, test_user):
    """Flujo normal de pago que no verifica invariantes de dominio."""
    payment_id = payment_service.process_payment(test_user.username, Decimal("30"), "USD")
    assert payment_id 