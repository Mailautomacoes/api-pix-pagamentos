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
from syncpay import criar_pagamento_pix, criar_pagamento_pix_v2, criar_saque_pix, consulta_transacao, gerar_token_auth

load_dotenv()

# Variáveis de ambiente
HOST = os.getenv("HOST", "0.0.0.0")  # Azure precisa de 0.0.0.0
PORT = int(os.getenv("PORT", "8000"))
POSTBACK_URL = os.getenv("POSTBACK_URL")

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
    phone: str = "34998524585"
    split: List[SplitPix]

class ClientePixV2(BaseModel):
    nome: str
    email: str
    cpf: str
    valor: float
    phone: str = "99999999999"



class DocumentPix(BaseModel):
    type: str  # cpf ou cnpj
    number: str

class CashOutPix(BaseModel):
    amount: float
    description: str = None
    pix_key_type: str  # CPF, CNPJ, EMAIL, PHONE, EVP
    pix_key: str
    document: DocumentPix


class Transacao(BaseModel):
    id: int
    external_reference: str


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Pagamento Pix!"}


@app.get("/saldo")
def saldo():
    return consulta_saldo()


@app.post("/pagamento-pix")
def pagamento_pix(cliente: ClientePix, request: Request):
    dados_cliente = {
        "nome": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "phone": cliente.phone
    }
    split = [split.dict() for split in cliente.split]
    ip_do_cliente = request.client.host
    
    print('Cliente: ', cliente)
    print('Valor que foi enviado: ', cliente.valor)
    print('IP DO CLIENTE QUE SOLICITOU O SAQUE: ', ip_do_cliente)
    
    
    return criar_pagamento_pix(dados_cliente, cliente.valor, ip_do_cliente, split)


@app.post("/pagamento-pix-v2")
def pagamento_pix_v2(cliente: ClientePixV2, request: Request):
    print("ENTROU NA ROTA PIX V2")
    ip_do_cliente = request.client.host
    
    dados_cliente = {
        "name": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "phone": cliente.phone
    }
    
    return criar_pagamento_pix_v2(dados_cliente, cliente.valor, ip_do_cliente)


@app.post("/cashout")
def cashout_pix(saida: CashOutPix, request: Request):
    dados_saque = {
        "amount": saida.amount,
        "description": saida.description,
        "pix_key_type": saida.pix_key_type,
        "pix_key": saida.pix_key,
        "document": saida.document.dict()
    }
    return criar_saque_pix(dados_saque)


@app.post("/transacao")
def transacaoPix(reembolso: Transacao, request: Request):
    dados_transacao = {
        "id": reembolso.id,
        "external_reference": reembolso.external_reference
    }
    return consulta_transacao(dados_transacao)


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


@app.post("/teste-token")
def testeToken(req: Request):
    return gerar_token_auth();


# Função para verificar credenciais
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, DOCS_USERNAME)
    correct_password = secrets.compare_digest(
        credentials.password, DOCS_PASSWORD)
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
