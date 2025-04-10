# 📦 Desafio Técnico - API Flask com Peewee, JWT e Docker

Este projeto é uma API RESTful desenvolvida em Python utilizando Flask. A aplicação realiza operações com usuários, estoques e equipamentos, com autenticação via JWT, banco de dados PostgreSQL e gerenciamento via Docker.

---

## 📁 Estrutura do Projeto

```
.
├── database/                   # Configuração do banco e criação de tabelas
├── models/                     # Modelos definidos com Peewee
├── routes/                     # Endpoints da API
├── schemas/                    # Esquemas de validação de dados
├── services/                   # Lógica de negócios
├── utils/                      # Funções auxiliares
├── .env.example                # Exemplo de variáveis de ambiente
├── app.py                      # Arquivo principal que inicia o servidor Flask
├── Dockerfile                  # Dockerfile para build da API
├── docker-compose.yml          # Orquestração dos serviços
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação
```

---

## 🚀 Como Rodar Localmente com Docker

### ✅ Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 🔧 Passos para executar:

1. **Clone o repositório:**

```bash
    git clone https://github.com/RaulMS03/desafio-tecnico.git
    cd desafio-tecnico
```

2. **Configure o `.env`:**

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
# Configs do Banco
PG_DB=nome_do_banco
PG_DB_USER=usuario_do_banco
PG_DB_PASSWORD=senha_do_banco
PG_DB_HOST=host
PG_DB_PORT=port

# Flask
DATABASE_URL=postgres://usuario:senha@hostname:port/nome_do_banco

# PGAdmin
PGADMIN_DEFAULT_EMAIL=email@email.com
PGADMIN_DEFAULT_PASSWORD=senha

# JWT
JWT_SECRET_KEY=sua_senha_jwt
```

3. **Suba os containers:**

```bash
  docker-compose up --build
```

A aplicação estará disponível em: [http://localhost:5000](http://localhost:5000)

---

## 🖥️ Acessando o Banco de Dados via pgAdmin

Após subir os containers com `docker-compose up --build`, você pode acessar o pgAdmin através do navegador:

- **URL:** [http://localhost:5050](http://localhost:5050)
- **Login:** valor de `PGADMIN_DEFAULT_EMAIL` no seu `.env`
- **Senha:** valor de `PGADMIN_DEFAULT_PASSWORD` no seu `.env`

Adicione uma nova conexão com os seguintes dados:

- **Host:** `db`
- **Porta:** `5432`
- **Usuário:** valor de `POSTGRES_USER` no seu `.env`
- **Senha:** valor de `POSTGRES_PASSWORD` no seu `.env`

---

## 📄 Acessando a Documentação Swagger

Após subir os containers, você pode acessar a documentação interativa da API gerada pelo Swagger em:

- **URL:** [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

---
## 📄 Como Rodar os Testes

### Requisitos

Antes de rodar os testes, certifique-se de que o container esta rodando.

### Passos para Rodar os Testes

#### 1. 🖥️ Dentro do docker
```bash
  docker-compose exec api pytest
```
#### 2. 🖥️ Localmente(fora do Docker)
basta apenas rodar no terminal na raiz do projeto
```bash
   pytest 
```

---

## 🔐 Autenticação com JWT

1. **Login:**

```http
POST /login
Content-Type: application/json

{
  "email": "usuario@example.com",
  "senha": "sua_senha"
}
```

2. **Requisições autenticadas:**

Adicione o token JWT retornado no header das requisições:

```
Authorization: Bearer <seu_token>
```

---

## 🛠 Tecnologias Utilizadas

- Python 3.10+
- Flask
- Peewee
- PostgreSQL
- Docker e Docker Compose
- JWT (JSON Web Token)
- Pytest

---

## 💡 Funcionalidades

- Cadastro, login e autenticação de usuários.
- Cadastro e gerenciamento de estoques.
- Cadastro de localizações, tipos de equipamentos e categorias.
- Cadastro e gerenciamento de equipamentos.
- Endpoints protegidos por token JWT.
- Banco de dados gerenciado por Peewee.
- Banco e tabelas criados automaticamente no primeiro build.
- Teste automatizado com pytest

---

## 📌 Observações

- O serviço de backend só inicia após o banco estar pronto.
- Código modular e seguindo boas práticas de clean code.

---