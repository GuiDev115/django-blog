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
    
    # URLs de categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categoria/<int:pk>/', views.categoria_detail, name='categoria_detail'),
    
    # URLs de autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]