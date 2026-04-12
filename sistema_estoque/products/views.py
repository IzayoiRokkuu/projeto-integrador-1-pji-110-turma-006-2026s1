from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Produto, Categoria, Fornecedor
import json

def produto_list(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        data = [{
            'id': p.id,
            'nome': p.nome,
            'codigo': p.codigo,
            'preco': str(p.preco),
            'quantidade_atual': p.quantidade_atual,
            'estoque_minimo': p.estoque_minimo,
            'categoria': p.categoria.nome if p.categoria else None,
            'fornecedor': p.fornecedor.nome if p.fornecedor else None
        } for p in produtos]
        return JsonResponse(data, safe=False)

@csrf_exempt
def produto_detail(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    if request.method == 'GET':
        data = {
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'codigo': produto.codigo,
            'preco': str(produto.preco),
            'quantidade_atual': produto.quantidade_atual,
            'estoque_minimo': produto.estoque_minimo,
            'categoria_id': produto.categoria.id if produto.categoria else None,
            'fornecedor_id': produto.fornecedor.id if produto.fornecedor else None
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        produto.nome = data.get('nome', produto.nome)
        produto.descricao = data.get('descricao', produto.descricao)
        produto.preco = data.get('preco', produto.preco)
        produto.estoque_minimo = data.get('estoque_minimo', produto.estoque_minimo)
        
        if 'categoria_id' in data:
            produto.categoria = get_object_or_404(Categoria, id=data['categoria_id'])
        if 'fornecedor_id' in data:
            produto.fornecedor = get_object_or_404(Fornecedor, id=data['fornecedor_id'])
        
        produto.save()
        return JsonResponse({'message': 'Produto atualizado com sucesso!'})
    
    elif request.method == 'DELETE':
        produto.delete()
        return JsonResponse({'message': 'Produto excluído com sucesso!'})

@csrf_exempt
def produto_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        produto = Produto.objects.create(
            nome=data['nome'],
            codigo=data['codigo'],
            preco=data['preco'],
            descricao=data.get('descricao', ''),
            quantidade_atual=data.get('quantidade_atual', 0),
            estoque_minimo=data.get('estoque_minimo', 0),
            categoria_id=data.get('categoria_id') if data.get('categoria_id') else None,
            fornecedor_id=data.get('fornecedor_id') if data.get('fornecedor_id') else None
        )
        
        return JsonResponse({
            'id': produto.id,
            'message': 'Produto cadastrado com sucesso!'
        }, status=201)
    
def listagem_view(request):
    return render(request, 'products/listagem.html')

def cadastro_view(request):
    return render(request, 'products/cadastro.html')

def listar_categorias(request):
    """Retorna lista de categorias para o frontend"""
    categorias = Categoria.objects.all()
    data = [{'id': c.id, 'nome': c.nome} for c in categorias]
    return JsonResponse(data, safe=False)