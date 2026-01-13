from ctypes import sizeof
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

# cria a conexão com o banco
db = create_engine("sqlite:///banco.db")

# cria a base do banco de dados
Base = declarative_base()

# cria as classes/tabelas do banco
# user
class User(Base):
    __tablename__ = "Users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

# order

class Order(Base):
    __tablename__ = "Orders"

#    STATUS_ORDERS = (
#        ("PENDENTE","PENDENTE"),
#        ("CANCELADO","CANCELADO"),
#       ("FINALIZADO","FINALIZADO")
#    )
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user = Column("user",ForeignKey("Users.id") )
    status = Column("status",String)
    price = Column("price", Float)
    itens = relationship("ItemOrder", cascade="all, delete")

    def __init__(self, user, status="PENDENTE", price=0):
        self.status = status
        self.user = user
        self.price = price

    def calc_price(self):
        order_price = 0
        for item in self.itens:
            item_price = item.unity_price * item.quantity
            order_price += item_price
        self.price = order_price

# order_items

class ItemOrder(Base):
    __tablename__ = "Items_order"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = ("quantity", Integer)
    flavor = ("flavor", String)
    size = ("size", String)
    unity_price = ("unity_price", Float)
    order = ("order", ForeignKey("Orders.id"))

    def __ini__(self, quantity, flavor, size, unity_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unity_price = unity_price
        self.order = order

# executa a criação dos metadados do seu banco 