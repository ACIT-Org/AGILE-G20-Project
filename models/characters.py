from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from db import db

class Characters(db.Model):
    __tablename__ = "characters"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    role = mapped_column(String)