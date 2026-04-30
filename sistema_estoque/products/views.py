from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import models
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

def criar_categoria(request):
    """Criar uma nova categoria"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            categoria = Categoria.objects.create(
                nome=data['nome'],
                descricao=data.get('descricao', '')
            )
            return JsonResponse({
                'id': categoria.id,
                'message': 'Categoria criada com sucesso!'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def detalhes_categoria(request, id):
    """Buscar, editar ou excluir uma categoria"""
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'GET':
        data = {'id': categoria.id, 'nome': categoria.nome, 'descricao': categoria.descricao}
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            categoria.nome = data.get('nome', categoria.nome)
            categoria.descricao = data.get('descricao', categoria.descricao)
            categoria.save()
            return JsonResponse({'message': 'Categoria atualizada com sucesso!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        categoria.delete()
        return JsonResponse({'message': 'Categoria excluída com sucesso!'})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def listar_fornecedores(request):
    """Retorna lista fornecedores para o frontend"""
    fornecedores = Fornecedor.objects.all()
    data = [{'id': f.id, 'nome': f.nome} for f in fornecedores]
    return JsonResponse(data, safe=False)

def criar_fornecedor(request):
    """Criar um novo fornecedor"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fornecedor = Fornecedor.objects.create(
                nome=data['nome'],
                cnpj=data.get('cnpj', ''),
                telefone=data.get('telefone', ''),
                email=data.get('email', '')
            )
            return JsonResponse({
                'id': fornecedor.id,
                'message': 'Fornecedor criado com sucesso!'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def detalhes_fornecedor(request, id):
    """Buscar, editar ou excluir um fornecedor"""
    fornecedor = get_object_or_404(Fornecedor, id=id)
    
    if request.method == 'GET':
        data = {
            'id': fornecedor.id,
            'nome': fornecedor.nome,
            'cnpj': fornecedor.cnpj,
            'telefone': fornecedor.telefone,
            'email': fornecedor.email
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            fornecedor.nome = data.get('nome', fornecedor.nome)
            fornecedor.cnpj = data.get('cnpj', fornecedor.cnpj)
            fornecedor.telefone = data.get('telefone', fornecedor.telefone)
            fornecedor.email = data.get('email', fornecedor.email)
            fornecedor.save()
            return JsonResponse({'message': 'Fornecedor atualizado com sucesso!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        fornecedor.delete()
        return JsonResponse({'message': 'Fornecedor excluído com sucesso!'})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def relatorio_estoque_baixo(request):
    """Retorna produtos com quantidade atual <= estoque mínimo"""
    produtos = Produto.objects.filter(quantidade_atual__lte=models.F('estoque_minimo'))
    
    data = [{
        'id': p.id,
        'nome': p.nome,
        'codigo': p.codigo,
        'quantidade_atual': p.quantidade_atual,
        'estoque_minimo': p.estoque_minimo,
        'categoria': p.categoria.nome if p.categoria else None
    } for p in produtos]
    
    return JsonResponse(data, safe=False)
