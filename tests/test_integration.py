import pytest
from unittest.mock import patch, mock_open
from app import app
from db import db
from models import Team, Player, Maps, Characters, Match, PlayerStats
from datetime import datetime, timedelta, timezone
import csv
from manage import import_players, import_maps, import_characters, import_matches
from pathlib import Path
import re


@pytest.fixture()
def setup_database():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

@pytest.fixture()
def client(setup_database):
    yield app.test_client() 


def test_homepage(client):
    response = client.get("/")
    #ensure correct response code and data is shown
    assert response.status_code == 200
    assert b"Marvel Rivals TV" in response.data

def test_matches_view_while_empty(client):
    response = client.get("/matches")
    #ensure correct response code and data is shown
    assert response.status_code == 200
    assert b"Completed Matches" in response.data and b"Matches" in response.data

def test_teams_view_with_one_team(client):
    #create team and addd to db
    team = Team(name="Lions")
    db.session.add(team)
    db.session.commit()

    response = client.get("/teams")
    #ensure correct response code and data is shown
    assert response.status_code == 200
    assert b"Lions" in response.data

def test_team_view_specific_person(client):
    #create team and player and add to db
    teamon = Team(name="wolves")
    player = Player(name="John Doe", team=teamon)
    db.session.add(teamon)
    db.session.add(player)
    db.session.commit()

    response = client.get("/teams/wolves")
    #ensure correct response code and data is shown
    assert response.status_code == 200
    assert b"John Doe" in response.data

def test_players_view_with_one_player(client):
    #create player and add to db
    player = Player(name="Test Player", team_id=None)
    db.session.add(player)
    db.session.commit()

    response = client.get("/players")
    #ensure correct response code and data is shown
    assert response.status_code == 200
    assert b"Test Player" in response.data

def test_match_view_to_view_one_player(client):
    #create a team and add it to the db
    team1 = Team(name="Sharks")
    db.session.add(team1)

    team2 = Team(name="Sharks")
    db.session.add(team2)

    #create a player and add them to the team
    player1 = Player(name="Jane Smith", team_id=team1.id,)
    db.session.add(player1)

    player2 = Player(name="John Smith", team_id=team2.id,)
    db.session.add(player2)

    #create two matches one completed and one not completed
    match1 = Match(team1_id=team1.id, team2_id=team2.id, completed=False)
    match2 = Match(team1_id=team2.id, team2_id=team1.id, completed=True)
    db.session.add(match1)
    db.session.add(match2)
    db.session.commit()

    response = client.get(f"/players/{player1.id}")
    #ensure correct response code and data is shown
    assert response.status_code == 200
    assert b"Jane Smith" in response.data

def test_import_players(setup_database):
    #create mock data
    fake_data="name,age,gamertag,team\nAlice,22,Alicorn,TeamA\n"
    mocked_open = mock_open(read_data=fake_data)

    #patch the mock data into the function
    with patch("builtins.open",mocked_open):
        import_players()

    player = db.session.query(Player).first()
    team = db.session.query(Team).first()
    #ensure data is loaded into the database correctly 
    assert player is not None
    assert team.name == "TeamA"
    assert player.team_id == team.id

def test_import_maps(setup_database):
    #create mock data
    fake_data="name\nArena1"
    mocked_open = mock_open(read_data=fake_data)

    #patch the mock data into the function
    with patch("builtins.open",mocked_open):
        import_maps()

    map = db.session.query(Maps).first()
    #ensure data is loaded into the database correctly 
    assert map is not None
    assert map.name == "Arena1"

def test_import_characters(setup_database):
    #create mock data
    fake_data="name,role\nWarrior,Tank"
    mocked_open = mock_open(read_data=fake_data)

    #patch the mock data into the function
    with patch("builtins.open",mocked_open):
        import_characters()

    character = db.session.query(Characters).first()
    #ensure data is loaded into the database correctly 
    assert character is not None
    assert character.role == "Tank"

@pytest.fixture
def match_csv():
    return (
        "player,team,kills,deaths,assists,damageDealt,damageBlocked,healingDone,accuracy,characterPlayed,winningTeam,timePlayed,map\n"
        "RogueNova,Team Liquid,45,5,42,15729,6987,26680,55%,Groot,Team Liquid,May 12 2025 0846 PM,Krakoa\n"
        "NightBloom,G2,33,17,48,23139,26613,16745,100%,Thor\n"
    )

def test_import_matches_success(setup_database, match_csv):
    with app.app_context():
        team1 = Team(name="Team Liquid")
        team2 = Team(name="G2")
        db.session.add(team1)
        db.session.add(team2)
        db.session.commit()

        player1 = Player(gamertag="RogueNova", team_id=team1.id)
        player2 = Player(gamertag="NightBloom", team_id=team2.id)
        db.session.add(player1)
        db.session.add(player2)
        db.session.commit()

    with patch("builtins.open", mock_open(read_data=match_csv)):
        with patch("manage.Path.iterdir", return_value=[Path("data/games/game1.csv")]):
            import_matches(1, 1)

            with app.app_context():
                matches = Match.query.all()
                stats = PlayerStats.query.all()

                assert len(matches) == 1
                assert matches[0].winner == "Team Liquid"
                assert matches[0].map == "Krakoa"
                assert len(stats) == 2
                assert stats[0].kills == 45
                assert stats[1].characterplayed == "Thor"

@pytest.mark.usefixtures("setup_database")
def test_import_matches_invalid_filename_raises_exception():
    with app.app_context():
        bad_filename = "badfile.csv"
        with patch("manage.Path.iterdir", return_value=[Path(bad_filename)]):
            with patch("builtins.open"):
                with pytest.raises(ValueError) as excinfo:  
                    import_matches(1, 1)
                
                assert "No valid game files found" in str(excinfo.value)

#Josh tests
def test_admin_redirects_if_not_logged_in(client): 
    response = client.get('/admin', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_admin_view_if_logged_in(client):
    with client.session_transaction() as sess:
        sess['admin_id'] = 1  

    response = client.get('/admin')
    assert response.status_code == 200
   
def test_calculate_winrate(setup_database):
    team = Team(id=1, name="G2")
    db.session.add(team)

    matches = [
        Match(team1_id=1, team2_id=2, completed=True, winner="G2"),
        Match(team1_id=3, team2_id=1, completed=True, winner="Team Liquid"),
        Match(team1_id=1, team2_id=4, completed=True, winner="G2"),
    ]
    db.session.add_all(matches)
    db.session.commit()

    team.calculate_winrate()
    assert team.winrate == 0.67

def test_calculate_winrate_no_matches(setup_database):
    team = Team(id=2, name="Team Liquid")
    db.session.add(team)
    db.session.commit()

    team.calculate_winrate()
    assert team.winrate == 0.0