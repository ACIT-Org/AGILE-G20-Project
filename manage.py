from sqlalchemy import select
from models import Team, Player, Match, PlayerStats, Maps, Characters, MatchVOD
from db import db
from app import app
import sys
import csv
from datetime import datetime as dt
from datetime import timedelta
from random import randint 
import datetime
from pathlib import Path
import re

def create_tables():
    """Create all database tables based on the models."""
    db.create_all()

def drop_tables():
    """Drop all existing database tables."""
    db.drop_all()

# ------------------ Data Import Functions ------------------

def import_players():
    with open("data/players.csv", "r", encoding="utf-8") as file:
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

def import_maps():
    with open("data/maps.csv", "r", encoding="utf-8") as file:
        data = csv.DictReader(file)  # Read each row as a dictionary.

        for line in data:
            map = Maps(
                name=line["name"]
            )
            db.session.add(map) 

        db.session.commit()  

def import_characters():
    with open("data/characters.csv", "r", encoding="utf-8") as file:
        data = csv.DictReader(file)  # Read each row as a dictionary.

        for line in data:
            character = Characters(
                name=line["name"],
                role=line["role"]
            )
            db.session.add(character) 

        db.session.commit()  

def import_matches(filefirst,filelast):

    folder_path=Path("data/games/")

    if folder_path.exists() and folder_path.is_dir():
        files=[]
        for item in folder_path.iterdir():
            if item.is_file():
                files.append(item.name)
    
    pattern = r'^game\d+\.csv$'

    for file in files:
        if re.fullmatch(pattern,file):
            pass
        else:
            raise Exception("File in foler does not match pattern of game_.csv")

    filefirst = int(filefirst)
    filelast = int(filelast)
    for num in range(filefirst,filelast+1):

        fileToOpen="data/games/game"
        fileToOpen+=str(num)
        fileToOpen+=".csv"

        cleaned_data = []
        with open(fileToOpen, "r", encoding="utf-8") as file:
            data = csv.DictReader(file) 

            for line in data:
                cleaned_line = {}

                for key, value in line.items():
                    # Skip empty keys
                    if not key:
                        continue

                    # Clean key and value
                    clean_key = key.strip()
                    if value is not None:
                        clean_value = value.strip() 
                    else: 
                        clean_value = ""

                    cleaned_line[clean_key] = clean_value

                cleaned_data.append(cleaned_line)

            teams =[]

            for line in cleaned_data:
                time=line['timePlayed']
                winner=line["winningTeam"]
                map=line["map"]
                break

            for line in cleaned_data:
                if line["team"] in teams:
                    pass
                else:
                    teams.append(line["team"])
                    
            teams=list(set(teams))
            team1=teams[0]
            team1=db.session.execute(select(Team).where(Team.name == team1)).scalar()
            team2=teams[1]
            team2=db.session.execute(select(Team).where(Team.name == team2)).scalar()

            play_date = datetime.datetime.strptime(time, "%b %d %Y %I%M %p")

            match = Match(
                winner=winner,
                play_date =play_date,
                team1 = team1,
                team2 = team2,
                map = map
            )

            db.session.add(match)

            for line in cleaned_data:
                player = db.session.execute(select(Player).where(Player.gamertag == line["player"])).scalar()
                playerstat =PlayerStats(
                    player_id = player.id,
                    match_id = match.id,
                    kills=line["kills"],
                    deaths=line["deaths"],
                    assists = line["assists"],
                    damageDealt = line["damageDealt"],
                    damageBlocked = line["damageBlocked"],
                    healing = line["healingDone"],
                    accuracy = line["accuracy"],
                    characterplayed = line["characterPlayed"]
                )

                db.session.add(playerstat)

    db.session.commit()
        
# # ------------------ Random Data Generation ------------------

# def random_matches():
#     for _ in range(30):  # Create 10 random matches
#         # Select a random team
#         random_team1 = db.session.execute(
#             select(Team).order_by(db.func.random())).scalar()
        
#         random_team2 = db.session.execute(
#             select(Team).where(Team.name != random_team1.name).order_by(db.func.random())).scalar()

#         # Generate a random match timestamp within the past few days
#         created_time = dt.now() - timedelta(
#             days=randint(-10, 10),
#             hours=randint(0, 15),
#             minutes=randint(0, 30)
#         )

#         #random maps
#         random_map = db.session.execute(
#             select(Maps).order_by(db.func.random())).scalar()
#         # Create the order
#         match = Match(
#             # winner=winning_team,
#             play_date =created_time,
#             team1 = random_team1,
#             team2 = random_team2,
#             map = random_map.name
#         )
#         db.session.add(match)
        
#         # random_match_player_stats(match)

#     db.session.commit()  # Save all matches


def random_videos():
    vodlist = []
    with open("data/videos.csv", "r", encoding="utf-8") as file:
        vods = csv.reader(file)
        for vod in vods:
            for v in vod:
                vodlist.append(v)

    for y in range(30):  # Assign 30 random videos
        x = randint(0,len(vodlist)-1)
        vods = MatchVOD(
            match_id = y,
            link = vodlist[x] )
        db.session.add(vods)
    db.session.commit()  # Save all matches

# def check_if_match_is_complete():
#     matches = db.select(Match).where(Match.completed == False)
#     results = db.session.execute(matches).scalars().all()

#     for match in results:
#         match.completed_check()
#     db.session.commit()

# ------------------ Main Execution Block ------------------

if __name__ == "__main__":
    # Ensure the user provided an action argument
    if len(sys.argv) < 2:
        print("usage: python main.py <action>")
        sys.exit(1)

    choice = sys.argv[1]  # The action: "drop", "create", or "import"
    app.app_context().push()  # Push Flask app context so that 'db' can be accessed outside of server runtime

    filefirst = sys.argv[2]
    if len(sys.argv) < 4:
        filefirst = 1
        filelast = sys.argv[2]
    else:
        filelast = sys.argv[3]

    if choice == "drop":
        drop_tables()
    elif choice == "create":
        create_tables()
    elif choice == "import":
        drop_tables()
        create_tables()
        import_players()
        import_maps()
        import_characters()
        import_matches(filefirst,filelast)
        random_videos()
        # check_if_match_is_complete()
        
