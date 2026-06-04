# BioFlow — Documentação da API REST

Base URL: `http://localhost:8000/api/`

## Autenticação

Todas as rotas exigem token de autenticação.

```bash
POST /api-token-auth/
Body: { "username": "admin", "password": "admin123" }
Response: { "token": "abc123..." }

# Uso nos headers:
Authorization: Token abc123...
```

---

## Reagentes `/api/reagents/`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/reagents/` | Listar todos os reagentes |
| POST | `/api/reagents/` | Criar novo reagente |
| GET | `/api/reagents/{id}/` | Detalhar reagente |
| PUT | `/api/reagents/{id}/` | Atualizar reagente |
| PATCH | `/api/reagents/{id}/` | Atualizar parcialmente |
| DELETE | `/api/reagents/{id}/` | Excluir reagente |

**Exemplo de payload (POST):**
```json
{
  "name": "Etanol PA",
  "category": "solvent",
  "manufacturer": "Sigma-Aldrich",
  "lot": "SA-2026-01",
  "expiration_date": "2027-12-31",
  "quantity": 500,
  "unit": "mL",
  "supplier": "Sigma-Aldrich",
  "location": "Prateleira A1"
}
```

**Campos extras na resposta:**
- `is_expired` (bool): reagente vencido
- `is_low_stock` (bool): estoque abaixo do limite

---

## Equipamentos `/api/equipments/`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/equipments/` | Listar equipamentos |
| POST | `/api/equipments/` | Cadastrar equipamento |
| GET | `/api/equipments/{id}/` | Detalhar |
| PUT | `/api/equipments/{id}/` | Atualizar |
| DELETE | `/api/equipments/{id}/` | Excluir |

**Status possíveis:** `available`, `in_use`, `maintenance`, `broken`, `inactive`

---

## Experimentos `/api/experiments/`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/experiments/` | Listar |
| POST | `/api/experiments/` | Criar |
| GET | `/api/experiments/{id}/` | Detalhar |
| PUT | `/api/experiments/{id}/` | Atualizar |

**Status possíveis:** `planning`, `in_progress`, `paused`, `completed`, `cancelled`

---

## Agendamentos `/api/schedules/`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/schedules/` | Listar |
| POST | `/api/schedules/` | Criar (com validação de conflito) |
| DELETE | `/api/schedules/{id}/` | Cancelar |

---

## Amostras `/api/samples/`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/samples/` | Listar |
| POST | `/api/samples/` | Cadastrar |
| GET | `/api/samples/{id}/` | Detalhar |

---

## Análises `/api/analysis/`

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/analysis/` | Listar |
| POST | `/api/analysis/` | Registrar |
| GET | `/api/analysis/{id}/` | Detalhar |

---

## Paginação

Todas as listagens retornam no formato:
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/reagents/?page=2",
  "previous": null,
  "results": [...]
}
```

## Busca

Endpoints com busca aceitam `?search=termo`:
```
GET /api/reagents/?search=etanol
GET /api/equipments/?search=hplc
```
