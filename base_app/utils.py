from base_app.models import Marca, Categoria, Condicion_Producto

def get_marcas():
    return {marca.id_mar: marca.nom_mar for marca in Marca.objects.all()} 

def get_condiciones():
    return {condicion.id_cond: condicion.nom_cond for condicion in Condicion_Producto.objects.all()}

def get_categorias():
    return {categoria.id_cate: categoria.nom_cate for categoria in Categoria.objects.all()}
