from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F
from .models import Usuario, Vehiculo, Ruta
from .forms import UsuarioForm, VehiculoForm, RutaForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Usuario
from .forms import RegistroForm, VerificacionForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# === Login ===
def login_view(request):
    error = None
    if request.method == 'POST':
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        user = authenticate(request, username=correo, password=contrasena)
        if user is not None:
            if not user.verificado:
                error = "Tu cuenta no está verificada. Revisa tu correo."
            else:
                login(request, user)
                return redirect('index')
        else:
            error = "Correo o contraseña incorrectos."
    return render(request, 'login.html', {'error': error})

# === Index ===
@login_required(login_url='login')
def index(request):
    rutas = Ruta.objects.annotate(
        pasajeros_count=Count('pasajeros'),
        cupos_restantes=ExpressionWrapper(
            F('cupos_disponibles') - Count('pasajeros'),
            output_field=IntegerField()
        )
    ).filter(
        pasajeros_count__lt=F('cupos_disponibles')
    )
    return render(request, 'index.html', {'rutas': rutas})


# === USUARIO CRUD ===
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/list.html', {'usuarios': usuarios})

@login_required(login_url='login')
def usuario_create(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta vista.")
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

@login_required(login_url='login')
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    return render(request, 'usuario/delete.html', {'usuario': usuario})

# === Función de verificación
from django.core.mail import send_mail
from django.conf import settings
import random  # solo si usas random en otro lugar

def enviar_codigo_verificacion(correo, codigo):
    asunto = 'Código de Verificación - Registro PUCE'
    mensaje = f'Su código de verificación es: {codigo}'
    remitente = settings.EMAIL_HOST_USER
    destinatario = [correo]

    resultado = send_mail(asunto, mensaje, remitente, destinatario)
    print(f"send_mail result: {resultado}")  # debería imprimir 1 si fue enviado



# ==== Registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            if not correo.endswith('@puce.edu.ec'):
                form.add_error('correo', 'El correo debe ser institucional (@puce.edu.ec)')
            elif Usuario.objects.filter(correo=correo).exists():
                form.add_error('correo', 'El correo ya está registrado')
            else:
                usuario = form.save(commit=False)
                codigo = str(random.randint(100000, 999999))
                usuario.codigo_verificacion = codigo
                usuario.verificado = False
                usuario.save()
                enviar_codigo_verificacion(correo, codigo)
                request.session['correo'] = correo  # guardamos para el siguiente paso
                return redirect('verificar')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# === Verificar código
def verificar_codigo(request):
    correo = request.session.get('correo')
    if not correo:
        return redirect('registro')

    usuario = Usuario.objects.filter(correo=correo).first()
    if request.method == 'POST':
        form = VerificacionForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo']
            if usuario.codigo_verificacion == codigo_ingresado:
                usuario.verificado = True
                usuario.codigo_verificacion = None
                usuario.save()
                return redirect('login')
            else:
                form.add_error('codigo', 'Código incorrecto')
    else:
        form = VerificacionForm()
    return render(request, 'verificar.html', {'form': form})



# === VEHICULO CRUD ===
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculo/list.html', {'vehiculos': vehiculos})

@login_required(login_url='login')
def vehiculo_create(request):
    form = VehiculoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vehiculo_list')
    return render(request, 'vehiculo/form.html', {'form': form})

@login_required(login_url='login')
def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    form = VehiculoForm(request.POST or None, instance=vehiculo)
    if form.is_valid():
        form.save()
        return redirect('vehiculo_list')
    return render(request, 'vehiculo/form.html', {'form': form})

@login_required(login_url='login')
def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('vehiculo_list')
    return render(request, 'vehiculo/delete.html', {'vehiculo': vehiculo})


# === RUTA CRUD ===
from django.db.models import Count, F, ExpressionWrapper, IntegerField

def ruta_list(request):
    rutas = Ruta.objects.annotate(
        pasajeros_count=Count('pasajeros'),
        cupos_restantes=ExpressionWrapper(
            F('cupos_disponibles') - Count('pasajeros'),
            output_field=IntegerField()
        )
    ).filter(
        pasajeros_count__lt=F('cupos_disponibles')
    )
    return render(request, 'ruta/list.html', {'rutas': rutas})


@login_required(login_url='login')
def ruta_create(request):
    form = RutaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('ruta_list')
    return render(request, 'ruta/form.html', {'form': form})

@login_required(login_url='login')
def ruta_update(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    form = RutaForm(request.POST or None, instance=ruta)
    if form.is_valid():
        form.save()
        return redirect('ruta_list')
    return render(request, 'ruta/form.html', {'form': form})

@login_required(login_url='login')
def ruta_delete(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    if request.method == 'POST':
        ruta.delete()
        return redirect('ruta_list')
    return render(request, 'ruta/delete.html', {'ruta': ruta})

@login_required(login_url='login')
def unirse_a_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)
    usuario = request.user

    # Evitar que el conductor se una como pasajero
    if ruta.conductor == usuario:
        return redirect('ruta_list')

    # Evitar duplicados
    if usuario not in ruta.pasajeros.all() and ruta.pasajeros.count() < ruta.cupos_disponibles:
        ruta.pasajeros.add(usuario)
        ruta.save()

    return redirect('ruta_list')

@login_required(login_url='login')
def abandonar_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, id=ruta_id)
    usuario = request.user

    if usuario in ruta.pasajeros.all():
        ruta.pasajeros.remove(usuario)
        ruta.save()

    return redirect('ruta_list')