# tests/test_impuestos.py
import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory

def test_calcular_impuestos():
    """
    Red: Se espera que calcular_impuestos retorne el valor del impuesto.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto", precio=250.00, stock=10)
    carrito.agregar_producto(producto, cantidad=4)  # Total = 1000

    # Act
    impuesto = carrito.calcular_impuestos(10)  # 10% de 1000 = 100

    # Assert
    assert impuesto == 100.00

def test_calcular_impuestos_carrito_vacio():
    """
    Prueba de calcular impuestos en un carrito vacío.
    """
    # Arrange
    carrito = Carrito()
    
    # Act
    impuesto = carrito.calcular_impuestos(10)
    
    # Assert
    assert impuesto == 0.0

@pytest.mark.parametrize(
    "porcentaje,total_carrito,impuesto_esperado",
    [
        (5, 1000, 50.0),    # 5% de 1000 = 50
        (10, 1000, 100.0),  # 10% de 1000 = 100
        (15, 1000, 150.0),  # 15% de 1000 = 150
        (7.5, 200, 15.0),   # 7.5% de 200 = 15
        (0, 500, 0.0),      # 0% de cualquier valor = 0
    ]
)
def test_calcular_impuestos_parametrizado(porcentaje, total_carrito, impuesto_esperado):
    """
    Prueba parametrizada para calcular impuestos con diferentes porcentajes.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto para impuestos", precio=total_carrito, stock=10)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    impuesto = carrito.calcular_impuestos(porcentaje)
    
    # Assert
    assert impuesto == impuesto_esperado

def test_calcular_impuestos_porcentaje_invalido():
    """
    Prueba que verifica que se lance una excepción al usar un porcentaje fuera del rango permitido.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto", precio=100.00, stock=10)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.calcular_impuestos(101)  # Porcentaje mayor a 100
    assert "El porcentaje debe estar entre 0 y 100" in str(excinfo.value)
    
    with pytest.raises(ValueError) as excinfo:
        carrito.calcular_impuestos(-5)  # Porcentaje negativo
    assert "El porcentaje debe estar entre 0 y 100" in str(excinfo.value) 