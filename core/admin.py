from django.contrib import admin

# Register your models here.

from .models import Producto
from .models import Categoria
from .models import Proveedor
from .models import Cliente
from .models import Boleta
from .models import Ventas

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Boleta)
admin.site.register(Ventas)