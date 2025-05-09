from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import DECIMAL, Integer, String, ForeignKey, Boolean
from db import db

class MatchVOD(db.Model):
    __tablename__ = "vods"
    id = mapped_column(Integer, primary_key=True)
    match_id = mapped_column(Integer, ForeignKey('matches.id'))
    link = mapped_column(String)