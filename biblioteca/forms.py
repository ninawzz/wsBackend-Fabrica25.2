from django import forms
from .models import Livros, Categoria

class bibliotecaForm(forms.ModelForm):
    class Meta:
        model = Livros
        fields = ['titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Digite o nome do livro:',
                'class': 'form-control'
            }),
        }
        labels = {
            'titulo': 'Nome do livro',
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        labels = {
            'nome': 'Nome da categoria'
        }
