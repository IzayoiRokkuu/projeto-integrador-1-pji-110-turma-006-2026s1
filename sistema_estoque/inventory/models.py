from django.db import models
from django.contrib.auth.models import User
from products.models import Produto

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Saida', 'Saída'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.produto.nome} - {self.quantidade}"
