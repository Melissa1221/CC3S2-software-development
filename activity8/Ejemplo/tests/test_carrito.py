## Ejemplo de prueba
# tests/test_carrito.py

import pytest
from src.carrito import Carrito, Producto
from src.factories import ProductoFactory

def test_agregar_producto_nuevo():
    """
    AAA:
    Arrange: Se crea un carrito y se genera un producto.
    Act: Se agrega el producto al carrito.
    Assert: Se verifica que el carrito contiene un item con el producto y cantidad 1.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Laptop", precio=1000.00, stock=10)
    
    # Act
    carrito.agregar_producto(producto)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].producto.nombre == "Laptop"
    assert items[0].cantidad == 1


def test_agregar_producto_existente_incrementa_cantidad():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se agrega el mismo producto nuevamente aumentando la cantidad.
    Assert: Se verifica que la cantidad del producto se incrementa en el item.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Mouse", precio=50.00, stock=10)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    carrito.agregar_producto(producto, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3


def test_remover_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con cantidad 3.
    Act: Se remueve una unidad del producto.
    Assert: Se verifica que la cantidad del producto se reduce a 2.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Teclado", precio=75.00, stock=10)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act
    carrito.remover_producto(producto, cantidad=1)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 2


def test_remover_producto_completo():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se remueve la totalidad de la cantidad del producto.
    Assert: Se verifica que el producto es eliminado del carrito.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Monitor", precio=300.00, stock=10)
    carrito.agregar_producto(producto, cantidad=2)
    
    # Act
    carrito.remover_producto(producto, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_actualizar_cantidad_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 5.
    Assert: Se verifica que la cantidad se actualiza correctamente.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Auriculares", precio=150.00, stock=10)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    carrito.actualizar_cantidad(producto, nueva_cantidad=5)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 5


def test_actualizar_cantidad_a_cero_remueve_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 0.
    Assert: Se verifica que el producto se elimina del carrito.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Cargador", precio=25.00, stock=10)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act
    carrito.actualizar_cantidad(producto, nueva_cantidad=0)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_calcular_total():
    """
    AAA:
    Arrange: Se crea un carrito y se agregan varios productos con distintas cantidades.
    Act: Se calcula el total del carrito.
    Assert: Se verifica que el total es la suma correcta de cada item (precio * cantidad).
    """
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Impresora", precio=200.00, stock=10)
    producto2 = ProductoFactory(nombre="Escáner", precio=150.00, stock=10)
    carrito.agregar_producto(producto1, cantidad=2)  # Total 400
    carrito.agregar_producto(producto2, cantidad=1)  # Total 150
    
    # Act
    total = carrito.calcular_total()
    
    # Assert
    assert total == 550.00


def test_aplicar_descuento():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con una cantidad determinada.
    Act: Se aplica un descuento del 10% al total.
    Assert: Se verifica que el total con descuento sea el correcto.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Tablet", precio=500.00, stock=10)
    carrito.agregar_producto(producto, cantidad=2)  # Total 1000
    
    # Act
    total_con_descuento = carrito.aplicar_descuento(10)
    
    # Assert
    assert total_con_descuento == 900.00


def test_aplicar_descuento_limites():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act y Assert: Se verifica que aplicar un descuento fuera del rango [0, 100] genere un error.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Smartphone", precio=800.00, stock=10)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(150)
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(-5)

def test_vaciar_carrito():
    """
    AAA:
    Arrange: Se crea un carrito y se agregan varios productos.
    Act: Se vacía el carrito.
    Assert: Se verifica que la lista de items quede vacía y el total sea 0.
    """
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Disco Duro", precio=120.00, stock=10)
    producto2 = ProductoFactory(nombre="Memoria RAM", precio=80.00, stock=10)
    carrito.agregar_producto(producto1, cantidad=2)
    carrito.agregar_producto(producto2, cantidad=3)
    
    # Act
    carrito.vaciar()
    
    # Assert
    assert len(carrito.obtener_items()) == 0
    assert carrito.calcular_total() == 0.0

def test_aplicar_descuento_condicional_cumple_minimo():
    """
    AAA:
    Arrange: Se crea un carrito con un total que supera el mínimo para el descuento.
    Act: Se aplica un descuento condicional del 15% con un mínimo de $500.
    Assert: Se verifica que se aplica el descuento ya que se cumple la condición.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Laptop Gaming", precio=200.00, stock=10)
    carrito.agregar_producto(producto, cantidad=3)  # Total 600
    
    # Act
    total_con_descuento = carrito.aplicar_descuento_condicional(15, 500)
    
    # Assert
    # 600 - (600 * 0.15) = 600 - 90 = 510
    assert total_con_descuento == 510.00

