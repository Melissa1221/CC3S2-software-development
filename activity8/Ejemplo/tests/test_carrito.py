## Ejemplo de prueba
# tests/test_carrito.py

import pytest
from src.carrito import Carrito, Producto
from src.factories import ProductoFactory

def test_agregar_producto_nuevo(carrito, producto_generico):
    """
    AAA:
    Arrange: Uso de fixture para un carrito vacío y un producto genérico.
    Act: Se agrega el producto al carrito.
    Assert: Se verifica que el carrito contiene un item con el producto y cantidad 1.
    """
    # Act
    carrito.agregar_producto(producto_generico)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].producto.nombre == "Genérico"
    assert items[0].cantidad == 1


def test_agregar_producto_existente_incrementa_cantidad(carrito):
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se agrega el mismo producto nuevamente aumentando la cantidad.
    Assert: Se verifica que la cantidad del producto se incrementa en el item.
    """
    # Arrange
    producto = ProductoFactory(nombre="Mouse", precio=50.00, stock=10)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    carrito.agregar_producto(producto, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3


def test_remover_producto(carrito, producto_generico):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se agrega un producto con cantidad 3.
    Act: Se remueve una unidad del producto.
    Assert: Se verifica que la cantidad del producto se reduce a 2.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=3)
    
    # Act
    carrito.remover_producto(producto_generico, cantidad=1)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 2


def test_remover_producto_completo(carrito, producto_generico):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se agrega un producto.
    Act: Se remueve la totalidad de la cantidad del producto.
    Assert: Se verifica que el producto es eliminado del carrito.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=2)
    
    # Act
    carrito.remover_producto(producto_generico, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_actualizar_cantidad_producto(carrito, producto_generico):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 5.
    Assert: Se verifica que la cantidad se actualiza correctamente.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=1)
    
    # Act
    carrito.actualizar_cantidad(producto_generico, nueva_cantidad=5)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 5


def test_actualizar_cantidad_a_cero_remueve_producto(carrito, producto_generico):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 0.
    Assert: Se verifica que el producto se elimina del carrito.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=3)
    
    # Act
    carrito.actualizar_cantidad(producto_generico, nueva_cantidad=0)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_calcular_total(carrito_con_productos):
    """
    AAA:
    Arrange: Se usa fixture de carrito con productos ya agregados.
    Act: Se calcula el total del carrito.
    Assert: Se verifica que el total es la suma correcta de cada item (precio * cantidad).
    """
    # Act
    total = carrito_con_productos.calcular_total()
    
    # Assert
    # Producto Barato: 50.0 * 2 = 100.0
    # Producto Caro: 500.0 * 1 = 500.0
    # Total: 600.0
    assert total == 600.00


def test_aplicar_descuento(carrito_con_productos):
    """
    AAA:
    Arrange: Se usa fixture de carrito con productos ya agregados.
    Act: Se aplica un descuento del 10% al total.
    Assert: Se verifica que el total con descuento sea el correcto.
    """
    # Act
    total_con_descuento = carrito_con_productos.aplicar_descuento(10)
    
    # Assert
    # Total sin descuento: 600.0
    # Descuento (10%): 60.0
    # Total con descuento: 540.0
    assert total_con_descuento == 540.00


def test_aplicar_descuento_limites(carrito, producto_generico):
    """
    AAA:
    Arrange: Se usa fixture de carrito y producto.
    Act y Assert: Se verifica que aplicar un descuento fuera del rango [0, 100] genere un error.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=1)
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(150)
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(-5)

def test_vaciar_carrito(carrito_con_productos):
    """
    AAA:
    Arrange: Se usa fixture de carrito con productos ya agregados.
    Act: Se vacía el carrito.
    Assert: Se verifica que la lista de items quede vacía y el total sea 0.
    """
    # Act
    carrito_con_productos.vaciar()
    
    # Assert
    assert len(carrito_con_productos.obtener_items()) == 0
    assert carrito_con_productos.calcular_total() == 0.0

def test_aplicar_descuento_condicional_cumple_minimo(carrito_con_productos):
    """
    AAA:
    Arrange: Se usa fixture de carrito con productos para un total de 600.
    Act: Se aplica un descuento condicional del 15% con un mínimo de $500.
    Assert: Se verifica que se aplica el descuento ya que se cumple la condición.
    """
    # Act
    total_con_descuento = carrito_con_productos.aplicar_descuento_condicional(15, 500)
    
    # Assert
    # 600 - (600 * 0.15) = 600 - 90 = 510
    assert total_con_descuento == 510.00

def test_aplicar_descuento_condicional_no_cumple_minimo(carrito, producto_barato):
    """
    AAA:
    Arrange: Se crea un carrito con un total que NO supera el mínimo para el descuento.
    Act: Se aplica un descuento condicional del 15% con un mínimo de $500.
    Assert: Se verifica que NO se aplica el descuento ya que no se cumple la condición.
    """
    # Arrange
    carrito.agregar_producto(producto_barato, cantidad=3)  # Total 150
    
    # Act
    total_con_descuento = carrito.aplicar_descuento_condicional(15, 500)
    
    # Assert
    # El total es 150, que es menor que 500, así que no se aplica descuento
    assert total_con_descuento == 150.00

