from django.db import models
from .choices import METODO_PAGO
from django.core.validators import MinLengthValidator,MaxLengthValidator
from.validadores import validacion_numeros,validacion_monto

class Proveedores(models.Model):
    id_proveedor = models.CharField(max_length=10, primary_key=True,validators=[MinLengthValidator(10),MaxLengthValidator(10),validacion_numeros])
    nombre_empresa = models.CharField(max_length=100)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'Proveedores' 

    def __str__(self):
        return f'{self.id_proveedor} - {self.nombre_empresa}'

class Producto(models.Model):
    id_producto = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10), MaxLengthValidator(10), validacion_numeros])
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50)  # Categoria de producto (Ej: Medicamento, Suplemento, etc.)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True)
    vencimiento = models.DateField(null=True, blank=True)  # Fecha de vencimiento si aplica

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'Productos'

    def __str__(self):
        return f'{self.nombre_producto} ({self.id_producto})'
    
    def actualizar_stock(self, cantidad):
        """Actualizar el stock de productos después de una venta"""
        self.stock -= cantidad
        self.save()

class Cliente(models.Model):
    id_cliente = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10), MaxLengthValidator(10), validacion_numeros])
    nombre_cliente = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10)
    email = models.EmailField()
    historial_compras = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'Clientes'

    def __str__(self):
        return self.nombre_cliente

class Venta(models.Model):
    id_venta = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10), MaxLengthValidator(10), validacion_numeros])
    fecha_venta = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO)
    productos = models.ManyToManyField(Producto, through='DetalleVenta')
    estado = models.CharField(max_length=20, default='Pendiente')  # Estado de la venta: Pendiente, Pagado, Cancelado

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'Ventas'

    def __str__(self):
        return f'Venta #{self.id_venta} - Cliente: {self.cliente.nombre_cliente}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalles Venta'
        db_table = 'DetalleVenta'

    def __str__(self):
        return f'{self.producto.nombre_producto} - Cantidad: {self.cantidad}'
    
    def save(self, *args, **kwargs):
        """Calcula el total y actualiza el stock cuando se guarda el detalle de la venta"""
        self.total = self.precio_unitario * self.cantidad
        self.producto.actualizar_stock(self.cantidad)
        super().save(*args, **kwargs)

class Receta(models.Model):
    id_receta = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10), MaxLengthValidator(10), validacion_numeros])
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_receta = models.DateField()
    doctor = models.CharField(max_length=100)
    productos_recetados = models.ManyToManyField(Producto)

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        db_table = 'Recetas'

    def __str__(self):
        return f'Receta #{self.id_receta} para {self.cliente.nombre_cliente}'

class Inventario(models.Model):
    id_inventario = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10), MaxLengthValidator(10), validacion_numeros])
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_ingreso = models.PositiveIntegerField()
    fecha_ingreso = models.DateField()
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        db_table = 'Inventarios'

    def __str__(self):
        return f'Ingreso de {self.producto.nombre_producto} - {self.cantidad_ingreso} unidades'

class PagoProveedor(models.Model):
    id_pago = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10), MaxLengthValidator(10), validacion_numeros])
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO)
    referencia = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Pago a Proveedor'
        verbose_name_plural = 'Pagos a Proveedores'
        db_table = 'Pagos_Proveedores'

    def __str__(self):
        return f'Pago #{self.id_pago} a {self.proveedor.nombre_empresa}'

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    numero_factura = models.CharField(max_length=20, unique=True)
    productos = models.ManyToManyField(Producto)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        db_table = 'Facturas'

    def __str__(self):
        return f'Factura #{self.numero_factura} - {self.proveedor.nombre_empresa}'
