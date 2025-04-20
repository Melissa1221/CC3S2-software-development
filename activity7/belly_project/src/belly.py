# src/belly.py
# from src.clock import get_current_time

class CantidadNegativaError(Exception):
    """Excepción lanzada cuando se intenta comer una cantidad negativa de pepinos."""
    pass

class CantidadExcesivaError(Exception):
    """Excepción lanzada cuando se intenta comer demasiados pepinos."""
    pass

class Belly:
    def __init__(self, modo_prueba_escalabilidad=False):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0
        self.modo_prueba_escalabilidad = modo_prueba_escalabilidad
        if modo_prueba_escalabilidad:
            self.limite_pepinos = 10000  # Límite mucho mayor para pruebas de escalabilidad
        else:
            self.limite_pepinos = 100    # Límite normal para uso regular
        
    def reset(self):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0

    def comer(self, pepinos):
        # Validar cantidad de pepinos
        if pepinos < 0:
            raise CantidadNegativaError(f"No puedes comer una cantidad negativa de pepinos: {pepinos}")
        
        if pepinos > self.limite_pepinos:
            raise CantidadExcesivaError(f"No puedes comer más de {self.limite_pepinos} pepinos: {pepinos}")
            
        # Registrar inicio para pruebas de rendimiento
        import time
        inicio = time.time()
        
        print(f"He comido {pepinos} pepinos.")
        self.pepinos_comidos += pepinos
        
        # Medir tiempo de ejecución para cantidades grandes
        if pepinos > 500:
            fin = time.time()
            tiempo_ejecucion = (fin - inicio) * 1000  # en milisegundos
            print(f"Rendimiento: Comer {pepinos} pepinos tomó {tiempo_ejecucion:.2f} ms")

    def esperar(self, tiempo_en_horas):
        # Registrar inicio para pruebas de rendimiento
        import time
        inicio = time.time()
        
        if tiempo_en_horas > 0:
            self.tiempo_esperado += tiempo_en_horas
        
        # Medir tiempo de ejecución para tiempos grandes
        if tiempo_en_horas > 5:
            fin = time.time()
            tiempo_ejecucion = (fin - inicio) * 1000  # en milisegundos
            print(f"Rendimiento: Esperar {tiempo_en_horas} horas tomó {tiempo_ejecucion:.2f} ms")

    def esta_gruñendo(self):
        # Verificar que ambas condiciones se cumplan correctamente:
        # Se han esperado al menos 1.5 horas Y se han comido más de 10 pepinos
        if self.tiempo_esperado >= 1.5 and self.pepinos_comidos > 10:
            return True
        return False
