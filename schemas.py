from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]
    
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