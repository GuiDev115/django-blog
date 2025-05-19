# Django Blog

Um blog simples desenvolvido em Django como parte da disciplina **GAC 116 - Desenvolvimento Web** na **Universidade Federal de Lavras (UFLA)**.

## Propósito

Este projeto tem como objetivo demonstrar os conceitos fundamentais de desenvolvimento web utilizando o framework Django. Ele inclui funcionalidades como:

- Gerenciamento de usuários com diferentes níveis de permissão (leitor, redator e administrador).
- Criação, edição e exclusão de artigos.
- Sistema de categorias para organização de artigos.
- Comentários e curtidas em artigos.
- Requisição para se tornar redator.
- Interface administrativa para gerenciar o conteúdo.

## Funcionalidades

- **Usuários**: Cadastro e autenticação de usuários com permissões específicas.
- **Artigos**: Criação e gerenciamento de artigos por redatores e administradores.
- **Comentários**: Adição de comentários em artigos.
- **Curtidas**: Sistema de curtidas para artigos.
- **Administração**: Interface administrativa para gerenciar usuários, artigos, categorias e permissões.

---

## Requisitos

Antes de executar o projeto, certifique-se de ter os seguintes requisitos instalados:

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)
- Banco de dados SQLite (já configurado por padrão no Django)

---

## Como executar o projeto

Siga os passos abaixo para configurar e executar o projeto localmente:

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/django-blog.git
cd django-blog
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Configure o banco de dados

Crie as migrações e aplique-as para configurar o banco de dados:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário
Crie um superusuário para acessar o ambiente administrativo:

```bash
python3 manage.py createsuperuser
```

### 6. Execute o servidor de desenvolvimento

Inicie o servidor local:

```bash
python manage.py runserver
```