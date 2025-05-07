from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey
from db import db

class Characters(db.Model):
    __tablename__ = "characters"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    role = mapped_column(String)