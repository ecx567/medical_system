from django import forms
from aplication.core.models import Paciente, Doctor, Especialidad
from django.utils import timezone
import datetime
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from aplication.security.models import User
from django.db import models
from django.forms import ImageField, FileInput
from django.contrib.auth.forms import PasswordChangeForm
from doctor.utils import valida_cedula
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(forms.Form):
    username = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
  dni = forms.CharField(max_length=10, label="DNI", validators=[valida_cedula])
  first_name = forms.CharField(max_length=30, label="Nombres")
  last_name = forms.CharField(max_length=150, label="Apellidos")
  phone = forms.CharField(max_length=10, required=False, label="Celular")
  email = forms.EmailField(required=True, label="Correo electrónico")
  image = forms.ImageField(required=False, label="Foto de perfil", widget=FileInput(attrs={
    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
  }))

  class Meta(UserCreationForm.Meta):
    model = User
    fields = [
      "username",
      "first_name",
      "last_name",
      "dni",
      "phone",
      "email",
      "image",
      "password1",
      "password2",
    ]


class CustomUserUpdateForm(forms.ModelForm):
  password = None

  # def clean_dni(self):
  #   dni = self.cleaned_data['dni']
  #   if not valida_cedula(dni):
  #       raise forms.ValidationError("La cédula ingresada no es válida.")
  #   return dni

  image = ImageField(widget=FileInput(attrs={
    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
  }))

  class Meta:
    model = User
    fields = ["first_name", "last_name", "dni", "phone", "email", "image"]
    error_messages = {
      "dni": {
        "unique": "Ya existe un usuario con este DNI.",
      },
      "phone": {
        "unique": "Ya existe un usuario con este número de celular.",
      },
      "email": {
        "unique": "Ya existe un usuario con este correo electrónico.",
      },
    }
    widgets = {
      "first_name": forms.TextInput(
        attrs={
          "placeholder": "Ingrese nombres del usuario",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "last_name": forms.TextInput(
        attrs={
          "placeholder": "Ingrese apellidos del usuario",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "dni": forms.TextInput(
        attrs={
          "placeholder": "Ingrese DNI del usuario",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "phone": forms.TextInput(
        attrs={
          "placeholder": "Ingrese número celular del usuario",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      "email": forms.EmailInput(
        attrs={
          "placeholder": "Ingrese correo electrónico del usuario",
          "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
      ),
      # "image": forms.FileInput(
      #   attrs={
      #     "placeholder": "Ingrese correo electrónico del usuario",
      #     "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
      #   }
      # ),
    }
    labels = {
      "first_name": "Nombres",
      "last_name": "Apellidos",
      "dni": "DNI o Ruc",
      "phone": "Celular",
      "email": "Correo electrónico",
      "image": "Imagen",
    }

class CustomPasswordChangeForm(PasswordChangeForm):
  old_password = forms.CharField(
    widget=forms.PasswordInput(attrs={
      "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
      "placeholder": "Contraseña actual"
    }),
    label="Contraseña actual"
  )
  new_password1 = forms.CharField(
    widget=forms.PasswordInput(attrs={
      "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
      "placeholder": "Nueva contraseña"
    }),
    label="Nueva contraseña"
  )
  new_password2 = forms.CharField(
    widget=forms.PasswordInput(attrs={
      "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
      "placeholder": "Confirma la nueva contraseña"
    }),
    label="Confirma la nueva contraseña"
  )

# class ProductForm(forms.ModelForm):
#   class Meta:
#     model = Product
#     fields = [
#       "description",
#       "price",
#       "stock",
#       "brand",
#       "categories",
#       "line",
#       "supplier",
#       "expiration_date",
#       "image",
#       "state",
#     ]
#     error_messages = {
#       "description": {
#         "unique": "Ya existe un producto con este nombre.",
#       },
#       "supplier": {
#         "unique": "Ya existe un producto con este proveedor.",
#       },
#     }
#     widgets = {
#       "description": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese descripción del producto",
#           "id": "id_description",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "price": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese precio del producto",
#           "id": "id_price",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "stock": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese stock del producto",
#           "id": "id_stock",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "brand": forms.Select(
#         attrs={
#           "id": "id_brand",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "categories": forms.SelectMultiple(
#         attrs={
#           "id": "id_categories",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "line": forms.Select(
#         attrs={
#           "id": "id_line",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "supplier": forms.Select(
#         attrs={
#           "id": "id_supplier",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "expiration_date": forms.DateInput(
#         attrs={
#           "type": "date",
#           "id": "id_expiration_date",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "image": forms.FileInput(
#         attrs={
#           "type": "file",
#           "id": "id_image",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "state": forms.CheckboxInput(
#         attrs={
#           "id": "id_state",
#           "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
#         }
#       ),
#     }
#     labels = {
#       "description": "Producto",
#       "price": "Precio",
#       "stock": "Stock",
#       "brand": "Marca",
#       "categories": "Categoría",
#       "line": "Línea",
#       "supplier": "Proveedor",
#       "expiration_date": "Fecha de vencimiento",
#       "image": "Imagen",
#       "state": "Estado",
#     }
#
#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     if (
#       not self.instance.pk
#     ):  # Solo establecer el valor predeterminado si el objeto es nuevo
#       self.fields["expiration_date"].initial = (
#         (timezone.now() + datetime.timedelta(days=30)).date().isoformat()
#       )
#
#   def clean_description(self):
#     description = self.cleaned_data.get("description")
#     return description.upper()













#
# class BrandForm(forms.ModelForm):
#   class Meta:
#     model = Brand
#     fields = ["description", "state"]
#     error_messages = {
#       "description": {
#         "unique": "Ya existe una marca con este nombre.",
#       },
#     }
#     widgets = {
#       "description": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese descripción del producto",
#           "id": "id_description",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "state": forms.CheckboxInput(
#         attrs={
#           "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
#         }
#       ),
#     }
#     labels = {
#       "description": "Descripción ",
#       "state": "Estado",
#     }
#
#   def clean_description(self):
#     description = self.cleaned_data.get("description")
#     return description.upper()
#
#
# class SupplierForm(forms.ModelForm):
#   class Meta:
#     model = Supplier
#     fields = ["name", "ruc", "address", "phone", "state", "image"]
#     error_messages = {
#       "ruc": {
#         "unique": "Ya existe un proveedor con este RUC o DNI.",
#       },
#       "phone": {
#         "unique": "Ya existe un proveedor con este número de celular.",
#       },
#       "name": {
#         "unique": "Ya existe un proveedor con este nombre.",
#       },
#     }
#     widgets = {
#       "name": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese nombre del proveedor",
#           "id": "id_name",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "ruc": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese RUC o DNI del proveedor",
#           "id": "id_ruc",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "address": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese dirección del proveedor",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "phone": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese número celular",
#           "id": "id_phone",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "state": forms.CheckboxInput(
#         attrs={
#           "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
#         }
#       ),
#       "image": forms.FileInput(
#         attrs={
#           "type": "file",
#           "id": "id_image",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#     }
#     labels = {
#       "name": "Nombre",
#       "ruc": "Ruc o Dni",
#       "address": "Dirección",
#       "phone": "Celular",
#       "state": "Estado",
#       "image": "Imagen",
#     }
#
#   def clean_name(self):
#     name = self.cleaned_data.get("name")
#     return name.upper()
#
#
# class CategoryForm(forms.ModelForm):
#   class Meta:
#     model = Category
#     fields = ["description", "state"]
#     error_messages = {
#       "description": {
#         "unique": "Ya existe una categoría con este nombre.",
#       },
#     }
#     widgets = {
#       "description": forms.TextInput(
#         attrs={
#           "placeholder": "Ingrese descripción del producto",
#           "id": "id_description",
#           "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
#         }
#       ),
#       "state": forms.CheckboxInput(
#         attrs={
#           "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
#         }
#       ),
#     }
#     labels = {
#       "description": "Nombre",
#       "state": "Estado",
#     }
#
#   def clean_description(self):
#     description = self.cleaned_data.get("description")
#     return description.upper()