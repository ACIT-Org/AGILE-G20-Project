from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey
from db import db

from sqlalchemy import String, DECIMAL, Integer
from sqlalchemy.orm import mapped_column
import operator

class ProductOrder(db.Model):
    __tablename__ = "product_orders"
    id = mapped_column(Integer, primary_key=True)
    
    product = relationship('Product')
    product_id = mapped_column(Integer, ForeignKey("products.id"))
    
    order = relationship('Order', back_populates='products')
    order_id = mapped_column(Integer, ForeignKey("orders.id"))

    quantity = mapped_column(Integer, nullable=False)