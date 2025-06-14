from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artigo, Categoria, Usuario
from .forms import ArtigoForm, CustomUserCreationForm

def index(request):
    artigos = Artigo.objects.all()
    return render(request, 'blog/artigo_list.html', {'artigos': artigos})

def artigo_list(request):
    artigos = Artigo.objects.all()
    return render(request, 'blog/artigo_list.html', {'artigos': artigos})

def artigo_detail(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    return render(request, 'blog/artigo_detail.html', {'artigo': artigo})

@login_required
def artigo_create(request):
    if not request.user.is_redator and not request.user.is_admin:
        return render(request, 'blog/erro_permissao.html', status=403)
    if request.method == 'POST':
        form = ArtigoForm(request.POST)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            form.save_m2m()  # Para salvar categorias many-to-many
            return redirect('artigo_list')
    else:
        form = ArtigoForm()
    return render(request, 'blog/artigo_form.html', {'form': form})

@login_required
def artigo_update(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if not (request.user.is_admin or (request.user.is_redator and artigo.autor == request.user)):
        return render(request, 'blog/erro_permissao.html', status=403)
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
    if not (request.user.is_admin or (request.user.is_redator and artigo.autor == request.user)):
        return render(request, 'blog/erro_permissao.html', status=403)
    if request.method == 'POST':
        artigo.delete()
        return redirect('artigo_list')
    return render(request, 'blog/artigo_confirm_delete.html', {'artigo': artigo})

def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'blog/categoria_list.html', {'categorias': categorias})

def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    artigos = Artigo.objects.filter(categorias=categoria)
    return render(request, 'blog/categoria_detail.html', {'categoria': categoria, 'artigos': artigos})

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