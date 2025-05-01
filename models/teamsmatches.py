from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from db import db

class TeamMatch(db.Model):
    __tablename__ = "teamsmatches"
    id = mapped_column(Integer, primary_key=True)
    
    teams = relationship('Team')
    teams_id = mapped_column(Integer, ForeignKey("teams.id"))
    
    matches = relationship('Match', back_populates='teams')
    matches_id = mapped_column(Integer, ForeignKey("matches.id"))