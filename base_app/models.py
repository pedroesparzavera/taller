import os
from django.db import models
import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# perfil del customer


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    tfno = models.CharField(max_length=20, blank=True)
    pais = models.CharField(max_length=200, blank=True)
    region = models.CharField(max_length=20, blank=True)
    ciu = models.CharField(max_length=20, blank=True)
    

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        perfil_usuario = Perfil(user=instance)
        perfil_usuario.save()


class Metodo_Registro(models.Model):
    id_metreg = models.AutoField(primary_key=True)
    nom_metreg = models.CharField(max_length=50)
    desc_metreg = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_metreg


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nom_rol = models.CharField(max_length=50)
    desc_rol = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_rol


class Condicion_Producto(models.Model):
    id_cond = models.AutoField(primary_key=True)
    nom_cond = models.CharField(max_length=50)
    desc_cond = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_cond


class Region(models.Model):
    id_reg = models.AutoField(primary_key=True)
    nom_reg = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_reg


class Comuna(models.Model):
    id_comu = models.AutoField(primary_key=True)
    nom_comu = models.CharField(max_length=50)
    id_reg = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_comu


class Ciudad(models.Model):
    id_ciu = models.AutoField(primary_key=True)
    nom_ciu = models.CharField(max_length=50)
    id_comu = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_ciu


class Estado_Usuario(models.Model):
    id_estusu = models.AutoField(primary_key=True)
    nom_estusu = models.CharField(max_length=50)
    desc_estusu = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_estusu


class Usuario(models.Model):
    id_usu = models.AutoField(primary_key=True)
    nom_usu = models.CharField(max_length=50)
    apepat_usu = models.CharField(max_length=50)
    apepmat_usu = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telefono = models.CharField(max_length=15)
    sexo_usu = models.CharField(max_length=10, choices=[(
        'masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')])
    contra_hash = models.CharField(max_length=255)
    fech_reg = models.DateTimeField(null=True, blank=True)
    fech_actualiusu = models.DateTimeField(null=True, blank=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    id_ciu = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    id_estusu = models.ForeignKey(Estado_Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_usu


class Marca(models.Model):
    id_mar = models.AutoField(primary_key=True)
    nom_mar = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_mar


class Categoria(models.Model):
    id_cate = models.AutoField(primary_key=True)
    nom_cate = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_cate


def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('media/', filename)


class Producto(models.Model):
    id_prod = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=700)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    imagen = models.ImageField(
        upload_to=get_file_path, max_length=200, blank=True, null=True)

    id_mar = models.ForeignKey(Marca, on_delete=models.CASCADE)
    id_cate = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_cond = models.ForeignKey(Condicion_Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Estado_Publicacion(models.Model):
    id_estpubli = models.AutoField(primary_key=True)
    nom_estpubli = models.CharField(max_length=50)
    desc_estpubli = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_estpubli


class Publicacion(models.Model):
    id_publi = models.AutoField(primary_key=True)
    titulo_publi = models.CharField(max_length=100)
    desc_publi = models.CharField(max_length=500)
    precio = models.FloatField()
    fech_publi = models.DateTimeField(null=True, blank=True)
    fech_actualipubli = models.DateTimeField(null=True, blank=True)
    id_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_estpubli = models.ForeignKey(
        Estado_Publicacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_publi


class Tipo_Evento(models.Model):
    id_tipoeven = models.AutoField(primary_key=True)
    nom_tipoeven = models.CharField(max_length=50)
    desc_tipoeven = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_tipoeven


class Historial_Publicacion(models.Model):
    id_hist = models.AutoField(primary_key=True)
    desc_hist = models.CharField(max_length=200, null=True, blank=True)
    prec_ant = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    prec_nue = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    fech_even = models.DateTimeField()
    id_publi = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    id_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_tipoeven = models.ForeignKey(Tipo_Evento, on_delete=models.CASCADE)
    id_estpubli = models.ForeignKey(
        Estado_Publicacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Historial {self.id_hist}"


class Foto(models.Model):
    id_foto = models.AutoField(primary_key=True)
    ruta_foto = models.CharField(max_length=200)
    id_prod = models.ForeignKey(Producto, related_name='fotos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Foto {self.id_foto} de Producto {self.id_prod.nombre}"


class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    fech_login = models.DateTimeField()
    ip_login = models.CharField(max_length=45, null=True, blank=True)
    disp_login = models.CharField(max_length=100, null=True, blank=True)
    est_login = models.CharField(max_length=10, choices=[(
        'exitoso', 'Exitoso'), ('fallido', 'Fallido')])
    ulti_login = models.DateTimeField(null=True, blank=True)
    res_token = models.CharField(max_length=255, null=True, blank=True)
    fech_exptoken = models.DateTimeField(null=True, blank=True)
    id_usu = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Login {self.id_login}"


class Registro(models.Model):
    id_reg = models.AutoField(primary_key=True)
    fech_reg = models.DateTimeField()
    met_reg = models.CharField(max_length=200)
    ip_reg = models.CharField(max_length=45)
    disp_reg = models.CharField(max_length=100, null=True, blank=True)
    id_metreg = models.ForeignKey(Metodo_Registro, on_delete=models.CASCADE)

    def __str__(self):
        return f"Registro {self.id_reg}"
