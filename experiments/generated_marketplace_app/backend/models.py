from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(String, primary_key=True)


class Order(Base):
    __tablename__ = "order"

    id = Column(String, primary_key=True)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(String, primary_key=True)
    timestamp = Column(String)
    action = Column(String)
    entity_name = Column(String)
    entity_id = Column(String)
    request_id = Column(String)


class ProductOrder(Base):
    __tablename__ = "product_order"

    product_id = Column(String, ForeignKey("product.id"), primary_key=True)
    order_id = Column(String, ForeignKey("order.id"), primary_key=True)

