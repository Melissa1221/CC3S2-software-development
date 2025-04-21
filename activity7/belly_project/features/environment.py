import os
import sys
import random
from unittest.mock import MagicMock
from src.belly import Belly

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def before_all(context):
    """
    Se ejecuta una vez al inicio de todas las pruebas.
    Configuración inicial global.
    """
    context.config.setup_logging()
    
    random.seed(42)
    
    os.environ["BEHAVE_TESTING_MODE"] = "True"

def after_all(context):
    """
    Se ejecuta una vez al final de todas las pruebas.
    Limpieza global.
    """
    if "BEHAVE_TESTING_MODE" in os.environ:
        del os.environ["BEHAVE_TESTING_MODE"]

def before_feature(context, feature):
    """
    Se ejecuta antes de cada feature.
    """
    if "language_english" in feature.tags:
        context.language = "english"
    else:
        context.language = "spanish"

def before_scenario(context, scenario):
    """
    Se ejecuta antes de cada escenario.
    """
    if "1000 pepinos" in scenario.name or "grandes cantidades" in scenario.name:
        context.belly = Belly(modo_prueba_escalabilidad=True)
        print("Modo de prueba de escalabilidad ACTIVADO")
    else:
        use_fake_clock = False
        for tag in scenario.tags:
            if tag in ["@mock_time", "@fake_clock"]:
                use_fake_clock = True
        
        if use_fake_clock:
            fake_clock = MagicMock()
            fake_clock.return_value = 1000.0  
            context.belly = Belly(clock_service=fake_clock)
            context.fake_clock = fake_clock
        else:
            context.belly = Belly()
        
    context.exception = None
    
    import time
    context.start_time = time.time()

def after_scenario(context, scenario):
    """
    Se ejecuta después de cada escenario.
    """
    if hasattr(context, "belly"):
        context.belly.reset()
        
    if hasattr(context, "fake_clock"):
        delattr(context, "fake_clock")
    
    import time
    end_time = time.time()
    execution_time = (end_time - context.start_time) * 1000  
    
    print(f"Escenario '{scenario.name}' tomó {execution_time:.2f} ms en ejecutarse")

"""
# features/environment.py

from unittest.mock import MagicMock
from src.belly import Belly
import time

def before_scenario(context, scenario):
    # Creamos un mock del reloj para poder simular tiempo
    fake_clock = MagicMock()
    # Valor inicial del reloj
    initial_time = 10000.0
    fake_clock.return_value = initial_time
    
    context.current_time = initial_time

    def advance_time(hours):
        # Convierte horas a segundos
        context.current_time += (hours * 3600)
        fake_clock.return_value = context.current_time

    context.advance_time = advance_time

    # Instanciamos Belly con el servicio de reloj mockeado
    context.belly = Belly(clock_service=fake_clock)
    context.exception = None

def after_scenario(context, scenario):
    # Limpieza al final del escenario
    pass

"""