def test_aplicar_descuento_condicional_igual_al_minimo(carrito, producto_caro):
    """
    AAA:
    Arrange: Se crea un carrito con un total exactamente igual al mínimo para el descuento.
    Act: Se aplica un descuento condicional del 15% con un mínimo de $500.
    Assert: Se verifica que se aplica el descuento ya que se cumple la condición.
    """
    # Arrange
    carrito.agregar_producto(producto_caro, cantidad=1)  # Total exactamente 500
    
    # Act
    total_con_descuento = carrito.aplicar_descuento_condicional(15, 500)
    
    # Assert
    # 500 - (500 * 0.15) = 500 - 75 = 425
    assert total_con_descuento == 425.00

def test_aplicar_descuento_condicional_porcentaje_invalido(carrito, producto_generico):
    """
    AAA:
    Arrange: Se usa fixture de carrito y producto.
    Act y Assert: Se verifica que aplicar un descuento condicional con porcentaje fuera del 
    rango [0, 100] genere un error.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=2)
    
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

def test_agregar_producto_dentro_del_stock(carrito):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se crea un producto con stock limitado.
    Act: Se agrega una cantidad dentro del límite de stock.
    Assert: Se verifica que el producto se agrega correctamente.
    """
    # Arrange
    producto = Producto("Monitor", 300.00, stock=5)
    
    # Act
    carrito.agregar_producto(producto, cantidad=3)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3

def test_agregar_producto_excede_stock(carrito):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se crea un producto con stock limitado.
    Act & Assert: Se verifica que se lanza una excepción al intentar agregar más unidades que el stock disponible.
    """
    # Arrange
    producto = Producto("Impresora 3D", 400.00, stock=2)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.agregar_producto(producto, cantidad=3)
    assert "No hay suficiente stock" in str(excinfo.value)

def test_agregar_producto_acumulado_excede_stock(carrito):
    """
    AAA:
    Arrange: Se usa fixture de carrito, se agrega un producto con cantidad válida.
    Act & Assert: Se verifica que se lanza una excepción al intentar agregar más unidades 
    que, sumadas a las ya existentes, exceden el stock.
    """
    # Arrange
    producto = Producto("Smartphone", 800.00, stock=5)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.agregar_producto(producto, cantidad=3)
    assert "No hay suficiente stock" in str(excinfo.value)

def test_actualizar_cantidad_excede_stock(carrito):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se agrega un producto.
    Act & Assert: Se verifica que se lanza una excepción al intentar actualizar la cantidad 
    a un valor que excede el stock.
    """
    # Arrange
    producto = Producto("Tablet", 250.00, stock=3)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.actualizar_cantidad(producto, nueva_cantidad=5)
    assert "No hay suficiente stock" in str(excinfo.value)

def test_obtener_items_ordenados_por_precio(carrito):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se agregan varios productos con diferentes precios.
    Act: Se solicitan los items ordenados por precio.
    Assert: Se verifica que la lista devuelta está ordenada de menor a mayor precio.
    """
    # Arrange
    producto1 = Producto("Ratón", 25.00, stock=10)
    producto2 = Producto("Teclado", 50.00, stock=10)
    producto3 = Producto("Monitor", 200.00, stock=10)
    
    # Agregamos los productos en orden diferente al esperado en el resultado
    carrito.agregar_producto(producto3, cantidad=1)
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=1)
    
    # Act
    items_ordenados = carrito.obtener_items_ordenados("precio")
    
    # Assert
    assert len(items_ordenados) == 3
    assert items_ordenados[0].producto.nombre == "Ratón"
    assert items_ordenados[1].producto.nombre == "Teclado"
    assert items_ordenados[2].producto.nombre == "Monitor"

def test_obtener_items_ordenados_por_nombre(carrito):
    """
    AAA:
    Arrange: Se usa fixture de carrito y se agregan varios productos con diferentes nombres.
    Act: Se solicitan los items ordenados por nombre.
    Assert: Se verifica que la lista devuelta está ordenada alfabéticamente por nombre.
    """
    # Arrange
    producto1 = Producto("Monitor", 200.00, stock=10)
    producto2 = Producto("Ratón", 25.00, stock=10)
    producto3 = Producto("Teclado", 50.00, stock=10)
    
    # Agregamos los productos en orden diferente al esperado en el resultado
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto3, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=1)
    
    # Act
    items_ordenados = carrito.obtener_items_ordenados("nombre")
    
    # Assert
    assert len(items_ordenados) == 3
    assert items_ordenados[0].producto.nombre == "Monitor"
    assert items_ordenados[1].producto.nombre == "Ratón"
    assert items_ordenados[2].producto.nombre == "Teclado"

def test_obtener_items_ordenados_criterio_invalido(carrito, producto_generico):
    """
    AAA:
    Arrange: Se usa fixture de carrito y producto.
    Act & Assert: Se verifica que se lanza una excepción al solicitar items ordenados con un criterio inválido.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=1)
    
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.obtener_items_ordenados("color")
    assert "Criterio de ordenamiento no válido" in str(excinfo.value)