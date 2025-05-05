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

