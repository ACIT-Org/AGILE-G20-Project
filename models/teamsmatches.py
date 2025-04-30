from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey
from db import db

class TeamsMatches(db.Model):
    __tablename__ = "teams_matches"
    id = mapped_column(Integer, primary_key=True)
    
    teams = relationship('Teams')
    teams_id = mapped_column(Integer, ForeignKey("teams.id"))
    
    matches = relationship('Matches', back_populates='teams.id')
    matches_id = mapped_column(Integer, ForeignKey("matches.id"))