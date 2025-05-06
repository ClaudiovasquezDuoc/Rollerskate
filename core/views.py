from django.shortcuts import render
from .models import Producto
from .forms import ProductoForm, RegistroForm, EditarUsuarioForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
import requests
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def accesorios(request):
    return render(request, 'core/accesorios.html')

def patines(request):
    return render(request, 'core/patines.html')

def protecciones(request):
    return render(request, 'core/protecciones.html')

def repuestos(request):
    return render(request, 'core/repuestos.html')

def servicio(request):
    return render(request, 'core/servicio.html')

def vestimenta(request):
    return render(request, 'core/vestimenta.html')

# otros

@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'core/listar.html', {'productos': productos})

@login_required
@staff_member_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST )
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
        return render(request, 'core/crear.html', {'form': form})
    else:
        form = ProductoForm()
    return render(request, 'core/crear.html', {'form': form})

@login_required
@staff_member_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('listar_productos')
    return render(request, 'core/editar.html', {'form': form, 'producto': producto})

@login_required
@staff_member_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'core/eliminar.html', {'producto': producto})


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('listar_productos')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})


# --------------------------
# EDICIÓN DE PERFIL
# --------------------------

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            password = form.cleaned_data.get('password1')
            if password:
                user.set_password(password)

            user.save()
            return redirect('login')  # Redirige para re-loguearse si se cambió la contraseña
    else:
        form = EditarUsuarioForm(instance=request.user)

    return render(request, 'core/editar_perfil.html', {'form': form})

def obtener_ciclovias(request):
    query = """
    [out:json];
    area["name"="Santiago"]["admin_level"="8"]->.searchArea;
    (
      way["highway"="cycleway"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """
    url = 'https://overpass-api.de/api/interpreter'
    response = requests.post(url, data={'data': query})

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'No se pudo obtener datos'}, status=500)


from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import serializers

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import Ventas, Boleta
from rest_framework.response import Response
from .serializers import VentasSerializer
from django.db import transaction

class VentasListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ventas = Ventas.objects.filter(usuario=request.user)
        serializer = VentasSerializer(ventas, many=True)
        return Response(serializer.data)
    
    @transaction.atomic
    def post(self, request):
        datos = request.data
        ventas = Ventas.objects.create(usuario=request.user)

        for item in datos.get('detalles', []):
            producto_id = item.get('id')
            cantidad = item.get('cantidad', 1)
            try:
                producto = Producto.objects.get(id=producto_id)
                boleta = Boleta(
                    id_cliente=ventas.usuario,
                    id_producto=producto,
                    cantidad=cantidad,
                    total=producto.precio * cantidad
                )
                
            except Producto.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"error": "Producto no encontrado."}, status=400)
            
        serializers = VentasSerializer(ventas)
        return Response(serializers.data, status=201)
            

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


from .models import Cliente

@login_required
def carrito(request):
    productos = Producto.objects.all()
    clientes = Cliente.objects.all()  # 👈

    productos_con_cantidad = []
    for producto in productos:
        cantidad = 1
        total = producto.precio * cantidad
        productos_con_cantidad.append({
            'producto': producto,
            'cantidad': cantidad,
            'total': total
        })

    return render(request, 'core/carrito.html', {
        'productos': productos_con_cantidad,
        'clientes': clientes  # 👈
    })


@csrf_exempt
@require_POST
@login_required
def procesar_Venta(request):
    if request.method == 'POST':
        datos = json.loads(request.body)
        productos = datos.get('productos', [])
        cliente_id = datos.get('cliente_id')  # 👈 OBTENEMOS EL ID DEL CLIENTE

        if not cliente_id:
            return JsonResponse({'mensaje': 'ID de cliente no proporcionado'}, status=400)

        try:
            cliente = Cliente.objects.get(id=cliente_id)  # 👈 CARGAMOS EL OBJETO CLIENTE
        except Cliente.DoesNotExist:
            return JsonResponse({'mensaje': 'Cliente no encontrado'}, status=404)

        for item in productos:
            producto_id = item['id']
            cantidad = item['cantidad']

            try:
                producto = Producto.objects.get(id=producto_id)
                Ventas.objects.create(
                    usuario=request.user,
                    id_producto=producto,
                    id_cliente=cliente,
                    cantidad=cantidad,
                    total=producto.precio * cantidad
                )
            except Producto.DoesNotExist:
                return JsonResponse({'mensaje': f'Producto con id {producto_id} no existe'}, status=400)

        return JsonResponse({'mensaje': 'Venta procesada correctamente'})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

