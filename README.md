# ForeSight

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/higorrsc/foresight/actions/workflows/ci.yaml/badge.svg)](https://github.com/higorrsc/foresight/actions/workflows/ci.yaml)

**ForeSight** é uma plataforma moderna para simulação orçamentária e projeção de custos, construída com uma arquitetura limpa e robusta em Python. O nome reflete o objetivo do projeto: *Anticipate. Plan. Achieve.*

---

## 🎯 Objetivos

- Migrar o sistema legado em **Excel + VBA + SQL Server** para uma aplicação de API moderna e escalável.
- Utilizar **Clean Architecture** e **Domain-Driven Design (DDD)** para garantir uma separação clara entre as camadas de negócio, aplicação e infraestrutura.
- Implementar um sistema de **autenticação (JWT)** e **autorização baseada em papéis (RBAC)**.
- Garantir a manutenibilidade, testabilidade e evolução futura do projeto através de uma base de código bem estruturada.

---

## 📐 Arquitetura

O projeto segue rigorosamente os princípios de **Clean Architecture** e **DDD**. A dependência é sempre direcionada para o interior, protegendo a lógica de negócio de detalhes de implementação.

```text
.
├── src/
│   ├── api/                      # Camada de Apresentação (FastAPI Endpoints)
│   │
│   ├── core/                     # Núcleo da aplicação (Base classes, Configs, Custom Types)
│   │   ├── application/
│   │   ├── domain/
│   │   └── infrastructure/
│   │
│   ├── finance/                  # Contexto: Finanças (Catálogo de Moedas)
│   │   └── domain/               # Entidades e Value Objects de Moedas
│   │
│   ├── identity_access_management/ # Contexto: Gestão de Identidade e Acesso
│   │   ├── application/          # Casos de Uso, DTOs
│   │   ├── domain/               # Entidades, Value Objects, Regras de Negócio
│   │   └── infrastructure/       # Repositórios, Mappers, Modelos SQLAlchemy
│   │
│   ├── planning/                 # Contexto: Planejamento (Cenários e Taxas de Câmbio)
│   │   ├── application/          # Casos de Uso, DTOs, Handlers
│   │   ├── domain/               # Entidades de Cenários e Taxas de Câmbio
│   │   └── infrastructure/       # Repositórios de Cenários, Modelos SQLAlchemy
│   │
│   ├── tenant_management/        # Contexto: Gestão de Tenants e Planos
│   │   ├── application/
│   │   ├── domain/
│   │   └── infrastructure/
│   │
│   ├── shared_kernel/            # Lógica compartilhada entre contextos (Áreas, Unidades Organizacionais)
│   │   ├── application/
│   │   ├── domain/
│   │   └── infrastructure/
│   │
│   └── scripts/                  # Scripts utilitários (ex: Seeding de banco de dados)
│       └── seed.py
│
└── tests/                    # Testes (Unidade, Integração, API e Scripts), separados do código-fonte.
```

| Camada | Responsabilidade | Tecnologias |
| :--- | :--- | :--- |
| **Domain** | Lógica de negócio pura: entidades, validações e regras. | Python 3.13+ |
| **Application** | Orquestração dos casos de uso, DTOs e abstrações (ex: `AbstractAuthenticationProvider`). | Dataclasses |
| **Infrastructure** | Implementações concretas: persistência, serviços externos, configurações. | SQLAlchemy, Alembic, Pydantic-Settings |
| **API (Presentation)** | Exposição dos casos de uso via endpoints RESTful, gestão de segurança. | FastAPI, JWT |
| **Tests** | Testes de unidade, integração e end-to-end para garantir a qualidade. | Pytest, TestClient |

---

## ✨ Funcionalidades Principais

- **API RESTful Completa**: Endpoints para gestão de `Users`, `Roles`, `Permissions`, `Tenants`, `Plans`, `Areas`, `Organizational Units` e `Scenarios` (com suporte a taxas de câmbio multimoeda).
- **Autenticação JWT**: Sistema de login seguro baseado em tokens.
- **Autorização Baseada em Papéis (RBAC)**: Endpoints protegidos que requerem papéis específicos (ex: `admin`).
- **Sistema de Migrações**: Evolução segura do esquema da base de dados com **Alembic**.
- **Repositório Genérico (Repository Pattern)**: Implementação de um repositório SQLAlchemy genérico que abstrai as operações de CRUD, simplificando a adição de novas entidades e garantindo a consistência da camada de dados.
- **Configuração por Ambiente**: Gestão de configurações flexível (`.env`) para diferentes ambientes (desenvolvimento, produção).
- **Injeção de Dependência**: Uso extensivo do `Depends` do FastAPI para gerir dependências e sessões de base de dados.
- **Testes Abrangentes**: Cobertura de testes para todas as camadas da aplicação.
- **Seeding Automático**: Inicialização automática da base de dados com dados essenciais durante o arranque da aplicação.

---

## 🚀 Como Executar o Projeto

Existem duas maneiras recomendadas para executar o projeto: via **Docker (recomendado)** ou **Localmente**.

### Com Docker (Recomendado)

Este método abstrai a necessidade de instalar Python ou gerir dependências manualmente.

**Pré-requisitos:**

- **Docker**
- **Docker Compose**

**Passos:**

1. Crie o ficheiro `.env` conforme descrito na secção de configuração local abaixo.
2. Suba os contentores da aplicação:

    ```bash
    docker-compose up -d --build
    ```

3. A API estará disponível em `http://127.0.0.1:8000/docs`.

### Localmente (Manual)

### Pré-requisitos

- **Python 3.13+**
- **uv** para gestão de dependências e ambiente virtual

### Passos para a Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/higorrsc/foresight.git
    cd foresight
    ```

2. **Instale as dependências:**

    ```bash
    uv sync
    ```

3. **Configure as Variáveis de Ambiente:**
    Crie um ficheiro `.env` na raiz do projeto, copiando a partir do exemplo (se existir) ou criando um novo. Para o ambiente de desenvolvimento padrão com SQLite, ele deve conter:

    ```env
    # .env
    DB_DRIVER="sqlite"
    DB_DATABASE="./foresight.db"

    SECRET_KEY="uma-chave-secreta-forte-e-unica"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    AUTH_PROVIDER="local"
    ```

4. **Aplique as Migrações da Base de Dados:**
    Este comando irá criar o ficheiro da base de dados (se não existir) e aplicar todas as migrações para criar as tabelas `areas`, `users`, `roles`, etc.

    ```bash
    uv run alembic upgrade head
    ```

5. **Execute a API:**

    ```bash
    uv run uvicorn src.api.main:app --reload
    ```

    A API estará disponível em `http://127.0.0.1:8000`, e a documentação interativa em `http://127.0.0.1:8000/docs`.

### Como Executar os Testes

Para executar toda a suíte de testes (unidade, integração e API), use o Pytest:

```bash
uv run pytest
```

---

## 🔄 CI/CD

O projeto utiliza **GitHub Actions** para automação de integração contínua. O workflow é acionado a cada `push` ou `pull request` e executa as seguintes etapas:

- **Linting**: Verifica a qualidade e o estilo do código.
- **Testing**: Executa a suíte de testes para garantir a integridade da aplicação.

---

## Próximos Passos

- **Modelar as Entidades de Negócio**: Implementar as entidades centrais do projeto (`CentroDeCusto`, `Orcamento`, `Projecao`).
- **Refinar a UI do Swagger**: Investigar e corrigir a renderização do formulário de autenticação no Swagger UI.
- **Adicionar Logging e Monitoramento**: Integrar ferramentas para observabilidade da aplicação em produção.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
