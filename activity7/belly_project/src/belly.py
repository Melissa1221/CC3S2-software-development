# src/belly.py
# from src.clock import get_current_time

class CantidadNegativaError(Exception):
    """Excepción lanzada cuando se intenta comer una cantidad negativa de pepinos."""
    pass

class CantidadExcesivaError(Exception):
    """Excepción lanzada cuando se intenta comer demasiados pepinos."""
    pass

class Belly:
    def __init__(self):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0

    def reset(self):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0

    def comer(self, pepinos):
        # Validar cantidad de pepinos
        if pepinos < 0:
            raise CantidadNegativaError(f"No puedes comer una cantidad negativa de pepinos: {pepinos}")
        
        if pepinos > 100:
            raise CantidadExcesivaError(f"No puedes comer más de 100 pepinos: {pepinos}")
            
        print(f"He comido {pepinos} pepinos.")
        self.pepinos_comidos += pepinos

    def esperar(self, tiempo_en_horas):
        if tiempo_en_horas > 0:
            self.tiempo_esperado += tiempo_en_horas

    def esta_gruñendo(self):
        # Verificar que ambas condiciones se cumplan correctamente:
        # Se han esperado al menos 1.5 horas Y se han comido más de 10 pepinos
        if self.tiempo_esperado >= 1.5 and self.pepinos_comidos > 10:
            return True
        return False
