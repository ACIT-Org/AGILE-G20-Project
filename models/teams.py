from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Float, or_, func
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

    players = relationship("Player",back_populates="team")

    def calculate_winrate(self):
        from models import Match
        stmt = db.select(Match).where(
            or_(Match.team1_id == self.id, Match.team2_id == self.id)).where(Match.completed == True)
        result = db.session.execute(stmt)
        matches = result.scalars().all()

        if not matches:
            self.winrate = 0.0
            return

        wins = sum(1 for match in matches if match.winner == self.name)
        self.winrate = round(wins / len(matches), 2)