from django import forms
from .models import Livros

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
