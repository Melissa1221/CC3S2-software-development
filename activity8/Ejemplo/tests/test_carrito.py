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

# Pruebas parametrizadas
@pytest.mark.parametrize(
    "porcentaje,total_esperado",
    [
        (0, 600.0),    # Sin descuento
        (10, 540.0),   # 10% de descuento
        (25, 450.0),   # 25% de descuento
        (50, 300.0),   # 50% de descuento
        (75, 150.0),   # 75% de descuento
        (100, 0.0),    # 100% de descuento
    ]
)
def test_aplicar_descuento_parametrizado(carrito_con_productos, porcentaje, total_esperado):
    """
    Prueba parametrizada para verificar diferentes porcentajes de descuento.
    """
    # Act
    total_con_descuento = carrito_con_productos.aplicar_descuento(porcentaje)
    
    # Assert
    assert total_con_descuento == total_esperado

@pytest.mark.parametrize(
    "porcentaje_invalido",
    [
        -10,  # Descuento negativo
        101,  # Descuento mayor a 100%
        150,  # Descuento muy alto
        -0.5, # Descuento negativo fraccional
    ]
)
def test_aplicar_descuento_porcentaje_invalido_parametrizado(carrito_con_productos, porcentaje_invalido):
    """
    Prueba parametrizada para verificar que porcentajes inválidos generan excepción.
    """
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito_con_productos.aplicar_descuento(porcentaje_invalido)
    assert "El porcentaje debe estar entre 0 y 100" in str(excinfo.value)

@pytest.mark.parametrize(
    "porcentaje,minimo,total_esperado,se_aplica_descuento",
    [
        (10, 100, 540.0, True),   # Supera el mínimo (600 > 100) - se aplica 10%
        (20, 700, 600.0, False),  # No supera el mínimo (600 < 700) - no se aplica descuento
        (15, 600, 510.0, True),   # Igual al mínimo (600 = 600) - se aplica 15%
        (50, 300, 300.0, True),   # Supera el mínimo y alto descuento - 50%
        (0, 0, 600.0, False),     # Ambos en 0 - no hay descuento real aunque se cumple condición
    ]
)
def test_aplicar_descuento_condicional_parametrizado(carrito_con_productos, porcentaje, minimo, total_esperado, se_aplica_descuento):
    """
    Prueba parametrizada para verificar diferentes escenarios de descuento condicional.
    """
    # Act
    total_con_descuento = carrito_con_productos.aplicar_descuento_condicional(porcentaje, minimo)
    
    # Assert
    if se_aplica_descuento:
        assert total_con_descuento < carrito_con_productos.calcular_total()
    else:
        assert total_con_descuento == carrito_con_productos.calcular_total()
    assert total_con_descuento == total_esperado

@pytest.mark.parametrize(
    "cantidad_inicial,nueva_cantidad,cantidad_esperada",
    [
        (1, 5, 5),     # Aumentar cantidad
        (3, 2, 2),     # Disminuir cantidad
        (2, 2, 2),     # Mantener cantidad
        (1, 10, 10),   # Cantidad máxima (dentro del stock)
        (5, 0, 0),     # Remover producto (cantidad 0)
    ]
)
def test_actualizar_cantidad_parametrizado(carrito, producto_generico, cantidad_inicial, nueva_cantidad, cantidad_esperada):
    """
    Prueba parametrizada para verificar actualización de cantidades válidas.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=cantidad_inicial)
    
    # Act
    carrito.actualizar_cantidad(producto_generico, nueva_cantidad=nueva_cantidad)
    
    # Assert
    items = carrito.obtener_items()
    if nueva_cantidad == 0:
        assert len(items) == 0  # El producto debe ser eliminado
    else:
        assert len(items) == 1
        assert items[0].cantidad == cantidad_esperada

@pytest.mark.parametrize(
    "stock,cantidad,excede_stock",
    [
        (5, 3, False),   # Dentro del stock
        (5, 5, False),   # Igual al stock
        (5, 6, True),    # Excede el stock
        (1, 2, True),    # Excede el stock (mínimo)
        (10, 11, True),  # Excede el stock (por 1)
    ]
)
def test_verificar_stock_parametrizado(carrito, stock, cantidad, excede_stock):
    """
    Prueba parametrizada para verificar la validación de stock.
    """
    # Arrange
    producto = Producto("Test Stock", 100.0, stock=stock)
    
    # Act & Assert
    if excede_stock:
        with pytest.raises(ValueError) as excinfo:
            carrito.agregar_producto(producto, cantidad=cantidad)
        assert "No hay suficiente stock" in str(excinfo.value)
    else:
        carrito.agregar_producto(producto, cantidad=cantidad)
        items = carrito.obtener_items()
        assert len(items) == 1
        assert items[0].cantidad == cantidad