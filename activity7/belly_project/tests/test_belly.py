import pytest
from src.belly import Belly, CantidadNegativaError, CantidadExcesivaError


def test_gruñir_si_comido_muchos_pepinos():
    belly = Belly()
    belly.comer(15)
    belly.esperar(2)
    assert belly.esta_gruñendo() is True


def test_no_gruñir_si_pocos_pepinos():
    belly = Belly()
    belly.comer(10)
    belly.esperar(2)
    assert belly.esta_gruñendo() is False


def test_no_gruñir_si_poco_tiempo():
    belly = Belly()
    belly.comer(20)
    belly.esperar(1)
    assert belly.esta_gruñendo() is False


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
    assert belly.esta_gruñendo() is True


def test_pepinos_restantes():
    belly = Belly()
    belly.comer(15)
    assert belly.pepinos_restantes() == 15
    belly.comer(7)
    assert belly.pepinos_restantes() == 22


def test_pepinos_disponibles():
    belly = Belly()
    belly.comer(8)
    assert belly.pepinos_disponibles() == 2

    belly.comer(3)
    assert belly.pepinos_disponibles() == 0


def test_esta_gruñendo_limite_exacto():
    belly = Belly()
    belly.comer(11)
    belly.esperar(1.5)
    assert belly.esta_gruñendo() is True


def test_esta_gruñendo_tiempo_exacto():
    belly = Belly()
    belly.comer(15)
    belly.esperar(1.5)
    assert belly.esta_gruñendo() is True


def test_esta_gruñendo_ambos_limites_fallan():
    belly = Belly()
    belly.comer(10)
    belly.esperar(1.4)
    assert belly.esta_gruñendo() is False


def test_tiempo_digestion_pepinos():
    belly = Belly()
    belly.comer(20)
    assert belly.tiempo_digestion() == 4.0

    belly.comer(10)
    assert belly.tiempo_digestion() == 6.0


def test_tiempo_digestion_cero_pepinos():
    belly = Belly()
    assert belly.tiempo_digestion() == 0.0


def test_tiempo_digestion_ya_digerido():
    belly = Belly()
    belly.comer(5)
    belly.esperar(5)
    assert belly.tiempo_digestion() == 0.0
