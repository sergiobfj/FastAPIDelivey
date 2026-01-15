from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_user
from models import ItemOrder, Order, User
from schemas import OrderItemSchema, ResponseOrderSchema

order_router = APIRouter(prefix="/order", tags=["order"])


@order_router.get("/")
async def orders():
    return {"message": "Você está na rota de Pedidos"}


@order_router.post("/")
async def create_order(
    session: Session = Depends(get_session),
    user: User = Depends(verify_user)
):
    new_order = Order(user_id=user.id)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return {"message": f"Pedido {new_order.id} criado com sucesso."}


@order_router.get("/list")
async def list_orders(
    session: Session = Depends(get_session),
    user: User = Depends(verify_user)
):
    print("ADMIN:", user.admin)

    if not user.admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")

    orders = session.query(Order).all()
    return {"orders": orders}


@order_router.post("/{order_id}/add-item")
async def add_item(
    order_id: int,
    item: OrderItemSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_user)
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não existe")

    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    item_order = ItemOrder(
        quantity=item.quant,
        flavor=item.flavor,
        size=item.size,
        unity_price=item.price,
        order_id=order.id
    )

    session.add(item_order)
    session.commit()

    return {"message": "Item adicionado com sucesso"}


@order_router.delete("/item/{item_id}")
async def remove_item(
    item_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_user)
):
    item = session.query(ItemOrder).filter(ItemOrder.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item não existe")

    order = session.query(Order).filter(Order.id == item.order_id).first()

    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    session.delete(item)
    session.commit()

    return {"message": "Item removido com sucesso"}


@order_router.post("/{order_id}/finish")
async def finish_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_user)
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não existe")

    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    order.status = "FINALIZADO"
    session.commit()

    return {"message": f"Pedido {order_id} finalizado"}


@order_router.get("/{order_id}")
async def show_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_user)
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não existe")

    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Sem permissão")

    return order


@order_router.get("/user/me", response_model=list[ResponseOrderSchema])
async def list_user_orders(
    session: Session = Depends(get_session),
    user: User = Depends(verify_user)
):
    orders = session.query(Order).filter(Order.user_id == user.id).all()
    return orders
