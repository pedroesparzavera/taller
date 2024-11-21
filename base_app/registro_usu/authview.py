from django.shortcuts import render, redirect
from django.contrib import messages
from base_app.forms import Form_Usu_Regis, Edit_Usu, Edit_Cont, Usu_Info_Form
from django.contrib.auth import authenticate, login, logout

from base_app.models import Perfil

def registro(request):
    form = Form_Usu_Regis()
    if request.method == 'POST':
        form = Form_Usu_Regis(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro Exitoso! Inicie Sesión para continuar")
            return redirect('/login')
    context = {'form':form}
    return render(request, "auth/registro.html", context)

def loginpage(request):
   #if request.user.is_authenticated:
        #messages.warning(request, "Ya iniciaste sesión")
        #return redirect('/')
    #else:

    if request.method == 'POST':
        name = request.POST.get('username')
        passwd = request.POST.get('password')

        user = authenticate(request, username=name, password=passwd)

        if user is not None:
                login (request, user)
                messages.success(request, "Incio de Sesión Exitoso")
                return redirect ("/")
        else:
                messages.error(request, "Email o Contraseña inválido")
                return redirect('/login')
    return render(request, "auth/login.html")       
    
def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Cierre de Sesión Exitoso")
    return redirect('/')


def editar_perfil(request):
    # Asegúrate de que el perfil exista
    if not Perfil.objects.filter(user=request.user).exists():
        Perfil.objects.create(user=request.user)

    # Obtén las instancias del usuario y del perfil
    current_user = request.user
    current_perfil = Perfil.objects.get(user=request.user)

    # Inicializa ambos formularios
    user_form = Edit_Usu(request.POST or None, instance=current_user)
    actu_info_form = Usu_Info_Form(request.POST or None, instance=current_perfil)

    # Verifica la validez de ambos formularios
    if user_form.is_valid() and actu_info_form.is_valid():
        user_form.save()
        actu_info_form.save()

        # Actualiza la sesión con los nuevos datos del usuario
        login(request, current_user)
        messages.success(request, "Se han actualizado sus datos con éxito")
        return redirect('/perfil_usu')

    # Renderiza el formulario con los errores (si los hay)
    return render(request, 'perfil/editar_perfil.html', {
        'user_form': user_form,
        'actu_info_form': actu_info_form
    })


def editar_cont(request):
    if request.user.is_authenticated:
        current_user = request.user
        #se ha completado el formulari?
        if request.method == 'POST':
            form = Edit_Cont(current_user, request.POST)
            #is teh form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Tu contraseña ha sido cambiada con éxito. Ingrese sesión nuevamente")
                #login(request, current_user) --> para iniciar automaticamente
                return redirect('/login') 
            else: 
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('/editar_cont')

        else: 
            edit_cont_form = Edit_Cont(current_user)
            return render (request, 'perfil/editar_cont.html', {'edit_cont_form':edit_cont_form})
    else:
        messages.success(request, "Debes estár registrado para editar tu perfil")
        return redirect('/home')


    