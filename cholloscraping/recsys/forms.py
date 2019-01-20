from django import forms

class UserForm(forms.Form):
    id = forms.CharField(label='Usuario ID')

class ProductForm(forms.Form):
    id = forms.CharField(label='Producto SKU')