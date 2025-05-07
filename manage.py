from sqlalchemy import select
from models import Team, Player, Match
from db import db
from app import app
import sys
import csv
from datetime import datetime as dt
from datetime import timedelta
from random import randint 


def create_tables():
    """Create all database tables based on the models."""
    db.create_all()

def drop_tables():
    """Drop all existing database tables."""
    db.drop_all()

# ------------------ Data Import Functions ------------------

def import_players():
    with open("players.csv", "r", encoding="utf-8") as file:
        data = csv.DictReader(file)  # Read each row as a dictionary.

        for line in data:
            # Check if the team already exists
            possible_team = db.session.execute(
                select(Team).where(Team.name == line["team"])).scalar()

            if not possible_team:
                team_obj = Team(name=line["team"])
                db.session.add(team_obj)  # Add new team
            else:
                team_obj = possible_team  # Reuse existing team

            # Create a new player linked to the category
            player = Player(
                name=line["name"],
                age=int(line["age"]),
                gamertag=line["gamertag"],
                team=team_obj
            )
            db.session.add(player) 

        db.session.commit()  

# # ------------------ Random Data Generation ------------------

def random_matches():
    for _ in range(10):  # Create 10 random matches
        # Select a random team
        random_team1 = db.session.execute(
            select(Team).order_by(db.func.random())).scalar()
        
        random_team2 = db.session.execute(
            select(Team).where(Team.name != random_team1.name).order_by(db.func.random())).scalar()

        # teams =[]
        # teams.append(random_team1)
        # teams.append(random_team2)

        randnum = randint(1, 2)
        if randnum == 1:
            winning_team = random_team1.name
        else:
            winning_team = random_team2.name

        # Generate a random match timestamp within the past few days
        created_time = dt.now() - timedelta(
            days=randint(-10, 10),
            hours=randint(0, 15),
            minutes=randint(0, 30)
        )

        #random maps
        maps = ["Central Park", "Hall of Djalia", "Symbiotic Surface", "Shin-Shibuya", "Midtown", "Spider-Islands", "Yggdrasil Path", "Birin T'challa", "Hell's Heaven", "Krakoa", "Royal Palace"]
        random_map_index = randint(0, len(maps)-1)
        # Create the order
        match = Match(
            winner=winning_team,
            play_date =created_time,
            team1 = random_team1,
            team2 = random_team2,
            map = maps[random_map_index]
        )
        db.session.add(match)
        # Create product-order entries for the order
        # for team in teams:
        #     teams_matches = TeamMatch(
        #         teams=team,
        #         matches=match,
        #     )
        #     db.session.add(teams_matches)

    db.session.commit()  # Save all matches

# ------------------ Main Execution Block ------------------

if __name__ == "__main__":
    # Ensure the user provided an action argument
    if len(sys.argv) < 2:
        print("usage: python main.py <action>")
        sys.exit(1)

    choice = sys.argv[1]  # The action: "drop", "create", or "import"
    app.app_context().push()  # Push Flask app context so that 'db' can be accessed outside of server runtime

    if choice == "drop":
        drop_tables()
    elif choice == "create":
        create_tables()
    elif choice == "import":
        drop_tables()
        create_tables()
        import_players()
        random_matches()
