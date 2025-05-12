"""Tests that demonstrate the conditional gateway fixture."""

import pytest
from decimal import Decimal
import time

@pytest.mark.slow
def test_payment_with_conditional_gateway(payment_service, test_user):
    """
    Este test usará el RealGateway con latencia cuando se ejecute con 
    USE_REAL_GATEWAY=1, o el DummyGateway cuando se ejecute normalmente.
    """
    start_time = time.time()
    
    payment_id = payment_service.process_payment(
        test_user.username, Decimal('100'), "USD"
    )
    
    execution_time = time.time() - start_time
    assert payment_id
    
    # No validamos tiempo exacto para evitar falsos positivos,
    # pero podemos ver en los logs si tomó tiempo o no. 