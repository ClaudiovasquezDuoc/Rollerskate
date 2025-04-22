from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError

class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    descripcion = models.TextField(blank=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.PROTECT, related_name='productos')
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='productos')

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?\d{8,15}$', 'Número de teléfono inválido.')]
    )
    email = models.EmailField(blank=True, unique=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Boleta(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='boletas')
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='boletas')
    fecha_boleta = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total != self.id_producto.precio * self.cantidad:
            raise ValidationError("El total no coincide con el precio del producto multiplicado por la cantidad.")

    def __str__(self):
        return f"Boleta {self.id} - Cliente: {self.id_cliente.nombre}"

    class Meta:
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"
        ordering = ['-fecha_boleta']

class Ventas(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='ventas')
    fecha_venta = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id} - Cliente: {self.id_cliente.nombre}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']