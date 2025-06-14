from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artigo, Categoria, Usuario
from .forms import ArtigoForm, CustomUserCreationForm, CategoriaForm

def index(request):
    artigos = Artigo.objects.filter(publicado=True).order_by('-data_criacao')
    return render(request, 'blog/index.html', {'artigos': artigos})

def post_detail(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk, publicado=True)
    return render(request, 'blog/artigo.html', {'artigo': artigo})

def artigo_list(request):
    artigos = Artigo.objects.all()
    return render(request, 'blog/artigo_list.html', {'artigos': artigos})

def artigo_detail(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    return render(request, 'blog/artigo_detail.html', {'artigo': artigo})

@login_required
def artigo_create(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            form.save_m2m() 
            return redirect('artigo_list')
    else:
        form = ArtigoForm()
    return render(request, 'blog/artigo_form.html', {'form': form})

@login_required
def artigo_update(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.method == 'POST':
        form = ArtigoForm(request.POST, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('artigo_detail', pk=artigo.pk)
    else:
        form = ArtigoForm(instance=artigo)
    return render(request, 'blog/artigo_form.html', {'form': form})

@login_required
def artigo_delete(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.method == 'POST':
        artigo.delete()
        return redirect('artigo_list')
    return render(request, 'blog/artigo_confirm_delete.html', {'artigo': artigo})

def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'blog/categoria_list.html', {'categorias': categorias})


def categoria_detail(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    try:
        artigos = categoria.artigo_set.all()
    except AttributeError:
        try:
            artigos = categoria.artigos.all()
        except AttributeError:
            artigos = Artigo.objects.filter(categoria=categoria)
    
    return render(request, 'blog/categoria_detail.html', {'categoria': categoria, 'artigos': artigos})


def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    
    return render(request, 'blog/categoria_create.html', {'form': form})


# Views de autenticação
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciais inválidas.')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})