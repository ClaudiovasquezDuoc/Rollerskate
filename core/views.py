from django.shortcuts import render
from .models import Producto
from .forms import ProductoForm, RegistroForm, EditarUsuarioForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login


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

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'core/listar.html', {'productos': productos})

def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_productos')
    return render(request, 'core/crear.html', {'form': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('listar_productos')
    return render(request, 'core/editar.html', {'form': form, 'producto': producto})


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
    return render(request, 'registro.html', {'form': form})


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

    return render(request, 'editar_perfil.html', {'form': form})

