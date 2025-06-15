from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Artigo, Categoria, Usuario, SolicitacaoRedator, Comentario, Curtida, SolicitacaoArtigo
from .forms import ArtigoForm, CustomUserCreationForm, CategoriaForm

# Funções de verificação de permissão (devem estar no topo)
def is_admin(user):
    return user.is_authenticated and user.is_admin()

def is_redator_or_admin(user):
    return user.is_authenticated and (user.is_redator() or user.is_admin())

def is_leitor_or_above(user):
    return user.is_authenticated and (user.is_leitor() or user.is_redator() or user.is_admin())

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

@login_required
@user_passes_test(is_redator_or_admin)
def artigo_create(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            # Se não for admin, o artigo não é publicado automaticamente
            if not request.user.is_admin():
                artigo.publicado = False
            artigo.save()
            form.save_m2m()
            
            if artigo.publicado:
                messages.success(request, 'Artigo criado e publicado com sucesso!')
            else:
                messages.success(request, 'Artigo enviado para aprovação!')
                
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

@login_required
@user_passes_test(is_admin)
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    
    return render(request, 'blog/categoria_create.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categoria_detail', pk=categoria.pk)
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'blog/categoria_form.html', {'form': form, 'categoria': categoria})

@login_required
@user_passes_test(is_admin)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso!')
        return redirect('categoria_list')
    return render(request, 'blog/categoria_confirm_delete.html', {'categoria': categoria})

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
        acao = request.POST.get('acao')
        
        print(f"DEBUG: solicitacao_id={solicitacao_id}, acao={acao}")  # Debug
        
        try:
            solicitacao = SolicitacaoRedator.objects.get(id=solicitacao_id)
            
            if acao == 'aprovar':
                # Chama o método aprovar da solicitação
                resultado = solicitacao.aprovar(request.user)
                if resultado:
                    messages.success(request, f'Solicitação de {solicitacao.usuario.username} aprovada com sucesso! Usuário agora é redator.')
                else:
                    messages.error(request, 'Erro ao aprovar solicitação. Verifique suas permissões.')
            elif acao == 'rejeitar':
                usuario_nome = solicitacao.usuario.username
                solicitacao.delete()
                messages.success(request, f'Solicitação de {usuario_nome} rejeitada.')
            else:
                messages.error(request, 'Ação inválida.')
                
        except SolicitacaoRedator.DoesNotExist:
            messages.error(request, 'Solicitação não encontrada.')
        except Exception as e:
            print(f"DEBUG: Erro na aprovação: {e}")  # Debug
            messages.error(request, f'Erro interno: {str(e)}')
            
        return redirect('solicitacoes_redator')
    
    return render(request, 'blog/solicitacoes_redator.html', {'solicitacoes': solicitacoes})

@login_required
@user_passes_test(is_admin)
def solicitacoes_artigo(request):
    artigos_pendentes = Artigo.objects.filter(publicado=False).order_by('-data_criacao')

    if request.method == 'POST':
        artigo_id = request.POST.get('artigo_id')
        acao = request.POST.get('acao')
        
        try:
            artigo = Artigo.objects.get(id=artigo_id)
            
            if acao == 'aprovar':
                artigo.publicado = True
                artigo.save()
                messages.success(request, f'Artigo "{artigo.titulo}" aprovado e publicado!')
            elif acao == 'rejeitar':
                titulo_artigo = artigo.titulo
                artigo.delete()
                messages.success(request, f'Artigo "{titulo_artigo}" foi rejeitado e removido.')
                
        except Artigo.DoesNotExist:
            messages.error(request, 'Artigo não encontrado.')
            
        return redirect('solicitacoes_artigo')

    return render(request, 'blog/solicitacoes_artigo.html', {'artigos_pendentes': artigos_pendentes})

@login_required
def comentario_create(request, artigo_pk):
    artigo = get_object_or_404(Artigo, pk=artigo_pk, publicado=True)
    
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo:
            Comentario.objects.create(
                artigo=artigo,
                autor=request.user,
                conteudo=conteudo
            )
            messages.success(request, 'Comentário adicionado com sucesso!')
        else:
            messages.error(request, 'O comentário não pode estar vazio.')
    
    return redirect('artigo_detail', pk=artigo_pk)

@login_required
@user_passes_test(is_leitor_or_above)
def comentario_update(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    
    # Só permite editar se for o autor do comentário ou admin
    if request.user != comentario.autor and not request.user.is_admin():
        messages.error(request, 'Você não tem permissão para editar este comentário.')
        return redirect('artigo_detail', pk=comentario.artigo.pk)
    
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo:
            comentario.conteudo = conteudo
            comentario.save()
            messages.success(request, 'Comentário atualizado com sucesso!')
        else:
            messages.error(request, 'O comentário não pode estar vazio.')
        return redirect('artigo_detail', pk=comentario.artigo.pk)
    
    return render(request, 'blog/comentario_form.html', {'comentario': comentario})

@login_required
def comentario_delete(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    
    # Só permite deletar se for o autor do comentário ou admin
    if request.user != comentario.autor and not request.user.is_admin():
        messages.error(request, 'Você não tem permissão para deletar este comentário.')
        return redirect('artigo_detail', pk=comentario.artigo.pk)
    
    artigo_pk = comentario.artigo.pk
    if request.method == 'POST':
        comentario.delete()
        messages.success(request, 'Comentário removido com sucesso!')
        return redirect('artigo_detail', pk=artigo_pk)
    
    return render(request, 'blog/comentario_confirm_delete.html', {'comentario': comentario})

@login_required
def curtir_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    Curtida.objects.get_or_create(artigo=artigo, usuario=request.user)
    return redirect('artigo_detail', pk=pk)

@login_required
def solicitar_redator(request):
    # Verifica se já existe uma solicitação pendente
    if SolicitacaoRedator.objects.filter(usuario=request.user, aprovada=False).exists():
        messages.warning(request, 'Você já possui uma solicitação pendente.')
        return redirect('index')
    
    # Verifica se o usuário já é redator ou admin
    if request.user.is_redator() or request.user.is_admin():
        messages.warning(request, 'Você já possui permissões de redator ou superior.')
        return redirect('index')
    
    if request.method == 'POST':
        motivacao = request.POST.get('motivacao')
        if motivacao:
            SolicitacaoRedator.objects.create(
                usuario=request.user,
                motivacao=motivacao
            )
            messages.success(request, 'Sua solicitação foi enviada e está aguardando aprovação!')
            return redirect('index')
        else:
            messages.error(request, 'Por favor, informe a motivação para se tornar redator.')
    
    return render(request, 'blog/solicitar_redator.html')