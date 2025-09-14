from django.urls import path
from . import views
from .views import (bibliotecaFormView,bibliotecaListView,bibliotecaDetailView,bibliotecaDeleteView, Adicionarlivro,adicionar_categoria, categoriaListView,categoriaDetailView, categoriaDeleteView, bibliotecaUpdateView,categoriaUpdateView
)

app_name = 'livros'

urlpatterns = [
    path('', bibliotecaFormView.as_view(), name='pesquisar'), # página inicial para pesquisar livros
    path('adicionar/', Adicionarlivro.as_view(), name='adicionar_livro'), # página para adicionar livro
    path('lista-livros/', bibliotecaListView.as_view(), name='listar_livros'), # página para listar todos os livros adicionados
    path('<int:pk>/detalhes-livro', bibliotecaDetailView.as_view(), name='detalhe_livro'), # página para mostrar os detalhes do livro
    path('<int:pk>/deletar-livro/', bibliotecaDeleteView.as_view(), name='deletar_livro'), # página para confirmar exclusão do livro
    path('<int:pk>/alterar-categoria/', bibliotecaUpdateView.as_view(), name='alterar_categoria'),# página para alterar categoria dos livros
    
    path('adicionar-categoria/', views.adicionar_categoria, name='adicionar_categoria'), #página para adicionar categoria
    path('listar-categorias/', categoriaListView.as_view(), name='listar_categorias'),# página para listar categorias - read / list
    path('<int:pk>/detalhes-categoria', categoriaDetailView.as_view(), name='ver_categoria'),# página para mostrar livros de uma tal categoria - read / detail
    path('<int:pk>/deletar-categoria/', categoriaDeleteView.as_view(), name='deletar_categoria'),# página para confirmar exclusão da categoria - delete
    path('<int:pk>/alterar-nome-categoria/', categoriaUpdateView.as_view(), name='editar_categoria'),
    
    # página para alterar categoria
    
]
