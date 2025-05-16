from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from db import db

class Admins(db.Model):
    __tablename__ = "admins"
    
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)