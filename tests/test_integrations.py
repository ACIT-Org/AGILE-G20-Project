#put integration tests in here
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app 
from db import db 
from models import Team, Player, Match

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
    assert response.status_code == 200
    assert b"Marvel Rivals TV" in response.data

def test_matches_view_while_empty(client):
    response = client.get("/matches")
    assert response.status_code == 200
    assert b"Completed Matches" in response.data and b"Matches" in response.data

def test_teams_view_with_one_team(client):
    team = Team(name="Lions")
    db.session.add(team)
    db.session.commit()

    response = client.get("/teams")
    assert response.status_code == 200
    assert b"Lions" in response.data

def test_team_view_specific_person(client):
    teamon = Team(name="wolves")
    player = Player(name="John Doe", team=teamon)
    db.session.add(teamon)
    db.session.add(player)
    db.session.commit()

    response = client.get("/teams/wolves")
    assert response.status_code == 200
    assert b"John Doe" in response.data

def test_players_view_with_one_player(client):
    player = Player(name="Test Player", team_id=None)
    db.session.add(player)
    db.session.commit()

    response = client.get("/players")
    assert response.status_code == 200
    assert b"Test Player" in response.data

def test_match_view_to_view_one_player(client):
    team = Team(name="Sharks")
    db.session.add(team)
    db.session.flush()

    player = Player(name="Jane Smith", team_id=team.id)
    db.session.add(player)

    match1 = Match(team1_id=team.id, team2_id=team.id, completed=False)
    match2 = Match(team1_id=team.id, team2_id=team.id, completed=True)
    db.session.add(match1)
    db.session.add(match2)
    db.session.commit()

    response = client.get(f"/players/{player.id}")
    assert response.status_code == 200
    assert b"Jane Smith" in response.data