from django.contrib import admin
from .models import Usuario, Vehiculo, Ruta

@admin.register(Vehiculo)
class DevAdmin(admin.ModelAdmin):
    pass

@admin.register(Ruta)
class DevAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from django.utils.translation import gettext_lazy as _


class UsuarioAdmin(UserAdmin):
    model = Usuario

    # Campos que se mostrarán en la lista del admin
    list_display = ('correo', 'nombre', 'is_staff', 'is_superuser', 'verificado')
    list_filter = ('is_staff', 'is_superuser', 'verificado')

    # Agrupación de campos para la vista de detalle
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        (_('Información personal'), {'fields': ('nombre', 'cedula', 'verificado')}),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas importantes'), {'fields': ('last_login',)}),
    )

    # Campos mostrados al crear un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'cedula', 'password1', 'password2', 'verificado', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('correo', 'cedula', 'nombre')
    ordering = ('correo',)

admin.site.register(Usuario, UsuarioAdmin)
