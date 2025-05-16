from sqlalchemy import select
from models import Team, Player, Match, PlayerStats, Maps, Characters, MatchVOD, Admins
from db import db
from app import app
import sys
import csv
from random import randint 
import datetime
from pathlib import Path
import re
from werkzeug.security import generate_password_hash


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


def import_matches(filefirst, filelast):
    folder_path = Path("data/games/")
    
    if not folder_path.exists() or not folder_path.is_dir():
        raise ValueError(f"Directory not found: {folder_path}")
    
    pattern = r'^game\d+\.csv$' 
    valid_files = []
    
    for item in folder_path.iterdir():
        if item.is_file():
            if re.fullmatch(pattern, item.name):
                valid_files.append(item)
            else:
                raise ValueError(f"File '{item.name}' does not match required pattern 'game<number>.csv'")
    
    if not valid_files:
        raise ValueError("No valid game files found in directory")

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
            now = datetime.datetime.now()
            completed = False
            if now > play_date:
                completed = True

            match = Match(
                winner=winner,
                play_date =play_date,
                team1 = team1,
                team2 = team2,
                map = map,
                completed=completed
            )

            db.session.add(match)

            for line in cleaned_data:
                if completed:
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

def create_admin():
    admin = Admins(
        username="admin",
        password=generate_password_hash("password123", method='pbkdf2:sha256')
    )
    db.session.add(admin)
    db.session.commit()
        
# ------------------ Random Data Generation ------------------

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
        create_admin()
        
