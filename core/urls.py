from django.urls import path
from .views import home, accesorios, patines, protecciones, repuestos, servicio, vestimenta

urlpatterns = [
    path('', home, name='home'),
    path('accesorios/', accesorios, name='accesorios'),
    path('patines/', patines,name='patines'),
    path('protecciones/', protecciones, name='protecciones'),
    path('repuestos/', repuestos, name='repuestos'),
    path('servicio/', servicio, name='servicio'),
    path('vestimenta/', vestimenta, name='vestimenta'),
]
