from django.shortcuts import render

from rest_framework import viewsets
from .models import Proveedores, Pagos, Facturas
from .serializers import ProveedorSerializer, PagoSerializer, FacturaSerializer
from rest_framework.permissions import AllowAny

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [AllowAny]

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pagos.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [AllowAny]

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Facturas.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [AllowAny]

