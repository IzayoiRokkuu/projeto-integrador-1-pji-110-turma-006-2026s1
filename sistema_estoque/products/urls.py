from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.produto_list, name='produto-list'),
    path('produtos/criar/', views.produto_create, name='produto-create'),
    path('produtos/<int:id>/', views.produto_detail, name='produto-detail'),
]