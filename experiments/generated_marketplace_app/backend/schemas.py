from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    pass

class ProductUpdate(BaseModel):
    pass

class ProductResponse(ProductCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    pass

class OrderUpdate(BaseModel):
    pass

class OrderResponse(OrderCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class ProductOrderCreate(BaseModel):
    product_id: str
    order_id: str

class ProductOrderUpdate(BaseModel):
    product_id: Optional[str] = None
    order_id: Optional[str] = None

class ProductOrderResponse(ProductOrderCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)
