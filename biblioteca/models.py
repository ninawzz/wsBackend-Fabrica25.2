from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Livros(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.titulo
    
    
