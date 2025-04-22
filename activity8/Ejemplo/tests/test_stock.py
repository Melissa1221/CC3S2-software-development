# tests/test_stock.py
import pytest
from src.carrito import Carrito, Producto

def test_agregar_producto_excede_stock():
    """
    Red: Se espera que al intentar agregar una cantidad mayor a la disponible en stock se lance un ValueError.
    """
    # Arrange
    producto = Producto("ProductoStock", 100.00, stock=5)
    carrito = Carrito()

    # Act & Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto, cantidad=6)

def test_agregar_producto_cantidad_exacta_stock():
    """
    Se puede agregar un producto con una cantidad igual al stock disponible.
    """
    # Arrange
    producto = Producto("ProductoExacto", 150.00, stock=3)
    carrito = Carrito()

    # Act
    carrito.agregar_producto(producto, cantidad=3)

    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3

def test_agregar_producto_acumulado_excede_stock():
    """
    No se debe poder agregar productos si la cantidad acumulada supera el stock.
    """
    # Arrange
    producto = Producto("ProductoAcumulado", 200.00, stock=8)
    carrito = Carrito()
    carrito.agregar_producto(producto, cantidad=5)  # Primero agregamos 5 unidades

    # Act & Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto, cantidad=4)  # Intentamos agregar 4 más (total 9 > stock 8)

def test_agregar_diferentes_productos_mismo_nombre():
    """
    Si se agregan dos productos con el mismo nombre pero diferentes instancias, se deben acumular.
    """
    # Arrange
    producto1 = Producto("ProductoDuplicado", 50.00, stock=10)
    producto2 = Producto("ProductoDuplicado", 50.00, stock=10)
    carrito = Carrito()
    
    # Act
    carrito.agregar_producto(producto1, cantidad=3)
    carrito.agregar_producto(producto2, cantidad=4)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 7

@pytest.mark.parametrize(
    "stock,cantidad,valido",
    [
        (10, 5, True),   # Cantidad menor al stock
        (10, 10, True),  # Cantidad igual al stock
        (10, 11, False), # Cantidad mayor al stock
        (1, 2, False),   # Cantidad ligeramente mayor al stock mínimo
        (0, 1, False),   # Stock cero
    ]
)
def test_validacion_stock_parametrizado(stock, cantidad, valido):
    """
    Prueba parametrizada para diferentes escenarios de validación de stock.
    """
    # Arrange
    producto = Producto("ProductoParametrizado", 75.00, stock=stock)
    carrito = Carrito()
    
    # Act & Assert
    if valido:
        carrito.agregar_producto(producto, cantidad=cantidad)
        items = carrito.obtener_items()
        assert len(items) == 1
        assert items[0].cantidad == cantidad
    else:
        with pytest.raises(ValueError):
            carrito.agregar_producto(producto, cantidad=cantidad) 