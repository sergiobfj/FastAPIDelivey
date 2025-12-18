from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth', tags=["auth"])

@auth_router.get('/')
async def auth():
    """
    Essa é a rota padrão de autenticação
    """
    return{"message":"Você está na rota de autenticação", "auth":False}

