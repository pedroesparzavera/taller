from django.contrib import admin
from base_app.models import *
from django.contrib.auth.models import User



admin.site.register(Metodo_Registro)
admin.site.register(Rol)
admin.site.register(Condicion_Producto)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Ciudad)
admin.site.register(Estado_Usuario)
admin.site.register(Usuario)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Estado_Publicacion)
admin.site.register(Publicacion)
admin.site.register(Tipo_Evento)
admin.site.register(Historial_Publicacion)
admin.site.register(Foto)
admin.site.register(Login)
admin.site.register(Registro)

admin.site.register(Perfil)


#mezcla de info de perfil y usuario

class Perfil_Inline(admin.StackedInline):
    model = Perfil

#Etencion de User Model
class AdminUsu(admin.ModelAdmin):
    models = User
    field =["username", "firs_name","last_name", "email"]
    inlines = [Perfil_Inline]

#desregistrar de la manera antigua
admin.site.unregister(User)

#registrar de la manera  nueva
admin.site.register(User, AdminUsu)