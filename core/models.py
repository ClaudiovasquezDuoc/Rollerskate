from django.db import models

# Create your models here.


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    descripcion = models.TextField(blank=True)
    id_proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, related_name='productos')
    id_categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productos')
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Boleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='boletas')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='boletas')
    fecha_boleta = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Boleta {self.id_boleta} - Cliente: {self.id_cliente.nombre}"

class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    fecha_venta = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id_venta} - Cliente: {self.id_cliente.nombre}"
