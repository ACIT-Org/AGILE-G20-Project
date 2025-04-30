from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey, Boolean
from db import db

class Matches(db.Model):
    __tablename__ = "matches"
    
    id = mapped_column(Integer, primary_key=True)
    completed = mapped_column(Boolean)

    teams = relationship('teamsmatches', back_populates='Matches')