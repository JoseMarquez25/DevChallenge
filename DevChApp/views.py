from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Vehiculo, Ruta
from .forms import UsuarioForm, VehiculoForm, RutaForm
from django.http import HttpResponse

# === Index ===
def index(request):
    rutas = Ruta.objects.all()  
    return render(request, 'index.html', {'rutas': rutas})


# === USUARIO CRUD ===
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/list.html', {'usuarios': usuarios})

def usuario_create(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('usuario_list')
    return render(request, 'usuario/form.html', {'form': form})

def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect('usuario_list')
    return render(request, 'usuario/form.html', {'form': form})

def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    return render(request, 'usuario/delete.html', {'usuario': usuario})


# === VEHICULO CRUD ===
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculo/list.html', {'vehiculos': vehiculos})

def vehiculo_create(request):
    form = VehiculoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vehiculo_list')
    return render(request, 'vehiculo/form.html', {'form': form})

def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    form = VehiculoForm(request.POST or None, instance=vehiculo)
    if form.is_valid():
        form.save()
        return redirect('vehiculo_list')
    return render(request, 'vehiculo/form.html', {'form': form})

def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('vehiculo_list')
    return render(request, 'vehiculo/delete.html', {'vehiculo': vehiculo})


# === RUTA CRUD ===
def ruta_list(request):
    rutas = Ruta.objects.all()
    return render(request, 'ruta/list.html', {'rutas': rutas})

def ruta_create(request):
    form = RutaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('ruta_list')
    return render(request, 'ruta/form.html', {'form': form})

def ruta_update(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    form = RutaForm(request.POST or None, instance=ruta)
    if form.is_valid():
        form.save()
        return redirect('ruta_list')
    return render(request, 'ruta/form.html', {'form': form})

def ruta_delete(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    if request.method == 'POST':
        ruta.delete()
        return redirect('ruta_list')
    return render(request, 'ruta/delete.html', {'ruta': ruta})
