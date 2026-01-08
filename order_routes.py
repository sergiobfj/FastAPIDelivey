from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, verify_user
from sqlalchemy.orm import Session
from models import Order, User
from schemas import OrderSchema

order_router = APIRouter(prefix='/order', tags=["order"], dependencies=[Depends(verify_user)])


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

order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_user)):
    order = session.query(Order).filter(Order.id==order_id).first()

    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encotrado.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar esse pedido.")
    
    order.status = "CANCELADO"
    session.commit()
    return {
        "message": f"Pedido número: {order_id} cancelado.",
        "order": order
    }