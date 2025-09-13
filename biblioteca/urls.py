from django.urls import path
from . import views
from .views import (
    bibliotecaFormView,
    bibliotecaListView,
    bibliotecaDetailView,
    bibliotecaDeleteView, Adicionarlivro,adicionar_categoria
)

app_name = 'livros'

urlpatterns = [
    path('', bibliotecaFormView.as_view(), name='pesquisar'),
    path('lista/', bibliotecaListView.as_view(), name='list'),
    path('<int:pk>/', bibliotecaDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', bibliotecaDeleteView.as_view(), name='delete'),
    path('confirmar/', Adicionarlivro.as_view(), name='confirmar'),
    path('categoria/adicionar/', views.adicionar_categoria, name='adicionar_categoria'),
]
