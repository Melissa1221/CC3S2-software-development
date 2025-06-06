# src/carrito.py

class Producto:
    def __init__(self, nombre, precio, stock=0):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __repr__(self):
        return f"Producto({self.nombre}, {self.precio}, stock={self.stock})"


class ItemCarrito:
    def __init__(self, producto, cantidad=1):
        self.producto = producto
        self.cantidad = cantidad

    def total(self):
        return self.producto.precio * self.cantidad

    def __repr__(self):
        return f"ItemCarrito({self.producto}, cantidad={self.cantidad})"


class Carrito:
    def __init__(self):
        self.items = []

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

    def agregar_producto(self, producto, cantidad=1):
        """
        Agrega un producto al carrito. Si el producto ya existe, incrementa la cantidad.
        Verifica que la cantidad a agregar no supere el stock disponible.
        
        Raises:
            ValueError: Si la cantidad a agregar supera el stock disponible.
        """
        # Verificar stock disponible usando el método de validación
        cantidad_actual = self.validar_stock(producto, cantidad)
            
        # Si hay suficiente stock, agregar producto
        for item in self.items:
            if item.producto.nombre == producto.nombre:
                item.cantidad += cantidad
                return
        self.items.append(ItemCarrito(producto, cantidad))

    def remover_producto(self, producto, cantidad=1):
        """
        Remueve una cantidad del producto del carrito.
        Si la cantidad llega a 0, elimina el item.
        """
        for item in self.items:
            if item.producto.nombre == producto.nombre:
                if item.cantidad > cantidad:
                    item.cantidad -= cantidad
                elif item.cantidad == cantidad:
                    self.items.remove(item)
                else:
                    raise ValueError("Cantidad a remover es mayor que la cantidad en el carrito")
                return
        raise ValueError("Producto no encontrado en el carrito")

    def actualizar_cantidad(self, producto, nueva_cantidad):
        """
        Actualiza la cantidad de un producto en el carrito.
        Si la nueva cantidad es 0, elimina el item.
        """
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
            
        # Verificar stock disponible usando la validación de stock
        if nueva_cantidad > producto.stock:
            raise ValueError(f"No hay suficiente stock. Disponible: {producto.stock}, Solicitado: {nueva_cantidad}")
            
        for item in self.items:
            if item.producto.nombre == producto.nombre:
                if nueva_cantidad == 0:
                    self.items.remove(item)
                else:
                    item.cantidad = nueva_cantidad
                return
        raise ValueError("Producto no encontrado en el carrito")

    def calcular_total(self):
        """
        Calcula el total del carrito sin descuento.
        """
        return sum(item.total() for item in self.items)

    def aplicar_descuento(self, porcentaje):
        """
        Aplica un descuento al total del carrito y retorna el total descontado.
        El porcentaje debe estar entre 0 y 100.
        """
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        total = self.calcular_total()
        descuento = total * (porcentaje / 100)
        return total - descuento

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

    def contar_items(self):
        """
        Retorna el número total de items (sumando las cantidades) en el carrito.
        """
        return sum(item.cantidad for item in self.items)

    def obtener_items(self):
        """
        Devuelve la lista de items en el carrito.
        """
        return self.items
        
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
        else:  # criterio == "nombre"
            return sorted(self.items, key=lambda item: item.producto.nombre)
        
    def vaciar(self):
        """
        Elimina todos los items del carrito.
        """
        self.items = []