def test_aplicar_descuento_condicional_no_cumple_minimo():
    """
    AAA:
    Arrange: Se crea un carrito con un total que NO supera el mínimo para el descuento.
    Act: Se aplica un descuento condicional del 15% con un mínimo de $500.
    Assert: Se verifica que NO se aplica el descuento ya que no se cumple la condición.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Teclado Mecánico", precio=100.00, stock=10)
    carrito.agregar_producto(producto, cantidad=3)  # Total 300
    
    # Act
    total_con_descuento = carrito.aplicar_descuento_condicional(15, 500)
    
    # Assert
    # El total es 300, que es menor que 500, así que no se aplica descuento
    assert total_con_descuento == 300.00

def test_aplicar_descuento_condicional_igual_al_minimo():
    """
    AAA:
    Arrange: Se crea un carrito con un total exactamente igual al mínimo para el descuento.
    Act: Se aplica un descuento condicional del 15% con un mínimo de $500.
    Assert: Se verifica que se aplica el descuento ya que se cumple la condición.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Monitor 4K", precio=250.00, stock=10)
    carrito.agregar_producto(producto, cantidad=2)  # Total exactamente 500
    
    # Act
    total_con_descuento = carrito.aplicar_descuento_condicional(15, 500)
    
    # Assert
    # 500 - (500 * 0.15) = 500 - 75 = 425
    assert total_con_descuento == 425.00

def test_aplicar_descuento_condicional_porcentaje_invalido():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act y Assert: Se verifica que aplicar un descuento condicional con porcentaje fuera del 
    rango [0, 100] genere un error.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Audífonos", precio=100.00, stock=10)
    carrito.agregar_producto(producto, cantidad=2)
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.aplicar_descuento_condicional(150, 500)
    with pytest.raises(ValueError):
        carrito.aplicar_descuento_condicional(-5, 500)

def test_producto_con_stock():
    """
    AAA:
    Arrange: Se crea un producto con stock.
    Act: Se verifica el stock.
    Assert: Se verifica que el stock es el correcto.
    """
    # Arrange & Act
    producto = Producto("Teclado", 50.00, stock=15)
    
    # Assert
    assert producto.stock == 15
    assert producto.__repr__() == "Producto(Teclado, 50.0, stock=15)"

def test_agregar_producto_dentro_del_stock():
    """
    AAA:
    Arrange: Se crea un carrito y un producto con stock limitado.
    Act: Se agrega una cantidad dentro del límite de stock.
    Assert: Se verifica que el producto se agrega correctamente.
    """
    # Arrange
    carrito = Carrito()
    producto = Producto("Monitor", 300.00, stock=5)
    
    # Act
    carrito.agregar_producto(producto, cantidad=3)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3

def test_agregar_producto_excede_stock():
    """
    AAA:
    Arrange: Se crea un carrito y un producto con stock limitado.
    Act & Assert: Se verifica que se lanza una excepción al intentar agregar más unidades que el stock disponible.
    """
    # Arrange
    carrito = Carrito()
    producto = Producto("Impresora 3D", 400.00, stock=2)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.agregar_producto(producto, cantidad=3)
    assert "No hay suficiente stock" in str(excinfo.value)

def test_agregar_producto_acumulado_excede_stock():
    """
    AAA:
    Arrange: Se crea un carrito, se agrega un producto con cantidad válida.
    Act & Assert: Se verifica que se lanza una excepción al intentar agregar más unidades 
    que, sumadas a las ya existentes, exceden el stock.
    """
    # Arrange
    carrito = Carrito()
    producto = Producto("Smartphone", 800.00, stock=5)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.agregar_producto(producto, cantidad=3)
    assert "No hay suficiente stock" in str(excinfo.value)

def test_actualizar_cantidad_excede_stock():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act & Assert: Se verifica que se lanza una excepción al intentar actualizar la cantidad 
    a un valor que excede el stock.
    """
    # Arrange
    carrito = Carrito()
    producto = Producto("Tablet", 250.00, stock=3)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.actualizar_cantidad(producto, nueva_cantidad=5)
    assert "No hay suficiente stock" in str(excinfo.value)