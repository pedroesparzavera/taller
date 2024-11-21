from django.urls import path
from base_app.registro_usu import authview
from base_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),

    path("home", views.index, name="index"),
    path("productos/", views.productos, name="productos"),
    path("productos/<str:categoria>/", views.productos_filtrados, name="productos_filtrados"),
    path("producto/<int:id>", views.detalle_producto, name="detalle_producto"),
    path("publicar/", views.publicar, name="publicar"),

    path("registro_usuario/", authview.registro),
    path("login/", authview.loginpage ),
    path("logout/", authview.logoutpage, name="logout"),

    path("perfil_usu/", views.perfil_usuario, name="perfil_usu"),
    path("editar_perfil/", authview.editar_perfil, name="editar_perfil"),
    path("editar_cont/", authview.editar_cont, name="editar_cont"),

    path("x/", views.x, name="x"),
    path('terminos_condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
    path('politicas_privacidad/', views.politicas_privacidad, name='politicas_privacidad'),
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),

    path('formulario_contacto/', views.contacto, name='formulario_contacto'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)