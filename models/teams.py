from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey, Boolean, Float
from db import db

class Team(db.Model):
    __tablename__ = "teams"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    number_of_wins = mapped_column(Integer)
    number_of_losses = mapped_column(Integer)
    winrate = mapped_column(Float)

    players = relationship("Player",back_populates="team")