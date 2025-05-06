from django.urls import path
from .views import home, accesorios, patines, protecciones, repuestos, servicio, vestimenta
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
<<<<<<< HEAD

from .views import ProductoListCreateAPIView, ProductoRetrieveUpdateDestroyAPIView, VentasListCreateAPIView
=======
from .views import ProductoListCreateAPIView, ProductoRetrieveUpdateDestroyAPIView
>>>>>>> aede43a4ebd1d4664c55c52550ee280677efa71d

api_patterns = [
    path('productos/', ProductoListCreateAPIView.as_view(), name='api_productos'),
    path('productos/<int:pk>/', ProductoRetrieveUpdateDestroyAPIView.as_view(), name='api_producto_detail'),
    path('api/ciclovias/', views.obtener_ciclovias, name='ciclovias'),

]

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
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    path('registro/', views.registro_usuario, name='registro'),
    path('recuperar/', auth_views.PasswordResetView.as_view(template_name='core/recuperar.html'), name='password_reset'),
    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='core/recuperar_enviado.html'), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/restablecer_confirmar.html'), name='password_reset_confirm'),
    path('recuperar/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='core/restablecer_completo.html'), name='password_reset_complete'),
    path('api/productos/', ProductoListCreateAPIView.as_view(), name='api_productos'),
    path('api/productos/<int:pk>/', ProductoRetrieveUpdateDestroyAPIView.as_view(), name='api_producto_detail'),
    path('api/ventas/', VentasListCreateAPIView.as_view(), name='api_ventas'),
    path('carrito/', views.carrito, name='carrito'),
    path('procesar_venta/', views.procesar_Venta, name='procesar_venta'),
    
   


]

