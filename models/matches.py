from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean, select
from db import db
from datetime import datetime as dt
from datetime import timedelta
import random
from models.matchstats import PlayerStats
from models.characters import Characters


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
    
    def complete_match(self):
        randnum = random.randint(1, 2)
        if randnum == 1:
            winning_team = self.team1
        else:
            winning_team = self.team2

        self.winner = winning_team.name
        self.random_match_player_stats()
        self.completed = True

    def completed_check(self):
        if not self.completed:
            # check if match time had passed
            if self.play_date < dt.now() - timedelta(hours=0):
                self.complete_match()
                db.session.commit()
    
    def random_match_player_stats(self):
        random_team1 = self.team1
        random_team2 = self.team2
        
        for player in random_team1.players + random_team2.players:
            random_character = db.session.execute(select(Characters).order_by(db.func.random())).scalar()
            playerstat = PlayerStats(
                player_id=player.id,
                match_id=self.id, 
                kills = random.randint(0 , 50),
                deaths = random.randint(0 , 50),
                assists = random.randint(0 , 50),
                damageDealt = random.randint(0 , 50000),
                damageBlocked = random.randint(0 , 30000),
                healing = random.randint(0 , 40000),
                accuracy = random.randint(0 , 100),
                characterplayed = random_character.name
            )
            db.session.add(playerstat)