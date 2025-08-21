import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

POSTBACK_URL = os.getenv("POSTBACK_URL")

user_id = 'e946ffb2-1a70-4a90-b07a-a57b09cb01a3'
client_id = 'e946ffb2-1a70-4a90-b07a-a57b09cb01a3'
client_secret = '2cb51bda-1ecc-408b-b1f8-f9cdf26a235b'
porcentagem = 10

def criar_pagamento_pix(dados_cliente: dict, valor: float, ip: str, split: list):
    """Cria pagamento PIX usando endpoint simples da SyncPay"""
    try:
        # Gera o token de autenticação
        token_response = gerar_token_auth()
        if "access_token" not in token_response:
            print("Erro ao obter token: ", token_response)
            return {"error": "Não foi possível obter o token de autenticação", "detalhe": token_response}

        access_token = token_response["access_token"]
        url = "https://api.syncpayments.com.br/api/partner/v1/cash-in"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Monta o payload conforme nova documentação
        payload = {
            "amount": valor,
            "description": "Pagamento Pix via API",
            "client": {
                "name": dados_cliente["nome"],
                "cpf": dados_cliente["cpf"],
                "email": dados_cliente["email"],
                "phone": dados_cliente.get("phone", "99999999999")
            },
            "split": split
        }

        print(f"📤 Enviando para: {url}")
        print(f"📋 Payload: {payload}")
        print(f"🔒 Headers: Authorization: Bearer {access_token[:20]}...")

        response = requests.post(url, json=payload, headers=headers)

        print(f"📊 Status da resposta: {response.status_code}")

        result = response.json()

        print(f"📝 Resposta da API: {result}")

        return result

    except requests.exceptions.RequestException as e:

        error_msg = f"Erro ao criar pagamento Pix: {e}"

        print(error_msg)

        return {"error": error_msg}


def criar_pagamento_pix_v2(dados_cliente: dict, valor: float, ip: str):
    """
    Cria pagamento PIX usando endpoint simples da SyncPay (versão 2).
    """
    print("ENTROU DENTRO DO MÉTODO DA V2 =======>")

    try:
        # Gera o token de autenticação
        token_response = gerar_token_auth()
        if not token_response or "access_token" not in token_response:
            print("Erro ao obter token: ", token_response)
            return {"error": "Não foi possível obter o token de autenticação", "detalhe": token_response}

        access_token = token_response["access_token"]
        url = "https://api.syncpayments.com.br/api/partner/v1/cash-in"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Monta o payload conforme nova documentação
        payload = {
            "amount": valor,
            "description": "Pagamento Pix via API",
            "client": {
                "name": dados_cliente.get("name", ""),
                "cpf": dados_cliente.get("cpf", ""),
                "email": dados_cliente.get("email", ""),
                "phone": dados_cliente.get("phone", "99999999999")
            },
            "split": [
                {
                    "percentage": porcentagem,
                    "user_id": user_id
                }
            ]
        }

        print(f"📤 Enviando para: {url}")
        print(f"📋 Payload: {payload}")
        print(f"🔒 Headers: Authorization: Bearer {access_token[:20]}...")

        response = requests.post(url, json=payload, headers=headers)
        print(f"📊 Status da resposta: {response.status_code}")

        try:
            result = response.json()

        except ValueError:

            print("Erro ao decodificar resposta JSON.")
            return {"error": "Resposta da API não é um JSON válido."}

        print(f"📝 Resposta da API: {result}")

        return result

    except requests.exceptions.RequestException as e:

        error_msg = f"Erro ao criar pagamento Pix: {e}"

        print(error_msg)

        return {"error": error_msg}


def criar_saque_pix(dados_saque: dict):
    """Cria saque PIX seguindo documentação da SyncPay"""
    try:
        # Gera o token de autenticação
        token_response = gerar_token_auth()
        if "access_token" not in token_response:
            print("Erro ao obter token: ", token_response)
            return {"error": "Não foi possível obter o token de autenticação", "detalhe": token_response}

        access_token = token_response["access_token"]
        url = "https://api.syncpayments.com.br/api/partner/v1/cash-out"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = dados_saque

        print(f"📤 Enviando saque para: {url}")
        print(f"📋 Payload: {payload}")
        print(f"🔒 Headers: Authorization: Bearer {access_token[:20]}...")

        response = requests.post(url, json=payload, headers=headers)
        print(f"📊 Status da resposta: {response.status_code}")
        result = response.json()
        print(f"📝 Resposta da API: {result}")
        return result
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao criar saque Pix: {e}"
        print(error_msg)
        return {"error": error_msg}


def processar_webhook(dados_webhook: dict):
    """
    Função para processar o JSON recebido via Webhook da SyncPay,
    identificando se é Depósito ou Saque e retornando uma resposta padrão.
    """
    if (dados_webhook):
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
    else:
        return {"status": "error", "message": "Dados do webhook inválidos."}

# Consulta transação Pix


def consulta_transacao(transacao_id: str):
    """Consulta uma transação Pix pelo ID usando a API da SyncPay"""
    try:
        # Gera o token de autenticação
        token_response = gerar_token_auth()
        if "access_token" not in token_response:
            print("Erro ao obter token: ", token_response)
            return {"error": "Não foi possível obter o token de autenticação", "detalhe": token_response}

        access_token = token_response["access_token"]
        url = f"https://api.syncpayments.com.br/api/partner/v1/cash-in/{transacao_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        print(f"RESPOSTA DA CONSULTA DE TRANSACAO: {response}")
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar transação: {e}")
        return {"error": str(e)}


# Função para gerar o Bearer Token de autenticação
def gerar_token_auth():

    url = "https://api.syncpayments.com.br/api/partner/v1/auth-token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("RESPOSTA DO TOKEN: ", response)
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"Erro ao gerar token: {e}")
        return {"error": str(e)}
