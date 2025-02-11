from django.contrib import admin
from .models import Proveedores, Pagos, Facturas
# Register your models here.

admin.site.register(Proveedores)
admin.site.register(Facturas)
admin.site.register(Pagos)

