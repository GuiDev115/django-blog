from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Artigo, Categoria, Usuario, SolicitacaoRedator, Comentario, Curtida, SolicitacaoArtigo

from .forms import ArtigoForm, CustomUserCreationForm, CategoriaForm

def index(request):
    artigos = Artigo.objects.filter(publicado=True).order_by('-data_criacao')
    return render(request, 'blog/index.html', {'artigos': artigos})

def post_detail(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk, publicado=True)
    return render(request, 'blog/artigo.html', {'artigo': artigo})

def artigo_list(request):
    artigos = Artigo.objects.filter(publicado=True)
    return render(request, 'blog/artigo_list.html', {'artigos': artigos})

def artigo_detail(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    return render(request, 'blog/artigo_detail.html', {'artigo': artigo})

def is_admin(user):
    return user.is_authenticated and user.is_admin()

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

@login_required
@user_passes_test(is_admin)
def solicitacoes_redator(request):
    solicitacoes = SolicitacaoRedator.objects.filter(aprovada=False)
    if request.method == 'POST':
        solicitacao_id = request.POST.get('solicitacao_id')
        solicitacao = SolicitacaoRedator.objects.get(id=solicitacao_id)
        solicitacao.aprovar(request.user)
        return redirect('solicitacoes_redator')
    return render(request, 'blog/solicitacoes_redator.html', {'solicitacoes': solicitacoes})

@login_required

@user_passes_test(is_admin)
def solicitacoes_artigo(request):
    artigos_pendentes = Artigo.objects.filter(publicado=False).order_by('-data_criacao')

    if request.method == 'POST':
        artigo_id = request.POST.get('artigo_id')
        artigo = Artigo.objects.get(id=artigo_id)
        artigo.publicado = True
        artigo.save()
        return redirect('solicitacoes_artigo')

    return render(request, 'blog/solicitacoes_artigo.html', {'artigos': artigos_pendentes})


def comentar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo:
            Comentario.objects.create(
                artigo=artigo,
                autor=request.user,
                conteudo=conteudo
            )
    return redirect('artigo_detail', pk=pk)

@login_required
def curtir_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    Curtida.objects.get_or_create(artigo=artigo, usuario=request.user)
    return redirect('artigo_detail', pk=pk)

