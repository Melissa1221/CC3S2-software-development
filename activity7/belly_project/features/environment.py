from src.belly import Belly

def before_scenario(context, scenario):
    # Activar modo prueba de escalabilidad solo para escenarios con "1000 pepinos" o similares
    if "1000 pepinos" in scenario.name or "grandes cantidades" in scenario.name:
        context.belly = Belly(modo_prueba_escalabilidad=True)
        print("Modo de prueba de escalabilidad ACTIVADO")
    else:
        context.belly = Belly()
        
    # Inicializar variable para almacenar excepciones
    context.exception = None
    
    # Registrar tiempo de inicio para mediciones de rendimiento
    import time
    context.start_time = time.time()

def after_scenario(context, scenario):
    # Medir tiempo total de ejecución del escenario
    import time
    end_time = time.time()
    execution_time = (end_time - context.start_time) * 1000  # en milisegundos
    
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
