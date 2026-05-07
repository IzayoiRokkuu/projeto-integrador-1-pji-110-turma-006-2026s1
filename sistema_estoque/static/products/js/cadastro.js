// Carregar categorias do backend
async function carregarCategorias() {
    try {
        const response = await fetch('/api/categorias/');
        const categorias = await response.json();
        
        const select = document.getElementById('categoriaProduto');
        
        // Limpar opções existentes (manter a primeira opção vazia)
        select.innerHTML = '<option value="">Selecione uma categoria...</option>';
        
        // Adicionar categorias do banco
        categorias.forEach(categoria => {
            const option = document.createElement('option');
            option.value = categoria.id;
            option.textContent = categoria.nome;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao carregar categorias:', error);
    }
}

async function cadastrarProduto(evento) {
    evento.preventDefault();  // Impede o formulário de recarregar a página
    
    // Pegar os valores do formulário
    const nome = document.getElementById('nomeProduto').value;
    const categoria = document.getElementById('categoriaProduto').value;
    const quantidade = parseInt(document.getElementById('quantidadeProduto').value);
    const preco = parseFloat(document.getElementById('precoProduto').value);
    
    // Validar campos obrigatórios
    if (!nome) {
        alert('Por favor, preencha o nome do produto.');
        return;
    }
    
    if (!categoria) {
        alert('Por favor, selecione uma categoria.');
        return;
    }
    
    if (isNaN(quantidade) || quantidade < 0) {
        alert('Por favor, insira uma quantidade válida.');
        return;
    }
    
    if (isNaN(preco) || preco <= 0) {
        alert('Por favor, insira um preço válido.');
        return;
    }
    
    // Montar objeto com os dados no formato que a API espera
    const dados = {
        nome: nome,
        codigo: nome.replace(/\s/g, '').substring(0, 10) + Date.now(), // Código único simples
        preco: preco,
        quantidade_atual: quantidade,
        estoque_minimo: 0  // Valor padrão
    };
    
    try {
        // Enviar para a API
        const resposta = await fetch('/api/produtos/criar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });
        
        const resultado = await resposta.json();
        
        if (resposta.ok) {
            alert(`✅ Produto "${nome}" cadastrado com sucesso!`);
            // Limpar o formulário
            document.getElementById('nomeProduto').value = '';
            document.getElementById('categoriaProduto').value = '';
            document.getElementById('quantidadeProduto').value = '';
            document.getElementById('precoProduto').value = '';
        } else {
            alert('Erro ao cadastrar produto: ' + (resultado.error || 'Verifique os dados'));
        }
    } catch (erro) {
        console.error('Erro:', erro);
        alert('Erro ao conectar com o servidor. Verifique se o servidor está rodando.');
    }
}

// Quando a página carregar, associar o evento ao formulário
document.addEventListener('DOMContentLoaded', function() {
    carregarCategorias();

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', cadastrarProduto);
    }
});