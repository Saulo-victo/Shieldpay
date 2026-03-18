# 🛡️ ShieldPay - API de Pagamentos Simplificada

O **ShieldPay** é uma API de transferências financeiras robusta, inspirada no desafio do PicPay. O projeto foca em transações seguras entre usuários e lojistas, aplicando conceitos avançados de arquitetura de software para garantir a integridade dos dados.

## 🚀 Funcionalidades

- **Cadastro de Usuários**: Diferenciação entre usuários comuns e lojistas.
- **Carteira Digital**: Controle de saldo e histórico.
- **Transferências Blindadas**: 
    - Validação de saldo.
    - **Autorização Externa**: Consulta um serviço de terceiros antes de processar o pagamento.
    - **Notificações em Tempo Real**: Envio de confirmação via Webhook após o sucesso da transação.
    - **Garantia de Transação (ACID)**: Uso de Unit of Work para garantir que, se um serviço externo falhar, o dinheiro retorne ao pagador (Rollback).

## 🏗️ Arquitetura e Padrões de Projeto

Este projeto foi construído seguindo os princípios da **Clean Architecture** e **DDD (Domain Driven Design)** para manter o código testável e desacoplado:

- **Unit of Work (UoW)**: Gerenciamento de transações de banco de dados.
- **Repository Pattern**: Abstração da camada de dados.
- **Dependency Injection**: Injeção de serviços externos (Autorizador e Notificador).
- **Service Layer**: Lógica de negócio isolada dos detalhes de infraestrutura.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12+**
* **FastAPI**: Framework web de alta performance.
* **SQLAlchemy**: ORM para mapeamento de dados.
* **Pydantic**: Validação de dados e tipagem.
* **HTTPX**: Cliente HTTP assíncrono para integração com APIs externas.
* **SQLite**: Banco de dados relacional.
* **Poetry**: Gerenciamento de dependências.

## 🔧 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/shieldpay.git](https://github.com/SEU_USUARIO/shieldpay.git)
   cd shieldpay
   ```

2. **Instale as dependências (via Poetry):**
   ```bash
    poetry install
   ```

3. **Configure as variáveis de ambiente (Crie o arquivo .env na raiz do projeto):**
   ```bash
    NOTIFICATION_URL="SUA_URL_DO_WEBHOOK_SITE"
    AUTHORIZER_URL="[https://util.devi.tools/api/v2/authorize](https://util.devi.tools/api/v2/authorize)"
   ```
4. **Inicie o servidor:**
   ```bash
    fastapi dev src/web/api.py
   ```

5. **Acesse a documentação para testar via Swagger UI:**
   ```bash
    http://127.0.0.1:8000/docs
   ```

Desenvolvido por [Saulo Victo] - [<a href="https://www.linkedin.com/in/saulo-victo-soares-3786873b2/">linkedin</a>]

















   
   
