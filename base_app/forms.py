from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from base_app.models import Perfil

from base_app.utils import get_marcas, get_condiciones, get_categorias


class PublicarProductoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=50)
    descripcion = forms.CharField(
        label="Descripción",
        max_length=500,
        widget=forms.Textarea
    )
    precio = forms.DecimalField(
        label="Precio",
        max_digits=10,
        decimal_places=2
    )
    descuento = forms.DecimalField(
        label="Descuento",
        max_digits=5,
        decimal_places=2,
        required=False
    )
    imagenes = forms.FileField(
        label="Imágenes",
        widget=forms.FileInput(attrs={'multiple': False}),
        required=False
    )

    marca = forms.ChoiceField(label="Marca", choices=get_marcas)
    categoria = forms.ChoiceField(label="Categoría", choices=get_categorias)
    condicion_producto = forms.ChoiceField(label="Condición del producto", choices=get_condiciones)

class Form_Usu_Regis(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un Email'})
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer Nombre'})
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos. letras, dígitos y @/./+/-/_ unicamente.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Ingrese Contraseña'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Tu contraseña no debe ser similar a su información personal anterior.</li>'
            '<li>Tu contraseña debe contener al menos 8 caracteres.</li>'
            '<li>Tu contraseña no debe ser una facilmente hackeable.</li>'
            '<li>Tu contraseña no puede ser enteramente numérica.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Ingrese Contraseña'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña anterior. Por verificación.</small></span>'



class Edit_Usu(UserChangeForm):
    password = None #ocultar password
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un Email'})
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer Nombre'})
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos. letras, dígitos y @/./+/-/_ unicamente.</small></span>'

class Usu_Info_Form(forms.ModelForm):
    tfno = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fono'}))
    pais = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}))
    region = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Región'}))
    ciu = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}))
    


    class Meta:
        model = Perfil
        fields = ("tfno", "pais", "region", "ciu")

    def clean_fecha_nac(self):
        fecha_nac = self.cleaned_data.get('fecha_nac')
        if not fecha_nac:
            raise forms.ValidationError('Este campo es obligatorio.')
        return fecha_nac


class Edit_Cont(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese Contraseña'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Tu contraseña no debe ser similar a su información personal anterior.</li>'
            '<li>Tu contraseña debe contener al menos 8 caracteres.</li>'
            '<li>Tu contraseña no debe ser una facilmente hackeable.</li>'
            '<li>Tu contraseña no puede ser enteramente numérica.</li>'
            '</ul>'
        )

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Ingrese Contraseña'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña anterior. Por verificación.</small></span>'

        