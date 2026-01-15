from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    admin: bool = False
    active: bool = True

    
    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    user: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
    
class OrderItemSchema(BaseModel):
    quant: int
    flavor: str
    size: str
    price: float

    class Config:
        from_attributes = True

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float

    class Config:
        from_attributes = True