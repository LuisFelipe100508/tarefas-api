# Tarefas API

API REST de gerenciamento de tarefas com autenticação JWT, onde cada usuário acessa apenas as próprias tarefas.

**Demo ao vivo:** https://tarefas-api-8yoz.onrender.com/api/docs/

> O plano gratuito do Render hiberna após inatividade. A primeira requisição pode levar cerca de 1 minuto.

## Tecnologias

Python, Django, Django REST Framework, SimpleJWT, drf-spectacular (Swagger), PostgreSQL (Neon), pytest, WhiteNoise e Gunicorn. Deploy no Render.

## Funcionalidades

- Registro de usuários e login com JWT (access e refresh)
- CRUD de tarefas (título, descrição, status, prazo)
- Cada usuário vê e altera somente as próprias tarefas
- Paginação, limite de requisições (throttling) e documentação Swagger
- Testes automatizados de autenticação e permissões

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth/register/` | Cria usuário |
| POST | `/api/auth/token/` | Login (retorna tokens) |
| POST | `/api/auth/token/refresh/` | Renova o access token |
| GET, POST | `/api/tasks/` | Lista e cria tarefas |
| GET, PATCH, PUT, DELETE | `/api/tasks/{id}/` | Detalhe, edição e remoção |

Documentação interativa em `/api/docs/`.

## Como rodar localmente

```bash
git clone https://github.com/SEU-USUARIO/tarefas-api.git
cd tarefas-api
python -m venv .venv
.venv\Scripts\activate        # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # Windows: copy .env.example .env
```

Edite o `.env` com uma `SECRET_KEY` própria (veja abaixo) e rode:

```bash
python manage.py migrate
python manage.py runserver
```

Gerar uma `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Testes

```bash
python -m pytest
```

## Decisões técnicas

**Segurança**
- **`SECRET_KEY` sem valor padrão e `DEBUG` padrão `False`:** se a configuração faltar em produção, a aplicação falha de forma segura em vez de expor erros ou rodar com chave fraca.
- **Segredos em variáveis de ambiente:** o `.env` fica fora do Git. O `.env.example` documenta as variáveis sem valores reais.
- **Isolamento por usuário em duas camadas:** o `get_queryset` filtra por dono e a permissão `IsOwner` confere o objeto. Acessar a tarefa de outro usuário retorna **404** e não 403, para não revelar que o recurso existe.
- **Campo `owner` fora do serializer:** o servidor define o dono, o que evita *mass assignment*.
- **`IsAuthenticated` como permissão global:** toda rota exige login, e só o registro e o login são públicos.
- **Throttling por escopo:** registro (5/hora) e login (10/min) têm limites mais duros contra criação em massa de contas e força bruta.
- **Access token curto (15 min):** limita o dano se vazar. O refresh token renova a sessão.
- **`validate_password` no registro:** reaproveita os validadores do Django contra senhas fracas.
- **HTTPS forçado em produção:** redirecionamento SSL, cookies seguros e HSTS quando `DEBUG=False`.

**Arquitetura e infraestrutura**
- **Banco externo (Neon):** separa os dados do ciclo de vida do serviço web.
- **`ALLOWED_HOSTS` dinâmico:** usa o domínio fornecido pela plataforma em vez de aceitar qualquer host.
- **Chave de produção diferente da local:** vazar o ambiente de desenvolvimento não compromete a produção.
- **WhiteNoise:** serve arquivos estáticos sem servidor adicional.

**Testes**
- **Foco em autenticação e permissões:** é onde um erro causa vazamento de dados. Há testes para o 404 entre usuários, tentativa de definir `owner` e edição de tarefa alheia.
- **Cache limpo a cada teste:** o throttling guarda contadores no cache.

## Limitações conhecidas

- O throttling usa cache em memória (por processo). Em produção real, o ideal seria Redis.
- O plano gratuito hiberna por inatividade.

## Melhorias futuras

Filtros e busca, categorias de tarefas, CI com GitHub Actions e logs estruturados.