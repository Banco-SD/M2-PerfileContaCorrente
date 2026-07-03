# Wallet Service

Um serviço de carteira digital implementado com Python, FastAPI, SQLAlchemy e PostgreSQL.

## Estrutura do projeto

- `app/` - código fonte da API
- `arquivo/` - casos de teste e guia de execução
- `requirements.txt` - dependências do Python
- `.env.example` - exemplo de configuração de ambiente

## Instalação

1. Criar e ativar ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

## Configuração do ambiente

1. Copie `.env.example` para `.env`:

```bash
cp .env.example .env
```

2. Atualize `DATABASE_URL` com a conexão do PostgreSQL existente.

## Executando a API

Execute o serviço com:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentação Swagger

Acesse a documentação automaticamente gerada em:

```text
http://127.0.0.1:8000/docs
```

## Endpoints principais

- `GET /health` - verifica status do serviço
- `GET /wallet/{user_id}` - consulta saldo da carteira
- `GET /wallet/{user_id}/statement` - obtém o extrato da carteira
- `POST /wallet/debit` - debita a carteira
- `POST /wallet/credit` - credita a carteira

## Notas importantes

- A aplicação não recria as tabelas existentes.
- Toda operação de crédito/débito é realizada em transação com `SELECT ... FOR UPDATE`.
- Mensagens de erro seguem códigos HTTP apropriados (400, 404, 409, 500).
