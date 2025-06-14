from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # URLs principais

    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('artigos/', views.artigo_list, name='artigo_list'),
    path('artigo/<int:pk>/', views.artigo_detail, name='artigo_detail'),
    path('artigo/novo/', views.artigo_create, name='artigo_create'),
    path('artigo/<int:pk>/editar/', views.artigo_update, name='artigo_update'),
    path('artigo/<int:pk>/deletar/', views.artigo_delete, name='artigo_delete'),
    path('solicitacoes_redator/', views.solicitacoes_redator, name='solicitacoes_redator'),
    path('artigo/<int:pk>/comentar/', views.comentar_artigo, name='comentar_artigo'),
    path('artigo/<int:pk>/curtir/', views.curtir_artigo, name='curtir_artigo'),

    
    # URLs de categorias
    path('categoria/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categoria/<int:categoria_id>/', views.categoria_detail, name='categoria_detail'),
    
    # URLs de autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    
]