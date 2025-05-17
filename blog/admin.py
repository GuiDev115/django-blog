from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, SolicitacaoRedator, Categoria, 
    Artigo, Comentario, Curtida, Recomendacao
)

# Personalizar o admin do usuário
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Tipo de Usuário', {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Tipo de Usuário', {'fields': ('tipo_usuario',)}),
    )


class SolicitacaoRedatorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_solicitacao', 'aprovada', 'data_aprovacao', 'aprovada_por')
    list_filter = ('aprovada',)
    search_fields = ('usuario__username', 'usuario__email')
    actions = ['aprovar_solicitacoes']
    
    def aprovar_solicitacoes(self, request, queryset):
        for solicitacao in queryset.filter(aprovada=False):
            solicitacao.aprovar(request.user)
        self.message_user(request, f"{queryset.count()} solicitação(ões) aprovada(s) com sucesso.")
    aprovar_solicitacoes.short_description = "Aprovar solicitações selecionadas"


class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao', 'publicado')
    list_filter = ('publicado', 'autor__tipo_usuario', 'categorias')
    search_fields = ('titulo', 'conteudo', 'autor__username')
    date_hierarchy = 'data_criacao'
    filter_horizontal = ('categorias',)  # Adiciona um widget mais amigável para selecionar categorias


class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'autor', 'data_criacao')
    list_filter = ('autor__tipo_usuario',)
    search_fields = ('conteudo', 'autor__username', 'artigo__titulo')


class CurtidaAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'usuario', 'data_criacao')
    list_filter = ('data_criacao',)
    search_fields = ('usuario__username', 'artigo__titulo')


class RecomendacaoAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'redator', 'data_recomendacao')
    list_filter = ('data_recomendacao',)
    search_fields = ('redator__username', 'artigo__titulo', 'comentario')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)


# Registrar os modelos no admin
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(SolicitacaoRedator, SolicitacaoRedatorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Artigo, ArtigoAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Curtida, CurtidaAdmin)
admin.site.register(Recomendacao, RecomendacaoAdmin)