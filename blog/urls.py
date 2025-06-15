from django.urls import path
from . import views

urlpatterns = [
    # URLs principais
    path('', views.index, name='index'),
    path('artigos/', views.artigo_list, name='artigo_list'),
    path('artigo/<int:pk>/', views.artigo_detail, name='artigo_detail'),
    path('artigo/novo/', views.artigo_create, name='artigo_create'),
    path('artigo/<int:pk>/editar/', views.artigo_update, name='artigo_update'),
    path('artigo/<int:pk>/deletar/', views.artigo_delete, name='artigo_delete'),
    
    # URLs de interação com artigos
    path('artigo/<int:artigo_pk>/comentar/', views.comentario_create, name='comentario_create'),
    path('comentario/<int:pk>/editar/', views.comentario_update, name='comentario_update'),
    path('comentario/<int:pk>/deletar/', views.comentario_delete, name='comentario_delete'),
    path('artigo/<int:pk>/curtir/', views.curtir_artigo, name='curtir_artigo'),
    
    # URLs de categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categoria/<int:categoria_id>/', views.categoria_detail, name='categoria_detail'),
    path('categoria/nova/', views.categoria_create, name='categoria_create'),
    path('categoria/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categoria/<int:pk>/deletar/', views.categoria_delete, name='categoria_delete'),
    
    # URLs de autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # URLs de solicitações
    path('solicitar-redator/', views.solicitar_redator, name='solicitar_redator'),
    path('solicitacoes-redator/', views.solicitacoes_redator, name='solicitacoes_redator'),
    path('solicitacoes-artigo/', views.solicitacoes_artigo, name='solicitacoes_artigo'),
]