import random
from django.core.validators import RegexValidator
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, contrasena=None, **extra_fields):
        if not correo:
            raise ValueError("El correo electrónico es obligatorio.")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(contrasena)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, contrasena=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # ¡Este sí es importante!
        return self.create_user(correo, contrasena, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='La cédula debe tener 10 dígitos numéricos.')]
    )
    correo = models.EmailField(unique=True)
    verificado = models.BooleanField(default=False)
    codigo_verificacion = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # necesario para admin

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'cedula']

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

    
class Vehiculo(models.Model):
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.marca} - {self.placa}"
    
class Ruta(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    cupos_disponibles = models.PositiveIntegerField(default=1)

    pasajeros = models.ManyToManyField(
        Usuario, 
        related_name='rutas_como_pasajero', 
        blank=True
    )

    def __str__(self):
        return f"{self.origen} me dirijo hacia {self.destino} y salgo a las {self.hora} del dia {self.fecha}"

    def agregar_pasajero(self, usuario):
        if self.pasajeros.count() < self.cupos_disponibles:
            self.pasajeros.add(usuario)
            return True
        return False