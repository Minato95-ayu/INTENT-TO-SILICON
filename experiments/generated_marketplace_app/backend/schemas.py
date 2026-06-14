from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    pass

class ProductUpdate(BaseModel):
    pass

class ProductResponse(ProductCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedProductResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    size: int

class OrderCreate(BaseModel):
    pass

class OrderUpdate(BaseModel):
    pass

class OrderResponse(OrderCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedOrderResponse(BaseModel):
    items: List[OrderResponse]
    total: int
    page: int
    size: int

class ProductOrderCreate(BaseModel):
    product_id: str
    order_id: str

class ProductOrderUpdate(BaseModel):
    product_id: Optional[str] = None
    order_id: Optional[str] = None

class ProductOrderResponse(ProductOrderCreate):
    model_config = ConfigDict(from_attributes=True)

class PaginatedProductOrderResponse(BaseModel):
    items: List[ProductOrderResponse]
    total: int
    page: int
    size: int
