# Exemplos de JSON para Requisições da API de Pagamentos PIX

Este documento contém exemplos de JSON para todas as requisições da API.

## 🚀 Informações Gerais

**Base URL**: `https://api-pix-dev.azurewebsites.net`

**Autenticação para Documentação**:
- Usuário: `admin`
- Senha: `admin123`

**Documentação Swagger**: `https://api-pix-dev.azurewebsites.net/docs`

---

## 📝 Endpoints e Exemplos

### 1. GET `/` - Verificar Status da API

**Requisição**: `GET /`

**Resposta**:
```json
{
  "message": "Bem-vindo à API de Pagamento Pix!"
}
```

---

### 2. POST `/pagamento-pix` - Criar Pagamento PIX (Versão 1)

**Requisição**: `POST /pagamento-pix`

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body**:
```json
{
  "nome": "João Silva",
  "email": "joao.silva@email.com",
  "cpf": "12345678901",
  "valor": 100.50,
  "phone": "(11)99999-9999"
}
```

**Resposta Esperada**:
```json
{
  "id": 12345,
  "amount": 100.50,
  "status": "pending",
  "pixCode": "00020126580014BR.GOV.BCB.PIX...",
  "expiresAt": "2025-07-16T23:59:59Z",
  "customer": {
    "name": "João Silva",
    "email": "joao.silva@email.com",
    "cpf": "12345678901"
  }
}
```

---

### 3. POST `/pagamento-pix-v2` - Criar Pagamento PIX (Versão 2)

**Requisição**: `POST /pagamento-pix-v2`

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body**:
```json
{
  "nome": "Maria Santos",
  "email": "maria.santos@email.com",
  "cpf": "98765432100",
  "valor": 250.75,
  "phone": "(21)88888-8888"
}
```

**Resposta Esperada**:
```json
{
  "id": 12346,
  "amount": 250.75,
  "status": "pending",
  "pixCode": "00020126580014BR.GOV.BCB.PIX...",
  "qrCode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "expiresAt": "2025-07-16T23:59:59Z"
}
```

---

### 4. POST `/cashout` - Criar Saque PIX

**Requisição**: `POST /cashout`

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body**:
```json
{
  "amount": 150.00,
  "pixKey": "joao.silva@email.com",
  "pixType": "email",
  "beneficiaryName": "João Silva",
  "beneficiaryDocument": "12345678901",
  "description": "Saque para conta pessoal"
}
```

**Tipos de PIX válidos**:
- `email` - E-mail
- `cpf` - CPF
- `cnpj` - CNPJ
- `phone` - Telefone
- `random` - Chave aleatória

**Resposta Esperada**:
```json
{
  "id": 12347,
  "amount": 150.00,
  "status": "processing",
  "beneficiaryName": "João Silva",
  "beneficiaryDocument": "12345678901",
  "createdAt": "2025-07-14T10:30:00Z"
}
```

---

### 5. POST `/refund` - Solicitar Reembolso

**Requisição**: `POST /refund`

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body**:
```json
{
  "id": 12345,
  "external_reference": "REF123456789"
}
```

**Resposta Esperada**:
```json
{
  "id": 12345,
  "refundId": 98765,
  "status": "refund_pending",
  "amount": 100.50,
  "refundAmount": 100.50,
  "processedAt": "2025-07-14T10:35:00Z"
}
```

---

### 6. POST `/webhook` - Receber Webhook da SyncPay

**Requisição**: `POST /webhook`

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body para Depósito**:
```json
{
  "id": 12345,
  "amount": 100.50,
  "status": "approved",
  "client_name": "João Silva",
  "client_email": "joao.silva@email.com",
  "client_cpf": "12345678901",
  "paymentcode": "PIX123456789",
  "paid_at": "2025-07-14T10:00:00Z",
  "created_at": "2025-07-14T09:30:00Z"
}
```

**Body para Saque**:
```json
{
  "id": 12347,
  "amount": 150.00,
  "status": "completed",
  "beneficiaryname": "João Silva",
  "beneficiarydocument": "12345678901",
  "pixkey": "joao.silva@email.com",
  "pixtype": "email",
  "processed_at": "2025-07-14T10:45:00Z"
}
```

**Resposta**:
```json
{
  "status": "success",
  "message": "Depósito recebido com sucesso."
}
```

---

### 7. POST `/notificar` - Endpoint de Notificação

**Requisição**: `POST /notificar`

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body**:
```json
{
  "transactionId": 12345,
  "status": "approved",
  "amount": 100.50,
  "timestamp": "2025-07-14T10:00:00Z"
}
```

**Resposta**:
```json
{
  "status": "ok",
  "mensagem": "Notificação de pagamento enviada com sucesso"
}
```

---

## 🔐 Autenticação

A API não requer autenticação para os endpoints de pagamento, mas a documentação (Swagger) está protegida por Basic Auth:

**Credenciais**:
- **Usuário**: `admin`
- **Senha**: `admin123`

---

## 📱 Status de Pagamentos

### Status Possíveis:
- `pending` - Aguardando pagamento
- `approved` - Pagamento aprovado
- `cancelled` - Pagamento cancelado
- `expired` - Pagamento expirado
- `processing` - Processando
- `completed` - Concluído
- `failed` - Falhou
- `refund_pending` - Reembolso pendente
- `refunded` - Reembolsado

---

## 🚨 Códigos de Erro HTTP

- `200` - Sucesso
- `400` - Dados inválidos
- `401` - Não autorizado (apenas para documentação)
- `404` - Endpoint não encontrado
- `422` - Erro de validação
- `500` - Erro interno do servidor

---

## 📞 Exemplos com cURL

### Criar Pagamento PIX:
```bash
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

### Criar Saque:
```bash
curl -X POST "https://api-pix-dev.azurewebsites.net/cashout" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 150.00,
    "pixKey": "joao.silva@email.com",
    "pixType": "email",
    "beneficiaryName": "João Silva",
    "beneficiaryDocument": "12345678901",
    "description": "Saque para conta pessoal"
  }'
```

### Solicitar Reembolso:
```bash
curl -X POST "https://api-pix-dev.azurewebsites.net/refund" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 12345,
    "external_reference": "REF123456789"
  }'
```

---

## 🌐 Testando a API

1. **Swagger UI**: Acesse `https://api-pix-dev.azurewebsites.net/docs`
2. **ReDoc**: Acesse `https://api-pix-dev.azurewebsites.net/redoc`
3. **Postman**: Importe os exemplos JSON acima
4. **Insomnia**: Use os exemplos cURL fornecidos

---

## ⚠️ Observações Importantes

1. **Valores monetários**: Sempre use ponto (.) como separador decimal
2. **CPF**: Apenas números, sem pontos ou hífens
3. **Telefone**: Formato sugerido: `(xx)xxxxx-xxxx`
4. **E-mail**: Deve ser um e-mail válido
5. **Chaves PIX**: Devem ser válidas conforme o tipo especificado
6. **Webhook**: O endpoint `/webhook` é chamado automaticamente pela SyncPay
7. **Postback URL**: Configurada automaticamente para o endpoint `/notificar`
