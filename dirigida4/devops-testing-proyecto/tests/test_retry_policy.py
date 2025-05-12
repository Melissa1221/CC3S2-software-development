"""Tests para la política de reintentos."""

import pytest
import time
from decimal import Decimal
from unittest.mock import Mock, call
from devops_testing.retry import RetryPolicy
from devops_testing.models import User
from devops_testing.config import Config
from devops_testing.services import PaymentService

@pytest.mark.parametrize("retries,fail_times", [
    (1, 0),  # Success on first try (no failures)
    (2, 1),  # Success on second try (1 failure)
    (3, 2),  # Success on third try (2 failures)
])
def test_retry_policy_execution(retries, fail_times):
    """Prueba parametrizada que verifica que la política reintenta correctamente."""
    retry_policy = RetryPolicy(max_retries=retries, delay=0.01)
    
    # Contador de llamadas
    call_count = 0
    
    # Función que fallará un número específico de veces
    def operation():
        nonlocal call_count
        call_count += 1
        if call_count <= fail_times:
            return False  # Falla las primeras n veces
        return True  # Luego tiene éxito
    
    start_time = time.time()
    result = retry_policy.execute(operation)
    execution_time = time.time() - start_time
    
    assert result is True
    assert call_count == fail_times + 1  # Fallamos n veces, luego éxito
    assert execution_time < 0.2  # No debería exceder el tiempo límite

def test_retry_in_payment_service():
    """Prueba que PaymentService usa la política de reintentos."""
    # Configuramos para 2 reintentos
    config = Config(retries=2)
    
    # Mock del gateway que falla en el primer intento
    gateway = Mock()
    gateway.charge.side_effect = [False, True]  # Falla, luego éxito
    
    # Repos y usuario de prueba
    user_repo = Mock()
    test_user = User(username="test", email="test@example.com")
    user_repo.get.return_value = test_user
    
    payment_repo = Mock()
    
    # Creamos el servicio con la configuración
    service = PaymentService(gateway, payment_repo, user_repo, config=config)
    
    # Procesamos el pago
    service.process_payment("test", Decimal("50"), "USD")
    
    # Verificamos que el método charge se llamó exactamente 2 veces
    assert gateway.charge.call_count == 2
    # Verificamos que se añadió exactamente un pago al repo
    assert payment_repo.add.call_count == 1

def test_all_retries_fail():
    """Prueba el caso donde todos los reintentos fallan."""
    retry_policy = RetryPolicy(max_retries=3, delay=0.01)
    
    # Función que siempre falla
    mock_operation = Mock(return_value=False)
    
    with pytest.raises(RuntimeError):
        retry_policy.execute(mock_operation)
    
    assert mock_operation.call_count == 3  # Se intentó exactamente 3 veces 