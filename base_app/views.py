from django.shortcuts import render,redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from base_app.models import Producto, Categoria, Marca, Condicion_Producto, Perfil, Foto
from base_app.forms import PublicarProductoForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
from marketplace import settings

def index(request):
    productos_recientes = Producto.objects.all()[:6]  # Para el Carrousel, 6  productos más recientes
    productos_descuento = Producto.objects.filter(descuento__isnull=False)[:8]  # Ejemplo: productos con descuento

    context = {
        'productos_recientes_start': productos_recientes[:3],
        'productos_recientes_end': productos_recientes[3:],
        'productos_descuento_start': productos_descuento[4:],
        'productos_descuento_end': productos_descuento[:4],  
    }
    return render(request, 'index.html', context)

def productos(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
    }
    return render(request, 'productos.html', context)

def productos_filtrados(request, categoria):
    categoriaProducto = Categoria.objects.get(nom_cate=categoria)
    productos = Producto.objects.filter(id_cate=categoriaProducto).all()
    context = {
        'productos': productos,
    }
    return render(request, 'productos.html', context)

def detalle_producto(request, id):
    producto = Producto.objects.get(id_prod=id)
    context = {
        'producto': producto,
    }
    return render(request, 'detalle_prod.html', context)

@login_required
def publicar(request):
    if request.method == 'POST':
        form = PublicarProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Validar las relaciones
                    marca = get_object_or_404(Marca, id_mar=request.POST.get('id_mar'))
                    categoria = get_object_or_404(Categoria, id_cate=request.POST.get('id_cate'))
                    condicion = get_object_or_404(Condicion_Producto, id_cond=request.POST.get('id_cond'))

                    # Crear el producto
                    producto = Producto.objects.create(
                        nombre=form.cleaned_data['nombre'],
                        descripcion=form.cleaned_data['descripcion'],
                        precio=form.cleaned_data['precio'],
                        descuento=form.cleaned_data['descuento'],
                        id_mar=marca,
                        id_cate=categoria,
                        id_cond=condicion,
                    )

                    # Procesar las imágenes subidas
                    imagenes = request.FILES.getlist('imagenes')
                    for imagen in imagenes:
                        # Verificar si el archivo es una imagen válida
                        if imagen.content_type.startswith('image/'):
                            fs = FileSystemStorage()
                            filename = fs.save(imagen.name, imagen)
                            ruta = fs.url(filename)
                            Foto.objects.create(id_prod=producto, ruta_foto=ruta)
                        else:
                            raise ValueError("El archivo subido no es una imagen válida.")

                    messages.success(request, "Producto publicado exitosamente.")
                    return redirect('productos')
            except Exception as e:
                messages.error(request, f"Error al publicar el producto: {e}")
        else:
            messages.error(request, "Por favor, revisa los datos ingresados.")
    else:
        form = PublicarProductoForm()
    return render(request, 'publicar.html', {'form': form})
def login_required_message(request):
    messages.error(request, "Debes iniciar sesión para publicar productos.")
    return redirect('/login')

def perfil_cliente(request):
    return render(request, 'perfil/perfil_cliente.html')

def perfil_usuario(request):
    if request.user.is_authenticated:
        user = request.user  # Usuario actual
        try:
            perfil = Perfil.objects.get(user=user)  # Obtenemos el perfil asociado al usuario
        except Perfil.DoesNotExist:
            perfil = None  # Si no existe el perfil, manejamos el caso adecuadamente

        productos = Producto.objects.all()
        context = {
            'user': user,           # Pasamos los datos del usuario
            'perfil': perfil,       # Pasamos el perfil del usuario
            'productos': productos, # Pasamos los productos
        }
        return render(request, 'perfil/perfil_usuario.html', context)
    else:
        messages.error(request, "Debes iniciar sesión para ver tu perfil.")
        return redirect('/login')



def x(request):
    return render (request, 'perfil/x.html')


def terminos_condiciones(request):
    return render(request, 'terminos_condiciones.html')

def politicas_privacidad(request):
    return render(request, 'politicas_privacidad.html')

def preguntas_frecuentes(request):
    return render(request, 'preguntas_frecuentes.html')

def contacto(request):
    """
    Vista para renderizar el formulario de contacto.
    """
    return render(request, 'formulario_contacto.html')