import pytest
from unittest.mock import MagicMock, patch
from src.belly import Belly, CantidadNegativaError, CantidadExcesivaError

class TestBellyWithMock:
    """Pruebas unitarias para la clase Belly usando mocks para simular el tiempo"""
    
    def test_gruñir_con_reloj_simulado(self):
        """Prueba que el estómago gruñe correctamente usando un reloj simulado"""
        mock_clock = MagicMock()
        mock_clock.return_value = 1000.0  #
        
        belly = Belly(clock_service=mock_clock)
        belly.comer(15)
        belly.esperar(2.0)
        
        assert belly.esta_gruñendo() == True
    
    def test_no_gruñir_con_reloj_simulado(self):
        """Prueba que el estómago no gruñe cuando no se cumplen las condiciones"""
        mock_clock = MagicMock()
        mock_clock.return_value = 2000.0
        
        belly = Belly(clock_service=mock_clock)
        
        belly.comer(5)
        belly.esperar(3.0)
        
        assert belly.esta_gruñendo() == False
    
    def test_tiempo_transcurrido_real(self):
        """Prueba que el tiempo transcurrido se calcula correctamente con el reloj simulado"""
        mock_clock = MagicMock()
        
        mock_clock.side_effect = [1000.0, 1000.0 + 7200.0]  
        
        belly = Belly(clock_service=mock_clock)
        
        assert belly.tiempo_transcurrido_real() == 2.0
    
    def test_digestion_con_reloj_simulado(self):
        """Prueba que el tiempo de digestión se calcula correctamente"""
        mock_clock = MagicMock()
        mock_clock.return_value = 3000.0
        
        belly = Belly(clock_service=mock_clock)
        
        belly.comer(10)  
        belly.esperar(0.5)  
        
        assert belly.tiempo_digestion() == 1.5 