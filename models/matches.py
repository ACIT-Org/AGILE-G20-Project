from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String
from db import db

class Match(db.Model):
    __tablename__ = "matches"
    
    id = mapped_column(Integer, primary_key=True)
    winner = mapped_column(String)
    time = mapped_column(String)
    

    teams = relationship('TeamMatch', back_populates='matches')