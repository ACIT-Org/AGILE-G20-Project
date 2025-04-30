from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey
from db import db

from sqlalchemy import String, DECIMAL, Integer
from sqlalchemy.orm import mapped_column
import operator

class Order(db.Model):
    __tablename__ = "orders"
    
    id = mapped_column(Integer, primary_key=True)

    
    customer = relationship("Customer", back_populates='orders')
    customer_id = mapped_column(Integer, ForeignKey("customer.id"))
    
    products = relationship('ProductOrder', back_populates='order')

    def to_json(self):
        
        dictionary = {
            
        } 
        return dictionary
