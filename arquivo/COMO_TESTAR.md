# COMO TESTAR

Este guia passo a passo explica como configurar e validar o Wallet Service.

## 1. Criar ambiente virtual

```bash
cd /home/jlucas/Área de trabalho/Faculdade/Sistemas Distribuídos/módulo 2-wallet
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## 3. Configurar o `.env`

1. Copie o arquivo exemplo:

```bash
cp .env.example .env
```

2. Abra `.env` e atualize a variável:

```text
DATABASE_URL=postgresql://usuario:senha@host/database
```

3. Salve o arquivo.

## 4. Iniciar a API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação será disponibilizada em `http://127.0.0.1:8000`.

## 5. Acessar o Swagger

Abra o navegador em:

```text
http://127.0.0.1:8000/docs
```

## 6. Inserir registros de teste no banco

Use seu cliente PostgreSQL favorito (`psql`, `pgcli`, DBeaver, etc.).

Exemplo:

```sql
INSERT INTO users (id, nome, cpf, email, created_at)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'Teste Usuario', '12345678901', 'teste@example.com', NOW());

INSERT INTO wallet (id, user_id, saldo, status, updated_at)
VALUES
  ('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', 1500.75, 'ATIVA', NOW());
```

Se a tabela já tiver dados, apenas use `user_id` existente.

## 7. Ordem recomendada de testes

1. `GET /health`
2. `GET /wallet/{user_id}`
3. `GET /wallet/{user_id}/statement`
4. `POST /wallet/credit`
5. `POST /wallet/debit`
6. `GET /wallet/{user_id}` novamente
7. `GET /wallet/{user_id}/statement` novamente

## 8. Testar cada endpoint

### `GET /health`

```bash
curl http://127.0.0.1:8000/health
```

### `GET /wallet/{user_id}`

```bash
curl http://127.0.0.1:8000/wallet/11111111-1111-1111-1111-111111111111
```

### `GET /wallet/{user_id}/statement`

```bash
curl http://127.0.0.1:8000/wallet/11111111-1111-1111-1111-111111111111/statement
```

### `POST /wallet/credit`

```bash
curl -X POST http://127.0.0.1:8000/wallet/credit \
  -H "Content-Type: application/json" \
  -d '{"user_id": "11111111-1111-1111-1111-111111111111", "valor": 250.00, "descricao": "Depósito", "referencia": "55555555-5555-5555-5555-555555555555"}'
```

### `POST /wallet/debit`

```bash
curl -X POST http://127.0.0.1:8000/wallet/debit \
  -H "Content-Type: application/json" \
  -d '{"user_id": "11111111-1111-1111-1111-111111111111", "valor": 120.50, "descricao": "Pagamento PIX", "referencia": "66666666-6666-6666-6666-666666666666"}'
```

## 9. Validar alteração de saldo

Após crédito ou débito, execute:

```bash
curl http://127.0.0.1:8000/wallet/11111111-1111-1111-1111-111111111111
```

Verifique que o valor de `saldo` foi atualizado corretamente.

## 10. Validar extrato

Após operações, execute o extrato:

```bash
curl http://127.0.0.1:8000/wallet/11111111-1111-1111-1111-111111111111/statement
```

Os lançamentos devem aparecer do mais recente para o mais antigo.

## 11. Testar row-level locking

Para verificar bloqueio de linha, dispare dois débitos simultâneos usando duas sessões separadas:

```bash
curl -X POST http://127.0.0.1:8000/wallet/debit -H "Content-Type: application/json" -d '{"user_id": "11111111-1111-1111-1111-111111111111", "valor": 100.00, "descricao": "Débito 1", "referencia": "88888888-8888-8888-8888-888888888888"}' &
curl -X POST http://127.0.0.1:8000/wallet/debit -H "Content-Type: application/json" -d '{"user_id": "11111111-1111-1111-1111-111111111111", "valor": 200.00, "descricao": "Débito 2", "referencia": "99999999-9999-9999-9999-999999999999"}' &
wait
```

Se o bloqueio estiver funcionando, uma requisição aguarda a outra e o saldo não fica negativo.

## 12. Confirmar consistência de saldo

Depois dos débitos simultâneos, consulte o saldo novamente e verifique se o valor é consistente.

## 13. Usar exemplos de `arquivo/testes.json`

O arquivo `arquivo/testes.json` contém exemplos para cada endpoint, incluindo casos de sucesso e erro.

1. Abra o arquivo.
2. Replique os objetos `method`, `endpoint`, `body` e os `expected_response` nos seus testes.
3. Valide que o retorno da API corresponde ao esperado.


## 14. Observações finais

- Todas as respostas são JSON.
- O serviço registra início, sucesso, rollback e erros no `logger`.
- Não há alteração de estrutura de tabelas: o serviço apenas consome as tabelas existentes.
