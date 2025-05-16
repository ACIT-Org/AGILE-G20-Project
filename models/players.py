from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from db import db

class Player(db.Model):
    __tablename__ = "players"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    age = mapped_column(Integer)
    gamertag = mapped_column(String)

    team = relationship("Team", back_populates="players")
    team_id = mapped_column(Integer, ForeignKey("teams.id"))