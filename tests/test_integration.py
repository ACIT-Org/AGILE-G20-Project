import pytest
from app import app  # Absolute import
from db import db
from models.teams import Team
from models.players import Player
from models.matches import Match
from datetime import datetime, timedelta



@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_match_completion_logic(test_client):
    # Create teams
    team1 = Team(name="Alpha")
    team2 = Team(name="Beta")
    db.session.add_all([team1, team2])
    db.session.commit()

    # Create a match in the past
    match = Match(
        map="Dust II",
        play_date=datetime.utcnow() - timedelta(hours=2),
        team1_id=team1.id,
        team2_id=team2.id
    )
    db.session.add(match)
    db.session.commit()

    # Run your method to mark matches completed
    match.completed_check()

    # Assert the match is completed and has a winner
    assert match.completed is True
    assert match.winner is not None  # Ensure a winner name is assigned
    assert match.winner in [team1.name, team2.name]  # The winner should be one of the team's names

def test_match_not_completed(test_client):
    # Create teams
    team1 = Team(name="Alpha")
    team2 = Team(name="Beta")
    db.session.add_all([team1, team2])
    db.session.commit()

    # Create a match in the past
    match = Match(
        map="Dust II",
        play_date=datetime.utcnow() + timedelta(hours=10),
        team1_id=team1.id,
        team2_id=team2.id
    )
    db.session.add(match)
    db.session.commit()


    match.completed_check()

    # Assert the match is not completed and has no winner
    assert match.completed != True
    assert match.winner == None  
