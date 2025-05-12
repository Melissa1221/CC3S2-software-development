"""Policy de reintentos para servicios."""

import time
from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar('T')

class RetryPolicy:
    """Política que permite reintentar operaciones que pueden fallar transitoriamente."""
    
    def __init__(self, max_retries: int = 3, delay: float = 0.01):
        """
        Inicializa la política de reintentos.
        
        Args:
            max_retries: Número máximo de intentos (incluyendo el primero)
            delay: Tiempo de espera en segundos entre intentos
        """
        self.max_retries = max_retries
        self.delay = delay
        
    def execute(self, operation: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        Ejecuta una operación con reintentos según la política configurada.
        
        Args:
            operation: Función a ejecutar
            *args: Argumentos posicionales para la operación
            **kwargs: Argumentos por nombre para la operación
            
        Returns:
            El resultado de la operación si tiene éxito
            
        Raises:
            Exception: La última excepción capturada si todos los intentos fallan
            o el valor de retorno evaluado a False
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                result = operation(*args, **kwargs)
                if result:  # Si la operación devuelve algo que evalúa a True
                    return result
            except Exception as e:
                last_error = e
                
            # No esperamos después del último intento
            if attempt < self.max_retries - 1:
                time.sleep(self.delay)
        
        # Si llegamos aquí, todos los intentos fallaron
        if last_error:
            raise last_error
        else:
            raise RuntimeError("La operación falló después de múltiples intentos") 