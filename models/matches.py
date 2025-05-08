from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean
from db import db
from datetime import datetime as dt
from datetime import timedelta



class Match(db.Model):
    __tablename__ = "matches"
    
    id = mapped_column(Integer, primary_key=True)
    winner = mapped_column(String)
    play_date = mapped_column(db.DateTime, nullable=False, default=db.func.now())
    map = mapped_column(String)
    completed = mapped_column(Boolean, default=False)
    
    team1_id = mapped_column(Integer, ForeignKey("teams.id"))
    team2_id = mapped_column(Integer, ForeignKey("teams.id"))
    #need the foreign_keys attribute since we're referencing the same table twice
    team1 = relationship("Team", foreign_keys=[team1_id], back_populates="as_team1_matches")
    team2 = relationship("Team", foreign_keys=[team2_id], back_populates="as_team2_matches")

    def completed_check(self):
        if not self.completed:
            # check if match time had passed
            if self.play_date < dt.utcnow() - timedelta(hours=0):
                self.completed = True
                db.session.commit()