"""Servicios de dominio.
SRP: cada servicio aborda un caso de uso. DIP: dependen de repositorios abstractos.
"""

from decimal import Decimal
from typing import Protocol, Optional
from .models import User, Payment, validate_amount
from .config import Config
from .retry import RetryPolicy

class PaymentGateway(Protocol):
    """Abstracción de pasarela de pagos externa."""
    def charge(self, amount: Decimal, currency: str, user: User) -> bool: ...

class PaymentService:
    """Orquesta la creación de un pago."""
    def __init__(self, gateway: PaymentGateway, payment_repo, user_repo,
                config: Optional[Config] = None, logger=None):
        self._gw = gateway
        self._pay_repo = payment_repo
        self._user_repo = user_repo
        self._cfg = config or Config()
        self._logger = logger
        self._retry_policy = RetryPolicy(max_retries=self._cfg.retries)

    def process_payment(self, username: str, amount: Decimal, currency: str) -> str:
        user = self._user_repo.get(username)
        validate_amount(amount)
        
        if self._logger:
            self._logger.info(f"start-payment: user={username} amount={amount} currency={currency}")
        
        # Usamos la política de reintentos para el cargo
        success = self._retry_policy.execute(
            self._gw.charge, amount, currency, user
        )
        
        if success:
            payment = Payment(amount=amount, currency=currency, user_id=user.id)
            self._pay_repo.add(payment)
            
            if self._logger:
                self._logger.info(f"payment-ok: id={payment.id}")
                
            return payment.id
        
        raise RuntimeError("Fallo el cobro")
