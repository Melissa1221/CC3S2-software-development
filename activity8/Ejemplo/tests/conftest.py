import pytest
from src.carrito import Carrito, Producto
from src.factories import ProductoFactory

@pytest.fixture
def carrito():
    """Fixture que retorna un carrito vacío"""
    return Carrito()

@pytest.fixture
def producto_generico():
    """Fixture que retorna un producto genérico usando la fábrica"""
    return ProductoFactory(nombre="Genérico", precio=100.0, stock=10)

@pytest.fixture
def producto_barato():
    """Fixture que retorna un producto de bajo precio"""
    return Producto(nombre="Producto Barato", precio=50.0, stock=10)

@pytest.fixture
def producto_caro():
    """Fixture que retorna un producto de alto precio"""
    return Producto(nombre="Producto Caro", precio=500.0, stock=10)

@pytest.fixture
def carrito_con_productos(carrito, producto_barato, producto_caro):
    """Fixture que retorna un carrito con productos ya agregados"""
    carrito.agregar_producto(producto_barato, cantidad=2)
    carrito.agregar_producto(producto_caro, cantidad=1)
    return carrito 