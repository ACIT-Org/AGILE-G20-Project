from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from db import db

class Team(db.Model):
    __tablename__ = "teams"
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    number_of_wins = mapped_column(Integer)
    number_of_losses = mapped_column(Integer)
    winrate = mapped_column(Float)

    as_team1_matches = relationship("Match", foreign_keys="Match.team1_id", back_populates="team1")
    as_team2_matches = relationship("Match", foreign_keys="Match.team2_id", back_populates="team2")
    
    players = relationship("Player", back_populates="team")