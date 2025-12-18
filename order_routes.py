from fastapi import APIRouter

order_router = APIRouter(prefix='/order', tags=["order"])


@order_router.get('/')
async def orders():
    """
    Essa é a rota padrão de pedidos
    """
    return {"message":"Você está na rota de Pedidos"}