import pytest
from src.belly import Belly, CantidadNegativaError, CantidadExcesivaError

def test_gruñir_si_comido_muchos_pepinos():
    belly = Belly()
    belly.comer(15)
    belly.esperar(2)
    assert belly.esta_gruñendo() == True

def test_no_gruñir_si_pocos_pepinos():
    belly = Belly()
    belly.comer(10)
    belly.esperar(2)
    assert belly.esta_gruñendo() == False

def test_no_gruñir_si_poco_tiempo():
    belly = Belly()
    belly.comer(20)
    belly.esperar(1)
    assert belly.esta_gruñendo() == False

def test_error_pepinos_negativos():
    belly = Belly()
    with pytest.raises(CantidadNegativaError):
        belly.comer(-5)

def test_error_pepinos_excesivos():
    belly = Belly()
    with pytest.raises(CantidadExcesivaError):
        belly.comer(150)

def test_modo_prueba_escalabilidad():
    belly = Belly(modo_prueba_escalabilidad=True)
    belly.comer(1000)  # No debería lanzar excepción
    belly.esperar(2)
    assert belly.esta_gruñendo() == True 