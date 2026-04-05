async function carregarProdutos() {
    try {
        const response = await fetch('/api/produtos/');
        const produtos = await response.json();
        
        const tbody = document.getElementById('tabela-produtos');
        
        if (produtos.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum produto cadastrado.</td></tr>';
            return;
        }
        
        tbody.innerHTML = produtos.map(produto => `
            <tr>
                <th scope="row">${produto.id}</th>
                <td>${produto.nome}</td>
                <td>${produto.categoria || 'Sem categoria'}</td>
                <td>${produto.quantidade_atual}</td>
                <td>R$ ${parseFloat(produto.preco).toFixed(2)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="editarProduto(${produto.id})">Editar</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="excluirProduto(${produto.id})">Excluir</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erro:', error);
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Erro ao carregar produtos.</td></tr>';
    }
}

async function excluirProduto(id) {
    if (!confirm('Tem certeza que deseja excluir este produto?')) return;
    
    try {
        const response = await fetch(`/api/produtos/${id}/`, { method: 'DELETE' });
        
        if (response.ok) {
            alert('Produto excluído com sucesso!');
            carregarProdutos();
        } else {
            alert('Erro ao excluir produto.');
        }
    } catch (error) {
        alert('Erro ao excluir produto.');
    }
}

function editarProduto(id) {
    alert(`Editar produto ${id} - Implementar depois`);
}

document.addEventListener('DOMContentLoaded', carregarProdutos);