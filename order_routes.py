from fastapi import APIRouter, Depends
from dependencies import get_session
from sqlalchemy.orm import Session
from  models import Order
from schemas import OrderSchema

order_router = APIRouter(prefix='/order', tags=["order"])


@order_router.get('/')
async def orders():
    """
    Essa é a rota padrão de pedidos
    """
    return {"message":"Você está na rota de Pedidos"}

@order_router.post('/order')
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.user)
    session.add(new_order)
    session.commit()
    return {'message':f'Pedido {new_order.id} criado com sucesso.'}