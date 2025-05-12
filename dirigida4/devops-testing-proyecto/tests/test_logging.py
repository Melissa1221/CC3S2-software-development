"""Tests para logging configurable en PaymentService."""

import pytest
import logging
from decimal import Decimal
from unittest.mock import Mock
from devops_testing.services import PaymentService
from devops_testing.models import User

class TestLogging:
    def test_logging_emitted(self, payment_repo, user_repo, dummy_gateway, test_user, capsys):
        """Verifica que los mensajes de log se emiten correctamente."""
        
        # Configuramos un logger que escribe a stderr (capturado por capsys)
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.INFO)
        
        # Aseguramos que se escriba a stderr
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        # Creamos el servicio con el logger inyectado
        service = PaymentService(
            dummy_gateway, payment_repo, user_repo, logger=logger
        )
        
        # Procesamos un pago
        payment_id = service.process_payment(test_user.username, Decimal("42.99"), "USD")
        
        # Capturamos la salida
        captured = capsys.readouterr()
        
        # Verificamos que los mensajes esperados están en la salida
        assert "start-payment" in captured.err
        assert "payment-ok" in captured.err
        assert payment_id in captured.err
    
    def test_no_logging_when_not_configured(self, payment_repo, user_repo, dummy_gateway, test_user):
        """Verifica que no hay errores cuando no se proporciona un logger."""
        
        # Creamos el servicio sin logger
        service = PaymentService(dummy_gateway, payment_repo, user_repo)
        
        # Procesamos un pago (no debería haber excepciones)
        payment_id = service.process_payment(test_user.username, Decimal("42.99"), "USD")
        
        assert payment_id
    
    def test_logger_receives_payment_info(self):
        """
        Verifica que el logger recibe la información correcta del pago
        usando un mock para verificar las llamadas exactas.
        """
        # Mocks para todas las dependencias
        gateway = Mock()
        gateway.charge.return_value = True
        
        payment_repo = Mock()
        user_repo = Mock()
        
        test_user = User(username="log_test", email="log@example.com")
        user_repo.get.return_value = test_user
        
        # Mock de logger
        logger = Mock()
        
        # Creamos el servicio con el logger mock
        service = PaymentService(gateway, payment_repo, user_repo, logger=logger)
        
        # Procesamos un pago
        amount = Decimal("99.99")
        currency = "EUR"
        service.process_payment(test_user.username, amount, currency)
        
        # Verificamos que logger.info se llamó exactamente 2 veces
        assert logger.info.call_count == 2
        
        # Verificamos que los mensajes contienen la información esperada
        first_call_args = logger.info.call_args_list[0][0][0]
        assert "start-payment" in first_call_args
        assert test_user.username in first_call_args
        assert str(amount) in first_call_args
        assert currency in first_call_args
        
        second_call_args = logger.info.call_args_list[1][0][0]
        assert "payment-ok" in second_call_args 