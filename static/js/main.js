// filepath: /home/guidev/repos/django-blog/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Função para exibir uma mensagem de sucesso
    function showSuccessMessage(message) {
        const successMessage = document.createElement('div');
        successMessage.className = 'bg-green-500 text-white p-4 rounded';
        successMessage.innerText = message;
        document.body.appendChild(successMessage);
        
        setTimeout(() => {
            successMessage.remove();
        }, 3000);
    }

    // Exemplo de uso da função
    const successButton = document.getElementById('success-button');
    if (successButton) {
        successButton.addEventListener('click', function() {
            showSuccessMessage('Operação realizada com sucesso!');
        });
    }

    // Função para confirmar a exclusão de um artigo
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const confirmed = confirm('Você tem certeza que deseja excluir este artigo?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});