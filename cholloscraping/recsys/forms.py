from django import forms

class ProductForm(forms.Form):
    id = forms.CharField(label='Producto SKU')