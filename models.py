from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="PENDENTE")
    price = Column(Float, default=0)

    itens = relationship("ItemOrder", back_populates="order", cascade="all, delete-orphan")

class ItemOrder(Base):
    __tablename__ = "items_order"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    flavor = Column(String, nullable=False)
    size = Column(String, nullable=False)
    unity_price = Column(Float, nullable=False)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="itens")

    

from database import engine
Base.metadata.create_all(bind=engine)
