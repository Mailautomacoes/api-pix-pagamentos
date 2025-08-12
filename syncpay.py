import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

# Variáveis de ambiente
API_KEY = os.getenv("SYNCPAY_API_KEY")
URL_PIX = os.getenv("SYNCPAY_URL_PIX", "https://api.syncpay.pro/v1/gateway/api")
URL_CASHOUT = os.getenv("SYNCPAY_URL_CASHOUT", "https://api.syncpay.pro/c1/cashout/api")
URL_REFUND = os.getenv("SYNCPAY_URL_REFUND", "https://api.syncpay.pro/v1/gateway/api/refund")
POSTBACK_URL = os.getenv("POSTBACK_URL", "http://127.0.0.1:8000/notificar")

# Codificar API_KEY em Base64 como exigido pela SyncPay
if API_KEY:
    API_KEY_B64 = base64.b64encode(API_KEY.encode()).decode()
    print(f"🔑 DEBUG: API_KEY original: {API_KEY[:10]}...")
    print(f"🔑 DEBUG: API_KEY Base64: {API_KEY_B64[:20]}...")
else:
    print("❌ API_KEY não encontrada!")
    API_KEY_B64 = None

HEADERS = {
    "Authorization": f"Basic {API_KEY_B64}",
    "Content-Type": "application/json"
}

def criar_pagamento_pix(dados):
    """Cria pagamento PIX usando endpoint simples da SyncPay"""
    try:
        print(f"📤 Enviando para: {URL_PIX}/")
        print(f"📋 Dados: {dados}")
        print(f"� Headers: Authorization: Basic {API_KEY_B64[:20]}...")
        
        response = requests.post(f"{URL_PIX}/", json=dados, headers=HEADERS)
        
        print(f"📊 Status da resposta: {response.status_code}")
        result = response.json()
        print(f"📝 Resposta da API: {result}")
        
        return result
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao criar pagamento Pix: {e}"
        print(error_msg)
        return {"error": error_msg}

def criar_pagamento_pix_completo(dados_cliente: dict, valor: float, ip: str):
    """Cria pagamento PIX completo usando endpoint split da SyncPay"""
    payload = {
        "amount": valor,
        "customer": {
            "name": dados_cliente["nome"],
            "email": dados_cliente["email"],
            "cpf": dados_cliente["cpf"],
            "phone": dados_cliente.get("phone", "9999999999"),
            "address": {
                "street": "Rua Genérica",
                "streetNumber": "123",
                "complement": "Complemento",
                "zipCode": "00000000",
                "neighborhood": "Bairro",
                "city": "Cidade",
                "state": "SP",
                "country": "br"
            }
        },
        "pix": {
            "expiresInDays": 2
        },
        "postbackUrl": POSTBACK_URL,
        "metadata": "metadata",
        "traceable": True,
        "ip": ip
    }

    try:
        print(f"📤 Enviando para: {URL_PIX}/split/")
        print(f"📋 Payload: {payload}")
        print(f"🔒 Headers: Authorization: Basic {API_KEY_B64[:20]}...")
        
        response = requests.post(f"{URL_PIX}/split/", json=payload, headers=HEADERS)
        
        print(f"📊 Status da resposta: {response.status_code}")
        result = response.json()
        print(f"📝 Resposta da API: {result}")
        
        return result
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao criar pagamento Pix completo: {e}"
        print(error_msg)
        return {"error": error_msg}

def processar_webhook(dados_webhook: dict):
    """
    Função para processar o JSON recebido via Webhook da SyncPay,
    identificando se é Depósito ou Saque e retornando uma resposta padrão.
    """
    
    if (dados_webhook) :
        transaction_type = "Desconhecido"

        # Verifica se é depósito
        if "client_name" in dados_webhook and "paymentcode" in dados_webhook:
            transaction_type = "Depósito"
            # Aqui você pode implementar a lógica de gravação em banco de dados ou outras ações necessárias

        # Verifica se é saque
        elif "beneficiaryname" in dados_webhook and "pixkey" in dados_webhook:
            transaction_type = "Saque"
            # Aqui você pode implementar a lógica de gravação em banco de dados ou outras ações necessárias

        return {"status": "success", "message": f"{transaction_type} recebido com sucesso."}
    
    else :
        # http_response_code(400);
        return {"status": "error", "message": "Dados do webhook inválidos."}

def criar_saque_pix(dados_saque: dict):
    """Cria saque PIX seguindo documentação da SyncPay"""
    # Adicionar api_key no payload conforme documentação
    payload = {
        "api_key": API_KEY,  # SyncPay exige api_key no payload para cashout
        **dados_saque
    }
    
    try:
        print(f"📤 Enviando saque para: {URL_CASHOUT}/")
        print(f"📋 Payload: {payload}")
        print(f"🔒 Headers: Authorization: Basic {API_KEY_B64[:20]}...")
        
        response = requests.post(URL_CASHOUT, json=payload, headers=HEADERS)
        
        print(f"📊 Status da resposta: {response.status_code}")
        result = response.json()
        print(f"📝 Resposta da API: {result}")
        
        return result
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao criar saque Pix: {e}"
        print(error_msg)
        return {"error": error_msg}

def solicitar_reembolso_pix(dados_refund: dict):
    """Solicita reembolso PIX seguindo documentação da SyncPay"""
    # Adicionar api_key no payload conforme documentação
    payload = {
        "api_key": API_KEY,  # SyncPay exige api_key no payload para refund
        **dados_refund
    }
    
    try:
        print(f"📤 Enviando reembolso para: {URL_REFUND}/")
        print(f"📋 Payload: {payload}")
        print(f"🔒 Headers: Authorization: Basic {API_KEY_B64[:20]}...")
        
        response = requests.post(URL_REFUND, json=payload, headers=HEADERS)
        
        print(f"📊 Status da resposta: {response.status_code}")
        result = response.json()
        print(f"📝 Resposta da API: {result}")
        
        return result
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao solicitar reembolso Pix: {e}"
        print(error_msg)
        return {"error": error_msg}

