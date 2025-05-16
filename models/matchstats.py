from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, ForeignKey
from db import db

class PlayerStats(db.Model):
    __tablename__ = 'PlayerStats'

    pstat_id = mapped_column(Integer, primary_key=True, nullable=False)
    player_id = mapped_column(Integer, ForeignKey('players.id'))  # Adjust table name if different
    match_id = mapped_column(Integer, ForeignKey('matches.id'))    # Adjust table name if different
    kills = mapped_column(Integer)
    deaths = mapped_column(Integer)
    assists = mapped_column(Integer)
    damageDealt = mapped_column(Integer)
    damageBlocked = mapped_column(Integer)
    healing = mapped_column(Integer)
    accuracy = mapped_column(Integer)
    characterplayed = mapped_column(String)
