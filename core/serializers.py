from rest_framework import serializers
from .models import Producto, Categoria, Proveedor, Cliente, Boleta, Ventas
from django.core.validators import RegexValidator

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    telefono = serializers.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?\d{8,15}$', 'Número de teléfono inválido.')],
        allow_blank=True
    )
    email = serializers.EmailField(allow_blank=True, required=False)

    class Meta:
        model = Cliente
        fields = '__all__'
class BoletaSerializer(serializers.ModelSerializer):
    producto_name = serializers.CharField(source='id_producto.nombre', read_only=True)
    class Meta:
        model = Boleta
        fields = 'id_cliente', 'id_producto', 'fecha_boleta', 'cantidad', 'total', 'producto_name'


class VentasSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')
    detalles = BoletaSerializer(source='boleta_set', many=True, read_only=True)

    class Meta:
        model = Ventas
        fields = ['id', 'usuario', 'fecha_venta', 'detalles']