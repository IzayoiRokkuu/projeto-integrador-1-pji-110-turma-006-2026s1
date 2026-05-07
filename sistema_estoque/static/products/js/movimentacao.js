let podeRegistrar = true;

async function carregarProdutos() {
    try {
        const response = await fetch('/api/produtos/');
        const produtos = await response.json();
        
        const select = document.getElementById('produtoSelecionado');
        if (!select) return;
        
        select.innerHTML = '<option value="">Selecione o produto...</option>';
        
        produtos.forEach(produto => {
            const option = document.createElement('option');
            option.value = produto.id;
            option.textContent = `${produto.nome} (Estoque: ${produto.quantidade_atual})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
    }
}

async function registrarMovimentacao() {
    if (!podeRegistrar) {
        console.log('Bloqueado: aguarde a operação anterior terminar');
        return;
    }
    
    console.log('registrarMovimentacao chamada', new Date().getTime());
    podeRegistrar = false;
    console.log('Registrando...');
    
    const tipo = document.getElementById('tipoMovimentacao').value;
    const produtoId = document.getElementById('produtoSelecionado').value;
    const quantidade = parseInt(document.getElementById('quantidadeMovimentacao').value);
    
    if (!produtoId || !quantidade || quantidade <= 0) {
        alert('Preencha todos os campos corretamente.');
        podeRegistrar = true;
        return;
    }
    
    const endpoint = tipo === 'entrada' ? '/api/movimentacoes/entrada/' : '/api/movimentacoes/saida/';
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                produto_id: parseInt(produtoId),
                quantidade: quantidade,
                observacao: ''
            })
        });
        
        const resultado = await response.json();
        
        if (response.ok) {
            alert(`${tipo === 'entrada' ? 'Entrada' : 'Saída'} registrada!`);
            document.getElementById('quantidadeMovimentacao').value = '';
            carregarProdutos();
            carregarMovimentacoes();
        } else {
            alert(resultado.error || 'Erro ao registrar.');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar.');
    }
    
    // Libera após 1 segundo
    setTimeout(() => { podeRegistrar = true; }, 1000);
}

async function carregarMovimentacoes() {
    const tbody = document.getElementById('tabela-movimentacoes');
    if (!tbody) return;
    
    try {
        const response = await fetch('/api/movimentacoes/');
        const movimentacoes = await response.json();
        
        if (movimentacoes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhuma movimentação.穷</tr>';
            return;
        }
        
        tbody.innerHTML = movimentacoes.map(m => `
            <tr>
                <td>${m.produto}</td>
                <td><span class="badge ${m.tipo === 'Entrada' ? 'bg-success' : 'bg-danger'}">${m.tipo}</span></td>
                <td>${m.quantidade}</td>
                <td>${m.usuario}</td>
                <td>${m.data}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erro:', error);
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    carregarProdutos();
    carregarMovimentacoes();
    
    const btn = document.getElementById('btnConfirmar');
    if (btn) {
        btn.addEventListener('click', registrarMovimentacao);
    }
});