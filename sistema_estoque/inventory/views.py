from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from products.models import Produto
from .models import Movimentacao
import json

@csrf_exempt
def entrada_produto(request):
    """Registrar entrada de produtos no estoque"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Buscar o produto
            produto = get_object_or_404(Produto, id=data['produto_id'])
            
            # Buscar o usuário (por enquanto, pega o primeiro admin)
            usuario = User.objects.filter(is_superuser=True).first()
            
            # Registrar movimentação
            movimentacao = Movimentacao.objects.create(
                produto=produto,
                usuario=usuario,
                tipo='Entrada',
                quantidade=data['quantidade'],
                observacao=data.get('observacao', '')
            )
            
            # Atualizar estoque do produto
            produto.quantidade_atual += data['quantidade']
            produto.save()
            
            return JsonResponse({
                'id': movimentacao.id,
                'message': 'Entrada registrada com sucesso!',
                'novo_estoque': produto.quantidade_atual
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@csrf_exempt
def saida_produto(request):
    """Registrar saída de produtos do estoque"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Buscar o produto
            produto = get_object_or_404(Produto, id=data['produto_id'])
            
            # Validar se há estoque suficiente
            if produto.quantidade_atual < data['quantidade']:
                return JsonResponse({
                    'error': f'Estoque insuficiente. Disponível: {produto.quantidade_atual}'
                }, status=400)
            
            # Buscar o usuário
            usuario = User.objects.filter(is_superuser=True).first()
            
            # Registrar movimentação
            movimentacao = Movimentacao.objects.create(
                produto=produto,
                usuario=usuario,
                tipo='Saida',
                quantidade=data['quantidade'],
                observacao=data.get('observacao', '')
            )
            
            # Atualizar estoque do produto
            produto.quantidade_atual -= data['quantidade']
            produto.save()
            
            return JsonResponse({
                'id': movimentacao.id,
                'message': 'Saída registrada com sucesso!',
                'novo_estoque': produto.quantidade_atual
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)


def listar_movimentacoes(request):
    """Listar todas as movimentações"""
    if request.method == 'GET':
        movimentacoes = Movimentacao.objects.all().order_by('-data')
        data = [{
            'id': m.id,
            'produto': m.produto.nome,
            'produto_id': m.produto.id,
            'tipo': m.tipo,
            'quantidade': m.quantidade,
            'usuario': m.usuario.username,
            'data': m.data.strftime('%d/%m/%Y %H:%M'),
            'observacao': m.observacao
        } for m in movimentacoes]
        return JsonResponse(data, safe=False)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)


def movimentacoes_por_produto(request, produto_id):
    """Listar movimentações de um produto específico"""
    if request.method == 'GET':
        produto = get_object_or_404(Produto, id=produto_id)
        movimentacoes = Movimentacao.objects.filter(produto=produto).order_by('-data')
        
        data = [{
            'id': m.id,
            'tipo': m.tipo,
            'quantidade': m.quantidade,
            'usuario': m.usuario.username,
            'data': m.data.strftime('%d/%m/%Y %H:%M'),
            'observacao': m.observacao
        } for m in movimentacoes]
        
        return JsonResponse({
            'produto': produto.nome,
            'estoque_atual': produto.quantidade_atual,
            'movimentacoes': data
        })
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)