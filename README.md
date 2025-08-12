# 🚀 API de Pagamentos PIX

API REST para integração com pagamentos PIX utilizando a SyncPay. Desenvolvida em FastAPI para alta performance e fácil integração.

## 📋 Funcionalidades

- ✅ **Criar Pagamentos PIX** - Gerar QR Codes e códigos PIX
- ✅ **Saques PIX** - Transferências para contas via PIX
- ✅ **Reembolsos** - Estorno de pagamentos
- ✅ **Webhooks** - Notificações automáticas de status
- ✅ **Autenticação** - Documentação protegida
- ✅ **Containerização** - Deploy com Docker
- ✅ **Deploy Azure** - Configurado para Azure Web App

## 🛠️ Tecnologias

- **Python 3.12** - Linguagem principal
- **FastAPI** - Framework web moderno e rápido
- **Uvicorn/Gunicorn** - Servidor ASGI para produção
- **Pydantic** - Validação de dados
- **Requests** - Cliente HTTP para SyncPay API
- **Docker** - Containerização
- **GitHub Actions** - CI/CD pipeline

## 🚀 Quick Start

### 1. Instalação Local

```bash
# Clone o repositório
git clone https://github.com/Lu1zH3nriq/api-pix.git
cd api-pix

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Execute a aplicação
python main.py
```

### 2. Usando Docker

```bash
# Build da imagem
docker build -t api-pix .

# Execute o container
docker run -p 8000:8000 --env-file .env api-pix
```

## 📚 Documentação e Exemplos

### 📖 Documentação Interativa
- **Swagger UI**: `https://api-pix-dev.azurewebsites.net/docs`
- **ReDoc**: `https://api-pix-dev.azurewebsites.net/redoc`
- **Credenciais**: admin / admin123

### 📝 Exemplos de Uso
- **[EXEMPLOS_JSON.md](./EXEMPLOS_JSON.md)** - Guia completo com exemplos de JSON
- **[collection.json](./collection.json)** - Collection para Postman/Insomnia
- **[test_api.py](./test_api.py)** - Script Python para testes

### 🧪 Testando a API

```bash
# Usando o script de teste
python test_api.py                 # Todos os testes
python test_api.py health         # Apenas health check
python test_api.py pix1           # Apenas pagamento PIX v1

# Usando cURL
curl -X GET "https://api-pix-dev.azurewebsites.net/"

# Criando um pagamento
curl -X POST "https://api-pix-dev.azurewebsites.net/pagamento-pix" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao.silva@email.com",
    "cpf": "12345678901",
    "valor": 100.50,
    "phone": "(11)99999-9999"
  }'
```

## 🔌 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Status da API |
| `POST` | `/pagamento-pix` | Criar pagamento PIX (v1) |
| `POST` | `/pagamento-pix-v2` | Criar pagamento PIX (v2) |
| `POST` | `/cashout` | Criar saque PIX |
| `POST` | `/refund` | Solicitar reembolso |
| `POST` | `/webhook` | Webhook da SyncPay |
| `POST` | `/notificar` | Endpoint de notificação |

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# SyncPay API
SYNCPAY_API_KEY=sua_chave_api_aqui
SYNCPAY_URL_PIX=https://api.syncpay.pro/v1/gateway/api
SYNCPAY_URL_CASHOUT=https://api.syncpay.pro/c1/cashout/api
SYNCPAY_URL_REFUND=https://api.syncpay.pro/v1/gateway/api/refund

# Servidor
HOST=0.0.0.0
PORT=8000
POSTBACK_URL=https://api-pix-dev.azurewebsites.net/notificar

# Documentação
DOCS_USERNAME=admin
DOCS_PASSWORD=admin123
```

## 🚀 Deploy

### Azure Web App (Automático)

O deploy é automático via GitHub Actions quando você faz push para a branch `main`:

1. **Fork** este repositório
2. **Configure** as variáveis de ambiente no Azure Web App
3. **Atualize** o arquivo `.github/workflows/azure-deploy.yml` com o nome do seu app
4. **Push** para a branch main

### Deploy Manual

```bash
# Usando Azure CLI
az webapp up --name sua-app --resource-group seu-grupo

# Usando Docker
docker push seu-registry/api-pix:latest
```

## 🔐 Segurança

- ✅ Documentação protegida por Basic Auth
- ✅ Validação de dados com Pydantic
- ✅ Variáveis de ambiente para credenciais
- ✅ CORS configurado para produção
- ✅ Headers de segurança

## 📊 Monitoramento

- **Logs**: Acessíveis via Azure Portal
- **Health Check**: `GET /`
- **Metrics**: Integração com Azure Application Insights

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

- 📧 **Email**: [seu-email@exemplo.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/Lu1zH3nriq/api-pix/issues)
- 📖 **Documentação**: [Swagger UI](https://api-pix-dev.azurewebsites.net/docs)

---

⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!