from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class Usuario(AbstractUser):
    """
    Modelo personalizado de usuário com campo para tipo de usuário
    """
    LEITOR = 'leitor'
    REDATOR = 'redator'
    ADMIN = 'admin'
    
    TIPO_USUARIO_CHOICES = [
        (LEITOR, 'Leitor'),
        (REDATOR, 'Redator'),
        (ADMIN, 'Administrador'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default=LEITOR,
    )
    
    # Para compatibilidade com AbstractUser
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='blog_users',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='blog_users',
        related_query_name='user',
    )
    
    def is_leitor(self):
        return self.tipo_usuario == self.LEITOR
        
    def is_redator(self):
        return self.tipo_usuario == self.REDATOR
    
    def is_admin(self):
        return self.tipo_usuario == self.ADMIN
    
    def pode_criar_artigo(self):
        """Verifica se o usuário pode criar artigos"""
        return self.is_redator() or self.is_admin()
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class SolicitacaoRedator(models.Model):
    """
    Modelo para representar solicitações de usuários para se tornarem redatores
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitacoes')
    motivacao = models.TextField(verbose_name='Motivação')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    aprovada = models.BooleanField(default=False)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    aprovada_por = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='solicitacoes_aprovadas'
    )
    
    def aprovar(self, admin_usuario):
        """Método para aprovar uma solicitação de redator"""
        if admin_usuario.is_admin:
            self.aprovada = True
            self.data_aprovacao = timezone.now()
            self.aprovada_por = admin_usuario
            self.save()
            
            # Atualiza o tipo de usuário para redator
            self.usuario.tipo_usuario = Usuario.REDATOR
            self.usuario.save()
            return True
        return False
    
    class Meta:
        verbose_name = 'Solicitação de Redator'
        verbose_name_plural = 'Solicitações de Redator'


class Categoria(models.Model):
    """Categoria para classificar os artigos"""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Artigo(models.Model):
    """Modelo para representar artigos no blog"""
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='artigos')
    categorias = models.ManyToManyField(Categoria, related_name='artigos')
    
    def __str__(self):
        return self.titulo
    
    #funcao para impedir no usuario de criar artigo 
    def save(self, *args, **kwargs):
        """Sobrescreve o método save para validar permissões"""
        if not self.autor.pode_criar_artigo():
            raise PermissionDenied("Usuário não tem permissão para criar artigos.")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'
        ordering = ['-data_criacao']


class Comentario(models.Model):
    """Modelo para comentários em artigos"""
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comentário por {self.autor.username} em {self.artigo.titulo}'
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-data_criacao']


class Curtida(models.Model):
    """Modelo para curtidas em artigos"""
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='curtidas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='curtidas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Curtida'
        verbose_name_plural = 'Curtidas'
        unique_together = ('artigo', 'usuario') # só pode curtir um artigo uma vez


class Recomendacao(models.Model):
    """Modelo para recomendações de artigos feitas por redatores"""
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='recomendacoes')
    redator = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recomendacoes')
    data_recomendacao = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Recomendação'
        verbose_name_plural = 'Recomendações'
        # Um redator só pode recomendar um artigo uma vez
        unique_together = ('artigo', 'redator')