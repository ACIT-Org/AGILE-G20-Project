from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from db import db

class Maps(db.Model):
    __tablename__ = "maps"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)