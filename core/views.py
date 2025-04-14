from django.shortcuts import render

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