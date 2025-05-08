import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from models import Match, Team 


@pytest.fixture
def test_teams():
    team1 = Team(name="Alpha")
    team2 = Team(name="Beta")
    return team1, team2


def test_match_creation(test_teams):
    match = Match(
        team1=test_teams[0],
        team2=test_teams[1],
        play_date=datetime.now(),
        map="Dust II"
    )

    assert match.team1.name == "Alpha"
    assert match.team2.name == "Beta"
    assert not match.completed
    assert match.map == "Dust II"


@patch("random.randint", return_value=1)
def test_complete_match_team1_wins(mock_randint, test_teams):
    match = Match(team1=test_teams[0], team2=test_teams[1])
    match.complete_match()

    assert match.completed is True
    assert match.winner == "Alpha"  # Because randint = 1, team1 wins


@patch("random.randint", return_value=2)
def test_complete_match_team2_wins(mock_randint, test_teams):
    match = Match(team1=test_teams[0], team2=test_teams[1])
    match.complete_match()

    assert match.completed is True
    assert match.winner == "Beta"  # Because randint = 2, team2 wins