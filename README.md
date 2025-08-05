# Workout API

API para gerenciamento de centros de treinamento, alunos e categorias. Densenvolvido para o Bootcamp Back-end Santander DIO.

## Tecnologias Utilizadas

- **Python 3.13**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL** (via `sqlalchemy.url`)
- **Uvicorn** (para servidor ASGI)

## Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/everton-hcosta/workout-API.git
cd workout-API
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o servidor

```bash
sudo docker compose up -d
make run
```

Acesse em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Funcionalidade

* Registro de **Alunos, Categorias e Centros de Treinamento**

## Exemplos de Endpoints

Documentação completa e interativa disponível em `/docs`.

* `GET /atletas`
* `POST /atletas`
* `PATCH /atletas`
* `DELETE /atletas`
* `GET /categorias`
* `POST /categorias`
* `PATCH /categorias`
* `DELETE /categorias`
* `GET /centros_treinamento`
* `POST /centros_treinamento`
* `PATCH /centros_treinamento`
* `DELETE /centros_treinamento`
