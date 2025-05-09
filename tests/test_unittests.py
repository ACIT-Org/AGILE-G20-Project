import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from models import Match, Team 


@pytest.fixture
def test_team1():
    #create a mock team
    team = Team(name="Alpha")
    return team

@pytest.fixture
def test_team2():
    #create another mock team 
    team = Team(name="Beta")
    return team

def test_match_creation(test_team1,test_team2):
    #create a match
    match = Match(
        team1=test_team1,
        team2=test_team2,
        play_date=datetime.now(),
        map="Dust II"
    )

    #ensure the teams are right match isnt completed and the correct map is present
    assert match.team1.name == "Alpha"
    assert match.team2.name == "Beta"
    assert match.map == "Dust II"
    assert not match.completed


#test team one wins 
@patch("random.randint", return_value=1)
def test_complete_match_team1_wins(mock_randint, test_team1, test_team2):
    #create a mock match with the two teams and complete the match
    match = Match(team1=test_team1, team2=test_team2)
    match.complete_match()
    
    assert mock_randint.called
    assert match.completed is True
    assert match.winner == "Alpha"  # Because randint = 1, team1 wins


#test team two wins
@patch("random.randint", return_value=2)
def test_complete_match_team2_wins(mock_randint, test_team1,test_team2):
    #create a mock match with the two teams and complete the match
    match = Match(team1=test_team1, team2=test_team2)
    match.complete_match()

    assert mock_randint.called
    assert match.completed is True
    assert match.winner == "Beta"  # Because randint = 2, team2 wins