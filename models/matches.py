from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey, Boolean
from db import db

class Match(db.Model):
    __tablename__ = "matches"
    
    id = mapped_column(Integer, primary_key=True)
    winner = mapped_column(String)
    time = mapped_column(String)
    
    team1_id = mapped_column(Integer, ForeignKey("teams.id"))
    team2_id = mapped_column(Integer, ForeignKey("teams.id"))
    #need the foreign_keys attribute since we're referencing the same table twice
    team1 = relationship("Team", foreign_keys=[team1_id], back_populates="as_team1_matches")
    team2 = relationship("Team", foreign_keys=[team2_id], back_populates="as_team2_matches")