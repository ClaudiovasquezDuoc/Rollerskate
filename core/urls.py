from django.urls import path
from .views import home, accesorios, patines, protecciones, repuestos, servicio, vestimenta
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('accesorios/', accesorios, name='accesorios'),
    path('patines/', patines,name='patines'),
    path('protecciones/', protecciones, name='protecciones'),
    path('repuestos/', repuestos, name='repuestos'),
    path('servicio/', servicio, name='servicio'),
    path('vestimenta/', vestimenta, name='vestimenta'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),


]

