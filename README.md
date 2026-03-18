# ShieldPay 🛡️💸

**ShieldPay** é um motor de pagamentos (Billing Engine) robusto, focado em integridade de dados e segurança transacional. O sistema gerencia o cadastro de clientes, contas digitais (wallets) e transferências entre usuários com validação rigorosa e persistência atômica.

---

## 🏗️ Arquitetura e Padrões de Projeto

O projeto foi construído seguindo os princípios da **Clean Architecture** e **DDD (Domain-Driven Design)** para garantir o desacoplamento total da lógica de negócio:

* **Entities & Value Objects**: Modelagem de domínio rica (ex: `Cpf`, `Email`, `Money`) com auto-validação.
* **Use Cases**: Camada de aplicação que orquestra as regras de negócio de forma isolada.
* **Repository Pattern**: Abstração da camada de dados permitindo fácil troca de persistência.
* **Unit of Work (UoW)**: Garantia de transações **ACID**. Se uma transferência falha ao atualizar o recebedor, o saldo do pagador é revertido automaticamente.
* **Pessimistic Locking**: Implementação de `with_for_update` no SQLAlchemy para evitar condições de corrida (race conditions) em transferências simultâneas.

---

## 🚀 Tecnologias

* **Python 3.10+**
* **FastAPI**: Interface profissional de API com Swagger automático.
* **SQLAlchemy 2.0**: Mapeamento objeto-relacional moderno.
* **SQLite**: Persistência relacional simples e eficaz.
* **Poetry**: Gestão de dependências e ambientes virtuais.

---

## 🛠️ Como Executar

### 1. Pré-requisitos
Certifique-se de ter o [Poetry](https://python-poetry.org/) instalado em sua máquina.

### 2. Instalação e Configuração
```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/shieldpay.git](https://github.com/seu-usuario/shieldpay.git)
cd shieldpay

# Instale as dependências
poetry install
```

### 3. Rodando o Servidor
```Bash
poetry run uvicorn src.api:app --reload
Acesse a documentação interativa em: http://127.0.0.1:8000/docs
```
📝 Licença
Este projeto está sob a licença MIT.
