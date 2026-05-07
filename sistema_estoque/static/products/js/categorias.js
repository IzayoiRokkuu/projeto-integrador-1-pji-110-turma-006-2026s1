async function carregarCategorias() {
    try {
        const response = await fetch('/api/categorias/');
        const categorias = await response.json();
        
        const tbody = document.getElementById('tabela-categorias');
        
        if (categorias.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">Nenhuma categoria cadastrada.穷<table>';
            return;
        }
        
        tbody.innerHTML = categorias.map(cat => `
            <tr>
                <td>${cat.id}</td>
                <td>${cat.nome}</td>
                <td>${cat.descricao || '-'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="excluirCategoria(${cat.id})">Excluir</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('tabela-categorias').innerHTML = '<tr><td colspan="4" class="text-center text-danger">Erro ao carregar.</tr>';
    }
}

async function cadastrarCategoria() {
    const nome = document.getElementById('nomeNovaCategoria').value;  // ← corrigido
    const descricao = document.getElementById('descricaoCategoria').value;
    
    if (!nome) {
        alert('Preencha o nome da categoria.');
        return;
    }
    
    try {
        const response = await fetch('/api/categorias/criar/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, descricao })
        });
        
        if (response.ok) {
            alert('Categoria cadastrada com sucesso!');
            document.getElementById('nomeNovaCategoria').value = '';
            document.getElementById('descricaoCategoria').value = '';
            
            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalCategoria'));
            modal.hide();
            
            carregarCategorias();
        } else {
            alert('Erro ao cadastrar categoria.');
        }
    } catch (error) {
        alert('Erro ao conectar com o servidor.');
    }
}

async function excluirCategoria(id) {
    if (!confirm('Tem certeza que deseja excluir esta categoria?')) return;
    
    try {
        const response = await fetch(`/api/categorias/${id}/`, { method: 'DELETE' });
        
        if (response.ok) {
            alert('Categoria excluída com sucesso!');
            carregarCategorias();
        } else {
            alert('Erro ao excluir categoria.');
        }
    } catch (error) {
        alert('Erro ao excluir categoria.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    carregarCategorias();
    
    // Associar o botão do modal ao cadastro
    const btnSalvar = document.querySelector('#modalCategoria .btn-primary');
    if (btnSalvar) {
        btnSalvar.removeEventListener('click', cadastrarCategoria);
        btnSalvar.addEventListener('click', cadastrarCategoria);
    }
});