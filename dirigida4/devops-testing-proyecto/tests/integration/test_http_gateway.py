"""Pruebas de integración para el gateway HTTP."""

import pytest
from decimal import Decimal
from devops_testing.models import User

@pytest.mark.http
def test_http_gateway_success(http_gateway, test_user):
    """Verifica que el gateway HTTP funciona correctamente en caso de éxito."""
    # Configuramos tasa de éxito al 100%
    http_gateway.success_rate = 1.0
    
    # Realizamos un cargo
    result = http_gateway.charge(Decimal("100"), "USD", test_user)
    
    # Verificamos resultado
    assert result is True
    assert len(http_gateway.calls) == 1
    assert http_gateway.calls[0][0] == Decimal("100")
    assert http_gateway.calls[0][1] == "USD"
    assert http_gateway.calls[0][2] == test_user.id

@pytest.mark.http
def test_http_gateway_failure(http_gateway, test_user):
    """Verifica que el gateway HTTP maneja correctamente los fallos."""
    # Configuramos tasa de éxito al 0%
    http_gateway.success_rate = 0.0
    
    # Realizamos un cargo
    result = http_gateway.charge(Decimal("100"), "USD", test_user)
    
    # Verificamos resultado
    assert result is False

@pytest.mark.http
def test_http_payment_service_integration(http_payment_service, test_user, payment_repo):
    """
    Prueba de integración end-to-end que usa el servicio de pagos
    con el gateway HTTP real.
    """
    # Realizamos un pago
    payment_id = http_payment_service.process_payment(
        test_user.username, Decimal("50"), "USD"
    )
    
    # Verificamos que se creó el pago
    assert payment_id
    
    # Verificamos que se guardó en el repositorio
    payments = payment_repo.list_by_user(test_user.id)
    assert len(payments) == 1
    assert payments[0].id == payment_id 