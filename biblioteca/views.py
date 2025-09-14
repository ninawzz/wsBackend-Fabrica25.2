from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView, DeleteView, UpdateView
from django.db import IntegrityError
from django.views import View
import requests
from .models import Livros, Categoria
from .forms import bibliotecaForm, CategoriaForm


class bibliotecaFormView(FormView): 
    template_name = 'livros/home.html'
    form_class = bibliotecaForm
    success_url = reverse_lazy("livros:listar_livros")
    
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

            return render(self.request, 'livros/home.html', {'resultados': resultado, 'form': form})
        else:
            return f'erro: {response.status_code}'
        

 # * SEÇÂO ADICIONAR LIVROS
 
class Adicionarlivro(FormView): 
    template_name = 'livros/confirmacao.html'
    form_class = bibliotecaForm
    success_url = reverse_lazy("livros:listar_livros")
    
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
    template_name = 'livros/biblioteca_listview.html'
    context_object_name = 'livros'
    
class bibliotecaDetailView(DetailView): 
    model = Livros
    template_name = 'livros/biblioteca_detailview.html'
    context_object_name = 'livro'
    
class bibliotecaDeleteView(DeleteView): 
    model = Livros
    template_name = 'livros/biblioteca_deleteview.html'
    context_object_name = 'livro'
    success_url = reverse_lazy("livros:listar_livros")
    
class bibliotecaUpdateView(UpdateView): 
    model = Livros
    fields = ['categoria']
    template_name = 'livros/biblioteca_updateview.html'
    context_object_name = 'livro'
    success_url = reverse_lazy("livros:listar_livros")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
    
# * SEÇÂO CATEGORIA

class AdicionarCategoriaView(View):
    template_name = 'categoria/adicionar_categoria.html'

    def get(self, request):
        # Mostra o formulário vazio
        return render(request, self.template_name)

    def post(self, request):
        # Pega o valor do input
        nome = request.POST.get('nome', '').strip()

        if not nome:
            return render(request, self.template_name, {"erro": "O nome não pode estar vazio."})

        try:
            # Tenta salvar no banco
            Categoria.objects.create(nome=nome)
        except IntegrityError:
            # Se já existir, mostra erro
            return render(request, self.template_name, {"erro": f'A categoria "{nome}" já existe.'})

        # Se der certo, redireciona
        return redirect('livros:listar_categorias')
    

class categoriaListView(ListView): 
    model = Categoria
    template_name = 'categoria/categoria_listview.html'
    context_object_name = 'categorias'
    
class categoriaDetailView(DetailView): 
    model = Categoria
    template_name = 'categoria/categoria_detailview.html'
    context_object_name = 'categoria'
    
class categoriaUpdateView(UpdateView): 
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/categoria_updateview.html'
    success_url = reverse_lazy('livros:listar_categorias')
    
class categoriaDeleteView(DeleteView): 
    model = Categoria
    template_name = 'categoria/categoria_deleteview.html'
    context_object_name = 'categoria'
    success_url = reverse_lazy('livros:listar_categorias')
    
      