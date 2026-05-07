async function carregarFornecedores() {
    try {
        const response = await fetch('/api/fornecedores/');
        const fornecedores = await response.json();
        
        const tbody = document.getElementById('tabela-fornecedores');
        
        if (fornecedores.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">Nenhum fornecedor cadastrado.</tr>';
            return;
        }
        
        tbody.innerHTML = fornecedores.map(f => `
            <tr>
                <td>${f.id}</td>
                <td>${f.nome}</td>
                <td>${f.cnpj || '-'}</td>
                <td>${f.telefone || '-'}</td>
                <td>${f.email || '-'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="editarFornecedor(${f.id})">Editar</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="excluirFornecedor(${f.id})">Excluir</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erro:', error);
    }
}

async function cadastrarFornecedor(evento) {
    evento.preventDefault();
    
    const dados = {
        nome: document.getElementById('nomeFornecedor').value,
        cnpj: document.getElementById('cnpjFornecedor').value,
        telefone: document.getElementById('telefoneFornecedor').value,
        email: document.getElementById('emailFornecedor').value
    };
    
    if (!dados.nome) {
        alert('Preencha o nome do fornecedor.');
        return;
    }
    
    try {
        const response = await fetch('/api/fornecedores/criar/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (response.ok) {
            alert('Fornecedor cadastrado com sucesso!');
            document.getElementById('formFornecedor').reset();
            carregarFornecedores();
        } else {
            alert('Erro ao cadastrar fornecedor.');
        }
    } catch (error) {
        alert('Erro ao conectar com o servidor.');
    }
}

async function excluirFornecedor(id) {
    if (!confirm('Tem certeza?')) return;
    
    try {
        const response = await fetch(`/api/fornecedores/${id}/`, { method: 'DELETE' });
        
        if (response.ok) {
            alert('Fornecedor excluído!');
            carregarFornecedores();
        } else {
            alert('Erro ao excluir.');
        }
    } catch (error) {
        alert('Erro ao excluir.');
    }
}

function editarFornecedor(id) {
    alert(`Editar fornecedor ${id} - Implementar depois`);
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('tabela-fornecedores')) {
        carregarFornecedores();

        const btnSalvar = document.querySelector('#modalFornecedor .btn-primary');
        if (btnSalvar) {
            btnSalvar.addEventListener('click', cadastrarFornecedor);
        }
    }
    
    const form = document.getElementById('formFornecedor');
    if (form) {
        form.addEventListener('submit', cadastrarFornecedor);
    }
});