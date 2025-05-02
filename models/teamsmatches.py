# from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
# from sqlalchemy import DECIMAL, Integer, String, ForeignKey
# from db import db

# class TeamMatch(db.Model):
#     __tablename__ = "team_matches"
#     id = mapped_column(Integer, primary_key=True)
#     team_id = mapped_column(Integer, ForeignKey("teams.id"))
#     matches_id = mapped_column(Integer, ForeignKey("matches.id"))

#     team = relationship("Team", back_populates="team_matches")
#     match = relationship('Match', back_populates='team_matches')
    