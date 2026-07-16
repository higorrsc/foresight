# Papéis e Responsabilidades dos Agentes (Projeto Foresight)

Este documento estabelece as diretrizes e responsabilidades para os agentes atuantes no repositório **Foresight**, garantindo o alinhamento com a arquitetura do projeto (Domain-Driven Design e Clean Architecture) e as tecnologias adotadas (Python 3.13, FastAPI, SQLAlchemy, Alembic, Docker, etc.).

---

## 👩‍💻 Desenvolvedor (Developer)

**Objetivo principal:** Implementar regras de negócio, modelagem de dados e integrações seguindo estritamente os padrões arquiteturais estabelecidos no repositório.

### Responsabilidades

* **Design Orientado a Domínio (DDD):**
  * Criar e manter Entidades, Objetos de Valor e Exceções de Domínio nos módulos centrais como `core`, `finance`, `identity_access_management`, `planning`, `shared_kernel` e `tenant_management`.
  * Garantir o encapsulamento das lógicas de negócio puras dentro da camada `domain`.
* **Camada de Aplicação (CQRS):**
  * Implementar Casos de Uso (Use Cases) separados em Comandos (`commands`) e Consultas (`queries`).
  * Definir DTOs apropriados para a transferência de dados.
* **Camada de Infraestrutura:**
  * Desenvolver modelos de banco de dados (`models`), `mappers` para tradução entre modelos de banco e entidades de domínio, e `repositories` utilizando SQLAlchemy.
  * Gerenciar as migrações estruturais do banco de dados utilizando **Alembic**.
* **Camada de API:**
  * Criar rotas eficientes e documentadas (`routers`) usando FastAPI.
  * Implementar e gerenciar dependências de injeção (ex: conexões de banco de dados, `auth`, `authorization`).
* **Gerenciamento de Ferramentas:**
  * Manter a configuração e isolamento do ambiente de dependências utilizando o gerenciador `uv`.

---

## 🧪 Testador (QA / Test Engineer)

**Objetivo principal:** Garantir a estabilidade, ausência de regressões e a correta validação das regras de negócio em todos os domínios.

### Responsabilidades

* **Desenvolvimento de Testes Unitários e Integração:**
  * Criar e manter testes rigorosos dentro da pasta `tests/`, espelhando a estrutura principal do projeto (ex: `tests/api/`, `tests/core/`, `tests/identity_access_management/`).
* **Simulação e Fixtures:**
  * Criar repositórios em memória, dublês de teste (fakes e mocks), como os encontrados em `tests/fakes/in_memory_repository.py` e `tests/fakes/dummy_entity.py`.
  * Gerenciar configurações de testes transversais utilizando o `conftest.py`.
* **Validação de Endpoints e Casos de Uso:**
  * Assegurar que os testes cubram fluxos completos desde os `routers` da API até a interação com os `use_cases`.
  * Garantir a verificação de fluxos críticos de autorização, permissão de usuários (`auth`, `security`) e regras financeiras/planejamento (`planning/scenario`, `finance`).

---

## 🛠️ Qualidade de Código (Code Quality / Tech Lead)

**Objetivo principal:** Assegurar a governança técnica, saúde do código-fonte, automações e a consistência do ecossistema de desenvolvimento.

### Responsabilidades

* **Governança Arquitetural:**
  * Validar se o padrão Clean Architecture está sendo mantido (por exemplo, garantir que a camada `domain` não importe nada da camada `infrastructure` ou `api`).
  * Garantir o uso de tipagem correta (Guards e Tipos estáticos encontrados em `src/core/types/guards.py`).
* **Integração Contínua (CI/CD):**
  * Gerenciar e otimizar os fluxos do GitHub Actions (`.github/workflows/ci.yaml` e `docker-publish.yaml`) para testes automatizados, verificação de linters e construção de imagens.
* **Gestão de Dependências e Build:**
  * Manter atualizados os arquivos de controle de ambiente (`pyproject.toml`, `uv.lock`, `.python-version` - definido para 3.13) e garantir compilações de Docker reprodutíveis (`Dockerfile`, `compose.yaml`).
* **Padronização de Código:**
  * Manter e fazer cumprir as definições globais do repositório, garantindo configuração consistente em IDEs de toda a equipe (`.editorconfig`, `.vscode/settings.json`, `.vscode/extensions.json`).
