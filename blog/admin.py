from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Artigo, Categoria, Comentario, Curtida, SolicitacaoRedator, Recomendacao

class UsuarioAdmin(UserAdmin):
    """Admin customizado para o modelo Usuario"""
    list_display = ('username', 'email', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Artigo)
admin.site.register(Categoria)
admin.site.register(Comentario)
admin.site.register(Curtida)
admin.site.register(SolicitacaoRedator)
admin.site.register(Recomendacao)