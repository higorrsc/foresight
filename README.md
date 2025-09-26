# ForeSight

**ForeSight** é uma plataforma para **simulação orçamentária e projeção de custos/gastos**, com foco em previsões, cenários financeiros e tomadas de decisão.  
O nome reflete o objetivo do projeto: *Anticipate. Plan. Achieve.*

---

## 🎯 Objetivos

- Migrar o sistema legado em **Excel + VBA + SQL Server** para uma aplicação moderna.  
- Utilizar **Clean Architecture** e **DDD** para manter separação clara entre camadas.  
- Garantir facilidade de manutenção, testes e evolução futura.  
- Criar base sólida para projeções financeiras e análises de cenários.

---

## 📐 Arquitetura

O projeto segue princípios de **Domain-Driven Design (DDD)** e **Clean Architecture**:

```
src/
├── core/
│   ├── domain/           # Regras de negócio (entidades, value objects, interfaces)
│   │   ├── _shared/      # Abstrações genéricas (Entity, Repository, ValueObject)
│   │   └── entities/     # Entidades específicas
│   │
│   ├── application/      # Casos de uso (Use Cases), DTOs
│   │   ├── _shared/      # Use cases genéricos (List, Delete) e exceções comuns
│   │   └── use_cases/    # Casos de uso específicos por entidade
│   │
│   └── infrastructure/   # Repositórios, serviços externos, implementações técnicas
│       └── repositories/ # Ex.: InMemoryRepository
│
└── tests/                # Testes unitários/integrados
```

### Camadas

| Camada | Responsabilidade |
|--------|------------------|
| **Domain** | Lógica de negócio pura: entidades, value objects, interfaces de repositório. |
| **Application** | Casos de uso, DTOs e regras de aplicação. |
| **Infrastructure** | Implementações técnicas: persistência, serviços externos, repositórios concretos. |
| **Tests** | Testes unitários e de integração, usando fakes/mocks. |

---

## 🛠️ Como rodar

### Pré-requisitos

- **Python 3.13+** (gerenciado via [asdf](https://asdf-vm.com/) ou pyenv)  
- **uv** para gerenciamento de dependências  
- `pytest` para rodar testes  

### Passos

```bash
# Clone o repositório
git clone https://github.com/higorrsc/foresight.git
cd foresight

# Instale dependências
uv sync

# Rode os testes
uv run pytest
```

---

## 📦 Exemplos de Uso

### GenericDeleteUseCase

```python
from uuid import uuid4
from core.application._shared.use_cases.generic_delete import GenericDeleteUseCase, InputDeleteRequestDTO
from core.domain._shared.exceptions import EntityNotFoundException
from core.infrastructure.repositories.in_memory_repository import InMemoryRepository
from core.domain.entities.user import User

repo = InMemoryRepository[User]()
user = User(name="Alice")
repo.save(user)

delete_uc = GenericDeleteUseCase[User](
    repository=repo,
    not_found_exception=EntityNotFoundException,
    not_found_message="User with id={id} not found"
)

delete_uc.execute(InputDeleteRequestDTO(id=user.id))
```

### GenericListUseCase

```python
from core.application._shared.use_cases.generic_list import GenericListUseCase

list_uc = GenericListUseCase[User](repository=repo)
response = list_uc.execute()
print(response.data)  # lista de usuários
```

---

## ✅ Boas Práticas

- Entidades imutáveis e validadas (`AbstractEntity`, `AbstractValueObject`).  
- Repositórios abstratos no **domínio** + implementações na **infraestrutura**.  
- **Use Cases genéricos** para operações comuns.  
- DTOs para entrada/saída dos casos de uso.  
- Testes com **InMemoryRepository** (sem depender de banco real).  

---

## 🚀 Próximos Passos

- Criar **casos de uso específicos** por entidade (Create, Update).  
- Implementar repositórios concretos (ex.: SQLAlchemy).  
- Adicionar camada de API (FastAPI ou Flask).  
- Configurar **CI/CD com GitHub Actions**.  
- Dockerizar aplicação para execução em produção.  

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

🔗 Repositório: [higorrsc/foresight](https://github.com/higorrsc/foresight)
