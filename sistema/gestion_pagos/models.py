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


class Pagos(models.Model):
    id_pago = models.CharField(max_length=10,primary_key=True,validators=[MinLengthValidator(10),MaxLengthValidator(10),validacion_numeros])
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2,validators=[validacion_monto])
    referencia = models.CharField(max_length=50, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50,choices=METODO_PAGO)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        db_table = 'Pagos'

    def __str__(self):
        return f'Pago #{self.id_pago} a {self.proveedor.nombre_empresa} el {self.fecha_pago}'


class Facturas(models.Model):
    id_factura = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2,validators=[validacion_monto])
    numero_factura = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        db_table = 'Facturas'

    def __str__(self):
        return f'Factura #{self.numero_factura} de {self.proveedor.nombre_empresa}'