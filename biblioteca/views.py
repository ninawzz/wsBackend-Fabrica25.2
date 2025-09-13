from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView, DeleteView
import requests
from .models import Livros, Categoria
from .forms import bibliotecaForm

# !! Função para buscar os livros e exibir os resultados - Não salva no banco
class bibliotecaFormView(FormView):
    template_name = 'home.html'
    form_class = bibliotecaForm
    success_url = reverse_lazy("livros:list")
    
    def form_valid(self,form):
        titulo = form.cleaned_data['titulo']
        url = f'https://www.googleapis.com/books/v1/volumes?q={titulo}&langRestrict=pt'
        response = requests.get(url)
        resultado = []
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])[:5]  
            for item in items:
                info = item.get('volumeInfo', {})
                resultado.append({
                    'titulo': info.get('title', 'Desconhecido'),
                    'autor': ", ".join(info.get('authors', ['Desconhecido'])),
                    'data': info.get('publishedDate', 'Não possui'),
                    'descricao': info.get('description', 'Sem descrição.')
                })

            return render(self.request, 'home.html', {'resultados': resultado, 'form': form})
        else:
            return f'erro: {response.status_code}'
        
  
        
# !! Função pra adicionar o livro no banco, Create, Read - list e detail, Delete
class Adicionarlivro(FormView):
    template_name = 'confirmacao.html'
    form_class = bibliotecaForm
    success_url = reverse_lazy("livros:list")

    def get_initial(self):
        return {
            'titulo': self.request.GET.get('titulo', ''),
            'autor': self.request.GET.get('autor', ''),
            'data': self.request.GET.get('data', ''),
            'descricao': self.request.GET.get('descricao', ''),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['titulo'] = self.request.GET.get('titulo', '')
        context['autor'] = self.request.GET.get('autor', '')
        context['data'] = self.request.GET.get('data', '')
        context['descricao'] = self.request.GET.get('descricao', '')
        context['categorias'] = Categoria.objects.all() 
        return context

    def form_valid(self, form):
        categoria_id = self.request.POST.get('categoria')
        categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None

        Livros.objects.create(
            titulo=form.cleaned_data.get('titulo') or self.request.GET.get('titulo'),
            autor=form.cleaned_data.get('autor')or self.request.GET.get('autor'),
            data=form.cleaned_data.get('data')or self.request.GET.get('data'),
            descricao=form.cleaned_data.get('descricao') or self.request.GET.get('descricao'),
            categoria=categoria
        )
        return super().form_valid(form)
    
class bibliotecaListView(ListView):
    model = Livros
    template_name = 'biblioteca_listview.html'
    context_object_name = 'livros'
    
class bibliotecaDetailView(DetailView):
    model = Livros
    template_name = 'biblioteca_detailview.html'
    context_object_name = 'livro'
    
class bibliotecaDeleteView(DeleteView):
    model = Livros
    template_name = 'biblioteca_deleteview.html'
    context_object_name = 'livro'
    success_url = reverse_lazy("livros:list")
    
# !! função pro usuário adicionar manualmente a categoria
def adicionar_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            Categoria.objects.create(nome=nome)
        return redirect('livros:pesquisar')  
    return render(request, 'categoria/adicionar_categoria.html')

class categoriaListView(ListView): # ?? Read - list
    model = Categoria
    template_name = 'biblioteca_listview.html'
    context_object_name = 'livros'
    
class categoriaDetailView(DetailView): # ?? Read - detail
    model = Categoria
    template_name = 'biblioteca_listview.html'
    context_object_name = 'livros'
      