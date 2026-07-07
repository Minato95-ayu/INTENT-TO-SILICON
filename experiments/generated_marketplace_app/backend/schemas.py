"""
=============================================================================
FILE: schemas.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

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

class AuditLogCreate(BaseModel):
    timestamp: str
    action: str
    entity_name: str
    entity_id: str
    request_id: str

class AuditLogUpdate(BaseModel):
    timestamp: Optional[str] = None
    action: Optional[str] = None
    entity_name: Optional[str] = None
    entity_id: Optional[str] = None
    request_id: Optional[str] = None

class AuditLogResponse(AuditLogCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedAuditLogResponse(BaseModel):
    items: List[AuditLogResponse]
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
