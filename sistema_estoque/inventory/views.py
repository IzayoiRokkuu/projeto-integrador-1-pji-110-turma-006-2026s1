from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from products.models import Produto
from .models import Movimentacao
from django.db.models import Sum
from datetime import datetime
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
            
            # Registrar movimentação (o save() do model atualiza o estoque)
            movimentacao = Movimentacao.objects.create(
                produto=produto,
                usuario=usuario,
                tipo='Entrada',
                quantidade=data['quantidade'],
                observacao=data.get('observacao', '')
            )
            
            # Buscar o produto atualizado novamente para pegar o novo estoque
            produto.refresh_from_db()
            
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
            
            # Validar se há estoque suficiente (antes de criar a movimentação)
            if produto.quantidade_atual < data['quantidade']:
                return JsonResponse({
                    'error': f'Estoque insuficiente. Disponível: {produto.quantidade_atual}'
                }, status=400)
            
            # Buscar o usuário
            usuario = User.objects.filter(is_superuser=True).first()
            
            # Registrar movimentação (o save() do model atualiza o estoque)
            movimentacao = Movimentacao.objects.create(
                produto=produto,
                usuario=usuario,
                tipo='Saida',
                quantidade=data['quantidade'],
                observacao=data.get('observacao', '')
            )
            
            # Buscar o produto atualizado novamente para pegar o novo estoque
            produto.refresh_from_db()
            
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


def relatorio_movimentacoes_periodo(request):
    """Retorna total de entradas e saídas em um período"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    movimentacoes = Movimentacao.objects.all()
    
    if data_inicio:
        movimentacoes = movimentacoes.filter(data__date__gte=data_inicio)
    if data_fim:
        movimentacoes = movimentacoes.filter(data__date__lte=data_fim)
    
    total_entradas = movimentacoes.filter(tipo='Entrada').aggregate(total=Sum('quantidade'))['total'] or 0
    total_saidas = movimentacoes.filter(tipo='Saida').aggregate(total=Sum('quantidade'))['total'] or 0
    
    return JsonResponse({
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'periodo': {
            'data_inicio': data_inicio or 'todas',
            'data_fim': data_fim or 'todas'
        }
    })