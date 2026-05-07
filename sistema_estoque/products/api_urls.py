from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.produto_list, name='produto-list'),
    path('produtos/criar/', views.produto_create, name='produto-create'),
    path('produtos/<int:id>/', views.produto_detail, name='produto-detail'),
    
    path('categorias/', views.listar_categorias, name='listar-categorias'),
    path('categorias/criar/', views.criar_categoria, name='criar-categoria'),
    path('categorias/<int:id>/', views.detalhes_categoria, name='detalhes-categoria'),
    
    path('fornecedores/', views.listar_fornecedores, name='listar-fornecedores'),
    path('fornecedores/criar/', views.criar_fornecedor, name='criar-fornecedor'),
    path('fornecedores/<int:id>/', views.detalhes_fornecedor, name='detalhes-fornecedor'),
    
    path('relatorios/estoque-baixo/', views.relatorio_estoque_baixo, name='relatorio-estoque-baixo'),
]