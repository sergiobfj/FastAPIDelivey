from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from dependencies import get_session, verify_user
from sqlalchemy.orm import Session
from models import ItemOrder, Order, User
from schemas import OrderSchema, OrderItemSchema

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


@order_router.get("/list")
async def list_order(session: Session = Depends(get_session), user: User = Depends (verify_user)):
    if not user.admin:
        raise HTTPException(status_code=401, detail='Usuário não autenticado.')
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders
        }
    
@order_router.post("/order/add-item/{order_id}")
async def add_item(order_id: int, item_order_schema: OrderItemSchema, session: Session = Depends(get_session), user: User = Depends(verify_user)):
    order = session.query(Order).filter(Order.id==order_id).first()

    if not order:
        raise HTTPException(status_code=400, detail="Pedido não existe")
    elif not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail='Usuário não autenticado.')
    
    item_order = ItemOrder(item_order_schema.quant, item_order_schema.flavor, item_order_schema.size, item_order_schema.price, order_id)

    session.add(item_order)
    order.calc_price()
    session.commit()
    return{
        "message": "Item criado.",
        "item_id": item_order.id,
        "price": order.price
    }