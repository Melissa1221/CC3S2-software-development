"""
Colección de fakes/mocks que cumplen las interfaces de producción (LSP).
"""
from decimal import Decimal
from devops_testing.models import User
import time

class DummyGateway:
    def __init__(self, succeed: bool = True):
        self._succeed = succeed
        self.calls: list[tuple[Decimal, str, str]] = []

    def charge(self, amount: Decimal, currency: str, user: User):
        self.calls.append((amount, currency, user.id))
        return self._succeed

class RealGateway:
    """Gateway que simula latencia como si fuera un servicio real externo."""
    def __init__(self, latency: float = 0.5, succeed: bool = True):
        self._latency = latency
        self._succeed = succeed
        self.calls: list[tuple[Decimal, str, str]] = []
    
    def charge(self, amount: Decimal, currency: str, user: User):
        time.sleep(self._latency)  # Simula latencia de red
        self.calls.append((amount, currency, user.id))
        return self._succeed
