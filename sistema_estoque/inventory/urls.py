from django.urls import path
from . import views

urlpatterns = [
    path('movimentacoes/', views.listar_movimentacoes, name='listar-movimentacoes'),
    path('movimentacoes/entrada/', views.entrada_produto, name='entrada-produto'),
    path('movimentacoes/saida/', views.saida_produto, name='saida-produto'),
    path('movimentacoes/produto/<int:produto_id>/', views.movimentacoes_por_produto, name='movimentacoes-por-produto'),
]