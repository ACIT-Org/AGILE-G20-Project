from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey, Boolean
from db import db

class PlayerStats(db.Model):
    __tablename__ = 'PlayerStats'

    pstat_id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))  # Adjust table name if different
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))    # Adjust table name if different
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    damageDealt = db.Column(db.Integer)
    damageBlocked = db.Column(db.Integer)
    healing = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    characterplayed = db.Column(db.Integer)
