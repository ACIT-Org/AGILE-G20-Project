from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey
from db import db

from sqlalchemy import String, DECIMAL, Integer
from sqlalchemy.orm import mapped_column
import operator

class Customer(db.Model):
    __tablename__ = "customer"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)

    orders = relationship("Order", back_populates="customer")

    def to_json(self):
        
        return {

        }   