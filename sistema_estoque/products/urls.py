from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('listagem/', views.listagem_view, name='listagem'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('categorias/', views.categorias_view, name='categorias'),
    path('fornecedores/', views.fornecedores_view, name='fornecedores'),
    path('movimentacao/', views.movimentacao_view, name='movimentacao'),
]