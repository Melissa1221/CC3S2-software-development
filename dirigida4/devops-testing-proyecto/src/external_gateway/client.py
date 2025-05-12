"""Cliente HTTP para la pasarela de pagos externa."""

import requests
from decimal import Decimal
from devops_testing.models import User

class HttpPaymentGateway:
    """
    Gateway que realiza llamadas HTTP a un servicio externo.
    Implementa la misma interfaz que los otros gateways (PaymentGateway).
    """
    
    def __init__(self, base_url: str, success_rate: float = 1.0):
        """
        Inicializa el gateway HTTP.
        
        Args:
            base_url: URL base del servicio (ej: "http://localhost:8000")
            success_rate: Tasa de éxito para pruebas (0.0-1.0)
        """
        self.base_url = base_url.rstrip('/')
        self.success_rate = success_rate
        self.calls = []  # Para compatibilidad con las pruebas
    
    def charge(self, amount: Decimal, currency: str, user: User) -> bool:
        """
        Realiza un cargo a través del servicio HTTP.
        
        Args:
            amount: Monto a cargar
            currency: Moneda (USD, EUR, etc.)
            user: Usuario al que se le hará el cargo
            
        Returns:
            True si el cargo fue exitoso, False en caso contrario
        """
        # Registramos la llamada para compatibilidad con las pruebas
        self.calls.append((amount, currency, user.id))
        
        # Preparamos los datos para la llamada
        payload = {
            "amount": float(amount),  # Convertimos a float para JSON
            "currency": currency,
            "user_id": user.id,
            "success_rate": self.success_rate
        }
        
        try:
            # Realizamos la llamada HTTP
            response = requests.post(
                f"{self.base_url}/charge",
                json=payload,
                timeout=5  # Timeout de 5 segundos
            )
            
            # Validamos la respuesta
            if response.status_code == 200:
                data = response.json()
                return data.get("success", False)
            
            # Si no es 200, fallamos
            return False
            
        except requests.RequestException:
            # Capturamos cualquier error de red
            return False 