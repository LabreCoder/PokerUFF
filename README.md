<div align="center">
<img alt="logo_finance" src="frontend\vue-project\src\assets\img\logo.svg" width="20%">
<h1>PokerUFF</h1>
</div>

Sistema de Planning Poker desenvolvido como trabalho da disciplina de **Redes de Computadores** do curso de **Sistemas de Informação da Universidade Federal Fluminense (UFF)**.

O PokerUFF permite que equipes participem de sessões de Planning Poker em tempo real, possibilitando a estimativa colaborativa de tarefas através da votação dos participantes. O sistema conta com comunicação em tempo real utilizando WebSockets, permitindo que os votos, entrada e saída de participantes e demais alterações da sessão sejam sincronizados instantaneamente entre todos os usuários conectados.

As sessões possuem um administrador responsável pela criação da sala e pelo gerenciamento da votação, incluindo revelar os votos, reiniciar a rodada e excluir a sessão.

Integrantes do grupo:
- Monique Elen Santos de Souza
- Luiz Miguel Viana Barbosa
- João Victor Labre Machado
- Igor Alexandre de Castro Toledo

---

## 🎯 Tecnologias Utilizadas

### Front-end

* Vue.js
* Vue Router
* JavaScript
* HTML
* CSS

### Back-end

* Python
* FastAPI
* WebSocket
* Uvicorn

---

## Pré-requisitos

- Python 3.11+
- Node.js ^20.19.0 ou >=22.12.0

Verifique as versões instaladas:

```bash
python3 --version
node -v
```

---

# 🚀 Como executar o projeto

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
```

Entrar na pasta do projeto:

```bash
cd PokerUFF
```

---

## 2. Executar o Back-end

Entrar na pasta do back-end:

```bash
cd backend
```

Criar e ativar o ambiente virtual (opcional):

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux/MacOS

```bash
python3 -m venv venv

source venv/bin/activate
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```

Executar o servidor:

```bash
uvicorn main:app --reload
```

---

## 3. Executar o Front-end

Abrir um novo terminal.

Retornar para a pasta raiz do projeto:

```bash
cd PokerUFF
```

Entrar na pasta do front-end:

```bash
cd frontend
```

Entrar na pasta do projeto Vue:

```bash
cd vue-project
```

Instalar as dependências:

```bash
npm install
```

Executar o projeto:

```bash
npm run dev
```

# 💻 Layouts

- Home:
<img src="frontend\vue-project\src\assets\img\layouts\home-view.png" width="100%">

- Ao criar uma sessão:
<img src="frontend\vue-project\src\assets\img\layouts\session-code.png" width="100%">

- Exibição da sessão para o usuário admin (criador da sessão):
<img src="frontend\vue-project\src\assets\img\layouts\session-admin.png" width="100%">

- Ao entrar em uma sessão já existente:
<img src="frontend\vue-project\src\assets\img\layouts\session-username.png" width="100%">

- Visualização da sessão para usuários comuns:
<img src="frontend\vue-project\src\assets\img\layouts\session-view.png" width="100%">


# 📋 Funcionalidades

* Criação de sessões de Planning Poker;
* Entrada em sessões através de código;
* Comunicação em tempo real utilizando WebSockets;
* Votação simultânea entre os participantes;
* Revelação dos votos pelo administrador;
* Reinício da rodada de votação;
* Exclusão da sessão pelo administrador;
* Entrada e saída dinâmica de participantes;
