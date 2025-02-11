from django.core.validators import RegexValidator
from django.core.validators import ValidationError


from decimal import Decimal,InvalidOperation

def validacion_numeros(value):
    if not value.isdigit():
        raise ValidationError("El valor debe contenir solo numeros")


    

def validacion_monto(valor):
    if not isinstance(valor, (int, float, Decimal)):  # Incluye Decimal
        raise ValidationError('El valor debe ser un número.')
    if valor <= 0:
        raise ValidationError('El valor debe ser un número positivo.')

def mi_vista(request):
    if request.method == 'POST':
        valor_str = request.POST.get('monto')
        if valor_str:
            valor_str = valor_str.strip()
            try:
                valor = Decimal(valor_str)  # Usa Decimal para precisión
            except (ValueError, InvalidOperation):  # Captura errores de Decimal
                raise ValidationError('El valor debe ser un número válido.')

            validacion_monto(valor)
            # ... (resto de tu código)