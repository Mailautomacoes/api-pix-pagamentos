from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import secrets
from dotenv import load_dotenv
from syncpay import criar_pagamento_pix, criar_pagamento_pix_completo, criar_saque_pix, solicitar_reembolso_pix

load_dotenv()

# Variáveis de ambiente
HOST = os.getenv("HOST", "0.0.0.0")  # Azure precisa de 0.0.0.0
PORT = int(os.getenv("PORT", "8000"))
POSTBACK_URL = os.getenv("POSTBACK_URL", "https://seu-app-name.azurewebsites.net/notificar")

# Credenciais para acessar a documentação
DOCS_USERNAME = os.getenv("DOCS_USERNAME", "admin")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "admin123")

security = HTTPBasic()


app = FastAPI(docs_url=None, redoc_url=None)  # Desabilita as rotas padrão

# Configuração do CORS para todas as origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClientePix(BaseModel):
    nome: str
    email: str
    cpf: str
    valor: float
    phone: str = "(99)99999-9999"

class CashOutPix(BaseModel):
    amount: float
    pixKey: str
    pixType: str  # CPF, CNPJ, EMAIL, PHONE, RANDOM
    beneficiaryName: str
    beneficiaryDocument: str
    description: str = "Pagamento generico"
    postbackUrl: str = None  # Será preenchido automaticamente

class RefundPix(BaseModel):
    id: int
    external_reference: str

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Pagamento Pix!"}


@app.post("/pagamento-pix")
def pagamento_pix(cliente: ClientePix, request: Request):
    dados_cliente = {
        "nome": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "phone": cliente.phone
    }

    ip_do_cliente = request.client.host
    return criar_pagamento_pix_completo(dados_cliente, cliente.valor, ip_do_cliente)


@app.post("/pagamento-pix-v2")
def pagamento_pix_v2(cliente: ClientePix, request: Request):
    ip_do_cliente = request.client.host
    dados_cliente = {
        "name": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "phone": cliente.phone
    }

    payload = {
        "amount": cliente.valor,
        "customer": dados_cliente,
        "postbackUrl": POSTBACK_URL,
        "ip": ip_do_cliente,
    }
    return criar_pagamento_pix(payload)


@app.post("/cashout")
def cashout_pix(saida: CashOutPix, request: Request):
    dados_saque = {
        "amount": saida.amount,
        "pixKey": saida.pixKey,
        "pixType": saida.pixType,
        "beneficiaryName": saida.beneficiaryName,
        "beneficiaryDocument": saida.beneficiaryDocument,
        "description": saida.description,
        "postbackUrl": POSTBACK_URL
    }
    return criar_saque_pix(dados_saque)


@app.post("/refund")
def refund_pix(reembolso: RefundPix, request: Request):
    dados_refund = {
        "id": reembolso.id,
        "external_reference": reembolso.external_reference
    }
    return solicitar_reembolso_pix(dados_refund)


@app.post("/webhook")
async def receber_webhook(payload: dict):
    from syncpay import processar_webhook
    return processar_webhook(payload)

@app.post("/notificar")
def notificar(dados_pix: dict):
    print("Dados recebidos para notificação:", dados_pix)
    return {
        "status": "ok",
        "mensagem": "Notificação de pagamento enviada com sucesso"
    }

# Função para verificar credenciais
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Rotas protegidas para documentação
@app.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(authenticate)):
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(openapi_url="/openapi.json", title="API Docs")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(authenticate)):
    return get_openapi(title="API de Pagamentos SyncPay", version="1.0.0", routes=app.routes)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)