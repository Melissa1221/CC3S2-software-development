# Actividad 8

inicializamos el repositorio con la estructura dada
![](https://i.imgur.com/ZSDrCkB.png)

##### Ejercicio 1: Método para vaciar el carrito
**Objetivo:**  
Implementa en la clase `Carrito` un método llamado `vaciar()` que elimine todos los items del carrito. Luego, escribe pruebas siguiendo el patrón AAA para verificar que, al vaciar el carrito, la lista de items quede vacía y el total sea 0.

Creamos el método vaciar

```py
    def vaciar(self):
        """
        Elimina todos los items del carrito.
        """
        self.items = []
```

Ahora el test para vaciar
```py
def test_vaciar_carrito():
    """
    AAA:
    Arrange: Se crea un carrito y se agregan varios productos.
    Act: Se vacía el carrito.
    Assert: Se verifica que la lista de items quede vacía y el total sea 0.
    """
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Disco Duro", precio=120.00)
    producto2 = ProductoFactory(nombre="Memoria RAM", precio=80.00)
    carrito.agregar_producto(producto1, cantidad=2)
    carrito.agregar_producto(producto2, cantidad=3)
    # Act
    carrito.vaciar()
    # Assert
    assert len(carrito.obtener_items()) == 0
    assert carrito.calcular_total() == 0.0
```

El resultado
![](https://i.imgur.com/0mwx7B0.png)

##### Ejercicio 2: Descuento por compra mínima
**Objetivo:**  
Amplía la lógica del carrito para aplicar un descuento solo si el total supera un monto determinado. Por ejemplo, si el total es mayor a \$500, se aplica un 15% de descuento.

Creando el método aplicar descuento condicional
```py
def aplicar_descuento_condicional(self, porcentaje, minimo):
        """
        Aplica un descuento solo si el total del carrito supera el monto mínimo.
        Args:
            porcentaje: Porcentaje de descuento a aplicar (entre 0 y 100).
            minimo: Monto mínimo que debe alcanzar el carrito para aplicar el descuento.
        Returns:
            El total con descuento si se cumple la condición, o el total sin descuento.
        """
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        total = self.calcular_total()
        if total >= minimo:
            descuento = total * (porcentaje / 100)
            return total - descuento
        return total
```

Los test
```py
def test_aplicar_descuento_condicional_cumple_minimo():
    """
    AAA:
    Arrange: Se crea un carrito con un total que supera el mínimo para el descuento.
    Act: Se aplica un descuento condicional del 15% con un mínimo de $500.
    Assert: Se verifica que se aplica el descuento ya que se cumple la condición.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Laptop Gaming", precio=200.00)
    carrito.agregar_producto(producto, cantidad=3)  # Total 600
    # Act
    total_con_descuento = carrito.aplicar_descuento_condicional(15, 500)
    # Assert
    # 600 - (600 * 0.15) = 600 - 90 = 510
    assert total_con_descuento == 510.00
```

El resultado
![](https://i.imgur.com/urMmMeb.png)

##### Ejercicio 3: Manejo de stock en producto
**Objetivo:**  
Modifica la clase `Producto` para que incluya un atributo `stock` (cantidad disponible). Luego, actualiza el método `agregar_producto` en `Carrito` para que verifique que no se agregue una cantidad mayor a la disponible en stock. Si se intenta agregar más, se debe lanzar una excepción.

Modificamos Producto

```py
class Producto:
    def __init__(self, nombre, precio, stock=0):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
    def __repr__(self):
        return f"Producto({self.nombre}, {self.precio}, stock={self.stock})"
```

Actualizamos la fábrica para que genere un stock

```py
class ProductoFactory(factory.Factory):
    class Meta:
        model = Producto
    nombre = factory.Faker("word")
    precio = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    stock = factory.Faker("random_int", min=1, max=100)
```

Actualizamos el test

```py
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
```

El resultado
![](https://i.imgur.com/RUmQZTo.png)

##### Ejercicio 4: Ordenar items del carrito
**Objetivo:**  
Agrega un método en `Carrito` que devuelva la lista de items ordenados por un criterio (por ejemplo, por precio unitario o por nombre del producto).

nuevo método
```py
 def obtener_items_ordenados(self, criterio):
        """
        Devuelve una lista ordenada de los items del carrito según el criterio especificado.
        Args:
            criterio: Criterio de ordenamiento ('precio' o 'nombre').
        Returns:
            Lista ordenada de items.
        Raises:
            ValueError: Si el criterio no es válido.
        """
        if criterio not in ["precio", "nombre"]:
            raise ValueError("Criterio de ordenamiento no válido. Debe ser 'precio' o 'nombre'")
        if criterio == "precio":
            return sorted(self.items, key=lambda item: item.producto.precio)
        else:  # criterio == "nombre"
            return sorted(self.items, key=lambda item: item.producto.nombre)
```

test
```py
def test_obtener_items_ordenados_criterio_invalido():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act & Assert: Se verifica que se lanza una excepción al solicitar items ordenados con un criterio inválido.
    """
    # Arrange
    carrito = Carrito()
    producto = Producto("Laptop", 800.00, stock=5)
    carrito.agregar_producto(producto, cantidad=1)
    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        carrito.obtener_items_ordenados("color")
    assert "Criterio de ordenamiento no válido" in str(excinfo.value)
```

El resultado

![](https://i.imgur.com/6ASrncv.png)

##### Ejercicio 5: Uso de Pytest Fixtures
**Objetivo:**  
Refactoriza las pruebas para que utilicen **fixtures** de Pytest, de modo que se reutilicen instancias comunes de `Carrito` o de productos.

Creamos un archivo conftest.py para los fixtures
```py
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
```

refactorizando algunos test
```py
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
```

![](https://i.imgur.com/1nTEggN.png)

##### Ejercicio 6: Pruebas parametrizadas
**Objetivo:**  

Utiliza la marca `@pytest.mark.parametrize` para crear pruebas que verifiquen múltiples escenarios de descuento o actualización de cantidades.
para los test

```py
# Pruebas parametrizadas
@pytest.mark.parametrize(
    "porcentaje,total_esperado",
    [
        (0, 600.0),    # Sin descuento
        (10, 540.0),   # 10% de descuento
        (25, 450.0),   # 25% de descuento
        (50, 300.0),   # 50% de descuento
        (75, 150.0),   # 75% de descuento
        (100, 0.0),    # 100% de descuento
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
```

El resultado
![](https://i.imgur.com/RdDBUFu.png)
##### Ejercicio 7: Calcular impuestos en el carrito
**Objetivo:**  
Implementar un método `calcular_impuestos(porcentaje)` que retorne el valor del impuesto calculado sobre el total del carrito.

Comenzamos con el test de impuestos

```py
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
    carrito.agregar_producto(producto, cantidad=4)  # Total = 1000
    # Act
    impuesto = carrito.calcular_impuestos(10)  # 10% de 1000 = 100
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
        (5, 1000, 50.0),    # 5% de 1000 = 50
        (10, 1000, 100.0),  # 10% de 1000 = 100
        (15, 1000, 150.0),  # 15% de 1000 = 150
        (7.5, 200, 15.0),   # 7.5% de 200 = 15
        (0, 500, 0.0),      # 0% de cualquier valor = 0
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
        carrito.calcular_impuestos(101)  # Porcentaje mayor a 100
    assert "El porcentaje debe estar entre 0 y 100" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        carrito.calcular_impuestos(-5)  # Porcentaje negativo
    assert "El porcentaje debe estar entre 0 y 100" in str(excinfo.value)
```

![](https://i.imgur.com/af2Vl3V.png)

Ahora implementamos el método

```py
    def calcular_impuestos(self, porcentaje):
        """
        Calcula el valor de los impuestos basados en el porcentaje indicado.
        Args:
            porcentaje (float): Porcentaje de impuesto a aplicar (entre 0 y 100).
        Returns:
            float: Monto del impuesto.
        Raises:
            ValueError: Si el porcentaje no está entre 0 y 100.
        """
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        total = self.calcular_total()
        return total * (porcentaje / 100)
```

El resultado
![](https://i.imgur.com/yZLMa2T.png)

##### Ejercicio 8: Aplicar cupón de descuento con límite máximo
**Objetivo:**  
Implementar un método `aplicar_cupon(descuento_porcentaje, descuento_maximo)` que aplique un cupón de descuento al total del carrito, pero asegurándose de que el descuento no supere un valor máximo.

Ahora implementamos el máximo descuento. Con esto estamos en la fase roja
![](https://i.imgur.com/z0sOXxx.png)


```py
 def aplicar_cupon(self, descuento_porcentaje, descuento_maximo):
        """
        Aplica un cupón de descuento al total del carrito, con un límite máximo.
        """
        if descuento_porcentaje < 0 or descuento_maximo < 0:
            raise ValueError("Los valores de descuento deben ser positivos")
        total = self.calcular_total()
        descuento_calculado = total * (descuento_porcentaje / 100)
        descuento_final = min(descuento_calculado, descuento_maximo)
        return total - descuento_final
```

El resultado
![](https://i.imgur.com/qPnV7XQ.png)

##### Ejercicio 9: Validación de stock al agregar productos (RGR)
**Objetivo:**  
Asegurarse de que al agregar un producto al carrito, no se exceda la cantidad disponible en stock.


Implementamos los test

![](https://i.imgur.com/hcjfPcR.png)
![](https://i.imgur.com/YSuo6zN.png)

Ahora implementamos un método refactor para validar el stock

```py
    def validar_stock(self, producto, cantidad_solicitada):
        """
        Valida que haya suficiente stock para la cantidad solicitada.
        Args:
            producto: El producto a validar.
            cantidad_solicitada: La cantidad que se quiere agregar o actualizar.
        Returns:
            La cantidad actual del producto en el carrito.
        Raises:
            ValueError: Si no hay suficiente stock disponible.
        """
        cantidad_actual = 0
        for item in self.items:
            if item.producto.nombre == producto.nombre:
                cantidad_actual = item.cantidad
                break
        if cantidad_actual + cantidad_solicitada > producto.stock:
            raise ValueError(f"No hay suficiente stock. Disponible: {producto.stock}, En carrito: {cantidad_actual}, Solicitado: {cantidad_solicitada}")
        return cantidad_actual
```

El resultado
![](https://i.imgur.com/K3zeRrR.png)

