from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='La cédula debe contener exactamente 10 dígitos numéricos.'
            )
        ]
    )
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}  ({self.cedula})"
    
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