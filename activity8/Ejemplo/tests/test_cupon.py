# tests/test_cupon.py
import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory

def test_aplicar_cupon_con_limite():
    """
    Red: Se espera que al aplicar un cupón, el descuento no supere el límite máximo.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto", precio=200.00, stock=10)
    carrito.agregar_producto(producto, cantidad=2)  # Total = 400

    # Act
    total_con_cupon = carrito.aplicar_cupon(20, 50)  # 20% de 400 = 80, pero límite es 50

    # Assert
    assert total_con_cupon == 350.00

def test_aplicar_cupon_sin_alcanzar_limite():
    """
    Caso donde el descuento calculado no supera el límite máximo.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto Económico", precio=100.00, stock=10)
    carrito.agregar_producto(producto, cantidad=2)  # Total = 200

    # Act
    total_con_cupon = carrito.aplicar_cupon(10, 50)  # 10% de 200 = 20, no supera el límite

    # Assert
    assert total_con_cupon == 180.00

def test_aplicar_cupon_carrito_vacio():
    """
    Aplicar un cupón a un carrito vacío debe retornar 0.
    """
    # Arrange
    carrito = Carrito()

    # Act
    total_con_cupon = carrito.aplicar_cupon(10, 50)

    # Assert
    assert total_con_cupon == 0.0

def test_aplicar_cupon_valores_negativos():
    """
    Se debe lanzar una excepción si se utilizan valores negativos.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto", precio=100.00, stock=10)
    carrito.agregar_producto(producto, cantidad=1)

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.aplicar_cupon(-10, 50)
    assert "Los valores de descuento deben ser positivos" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        carrito.aplicar_cupon(10, -50)
    assert "Los valores de descuento deben ser positivos" in str(excinfo.value)

@pytest.mark.parametrize(
    "porcentaje,maximo,total_carrito,total_esperado",
    [
        (20, 50, 400, 350),   # Descuento de 80, limitado a 50
        (10, 100, 500, 450),  # Descuento de 50, no alcanza el límite
        (30, 20, 200, 180),   # Descuento de 60, limitado a 20
        (5, 10, 100, 95),     # Descuento de 5, no alcanza el límite
        (0, 0, 300, 300),     # Sin descuento
    ]
)
def test_aplicar_cupon_parametrizado(porcentaje, maximo, total_carrito, total_esperado):
    """
    Prueba parametrizada para diferentes escenarios de cupones.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Producto parametrizado", precio=total_carrito, stock=10)
    carrito.agregar_producto(producto, cantidad=1)

    # Act
    total_con_cupon = carrito.aplicar_cupon(porcentaje, maximo)

    # Assert
    assert total_con_cupon == total_esperado 