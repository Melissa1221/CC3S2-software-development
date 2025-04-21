# src/belly.py
# from src.clock import get_current_time

class CantidadNegativaError(Exception):
    """Excepción lanzada cuando se intenta comer una cantidad negativa de pepinos"""
    pass

class CantidadExcesivaError(Exception):
    """Excepción lanzada cuando se intenta comer demasiados pepinos"""
    pass

class Belly:
    LIMITE_GRUÑIDO_PEPINOS = 10
    TIEMPO_MINIMO_GRUÑIDO = 1.5
    TIEMPO_DIGESTION_POR_PEPINO = 0.2
    
    def __init__(self, modo_prueba_escalabilidad=False):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0
        self.modo_prueba_escalabilidad = modo_prueba_escalabilidad
        if modo_prueba_escalabilidad:
            self.limite_pepinos = 10000
        else:
            self.limite_pepinos = 100  
        
    def reset(self):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0

    def comer(self, pepinos):
        if pepinos < 0:
            raise CantidadNegativaError(f"No puedes comer una cantidad negativa de pepinos: {pepinos}")
        
        if pepinos > self.limite_pepinos:
            raise CantidadExcesivaError(f"No puedes comer más de {self.limite_pepinos} pepinos: {pepinos}")
            
        import time
        inicio = time.time()
        
        print(f"He comido {pepinos} pepinos.")
        self.pepinos_comidos += pepinos
        
        if pepinos > 500:
            fin = time.time()
            tiempo_ejecucion = (fin - inicio) * 1000
            print(f"Rendimiento: Comer {pepinos} pepinos tomó {tiempo_ejecucion:.2f} ms")

    def esperar(self, tiempo_en_horas):
        import time
        inicio = time.time()
        
        if tiempo_en_horas > 0:
            self.tiempo_esperado += tiempo_en_horas
        
        if tiempo_en_horas > 5:
            fin = time.time()
            tiempo_ejecucion = (fin - inicio) * 1000
            print(f"Rendimiento: Esperar {tiempo_en_horas} horas tomó {tiempo_ejecucion:.2f} ms")

    def esta_gruñendo(self):
        return self._suficientes_pepinos() and self._tiempo_suficiente()
    
    def _suficientes_pepinos(self):
        return self.pepinos_comidos > self.LIMITE_GRUÑIDO_PEPINOS
    
    def _tiempo_suficiente(self):
        return self.tiempo_esperado >= self.TIEMPO_MINIMO_GRUÑIDO
        
    def pepinos_restantes(self):
        return self.pepinos_comidos
        
    def pepinos_disponibles(self):
        disponibles = max(0, self.LIMITE_GRUÑIDO_PEPINOS - self.pepinos_comidos)
        return disponibles
        
    def tiempo_digestion(self):
        if self.pepinos_comidos <= 0:
            return 0.0
            
        tiempo_total = self.pepinos_comidos * self.TIEMPO_DIGESTION_POR_PEPINO
        tiempo_restante = max(0.0, tiempo_total - self.tiempo_esperado)
        return round(tiempo_restante, 1)
