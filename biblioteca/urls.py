from django.urls import path
from . import views
from .views import (bibliotecaFormView,bibliotecaListView,bibliotecaDetailView,bibliotecaDeleteView, Adicionarlivro, categoriaListView,categoriaDetailView, categoriaDeleteView, bibliotecaUpdateView,categoriaUpdateView,AdicionarCategoriaView
)

app_name = 'livros'

urlpatterns = [
    path('', bibliotecaFormView.as_view(), name='pesquisar'), 
    path('adicionar/', Adicionarlivro.as_view(), name='adicionar_livro'), 
    path('lista-livros/', bibliotecaListView.as_view(), name='listar_livros'), 
    path('<int:pk>/detalhes-livro', bibliotecaDetailView.as_view(), name='detalhe_livro'), 
    path('<int:pk>/deletar-livro/', bibliotecaDeleteView.as_view(), name='deletar_livro'), 
    path('<int:pk>/alterar-categoria/', bibliotecaUpdateView.as_view(), name='alterar_categoria'),
    
    path('adicionar-categoria/', AdicionarCategoriaView.as_view(), name='adicionar_categoria'), 
    path('listar-categorias/', categoriaListView.as_view(), name='listar_categorias'),
    path('<int:pk>/detalhes-categoria', categoriaDetailView.as_view(), name='ver_categoria'),
    path('<int:pk>/deletar-categoria/', categoriaDeleteView.as_view(), name='deletar_categoria'),
    path('<int:pk>/alterar-nome-categoria/', categoriaUpdateView.as_view(), name='editar_categoria'),
]
