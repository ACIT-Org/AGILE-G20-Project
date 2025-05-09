from flask import Flask, render_template, redirect, url_for, request
from pathlib import Path
from models import Match, Player, Team, PlayerStats
from db import db
from routes.api import api_bp
from sqlalchemy import desc, or_
from datetime import datetime as dt
from datetime import timedelta

app = Flask(__name__)

# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()
db.init_app(app)

@app.route("/")
def home():
 return render_template("home.html", my_list=["Tim", "Bob", "Alice"])

@app.route("/matches")
def matches_view():
    statement = db.select(Match).where(Match.completed == False).order_by(Match.play_date)
    results = db.session.execute(statement).scalars()

    statement = db.select(Match).where(Match.completed == True).order_by(Match.play_date.desc())
    results2 = db.session.execute(statement).scalars()
    return render_template("matches.html", upcoming_matches=results, completed_matches=results2)

@app.route("/matches/<int:id>")
def matches_details(id):
    statement = db.select(Match).where(Match.id == id)
    match = db.session.execute(statement).scalar()
    return render_template("match_details.html",matches=match,teams=Team.query.all(),players=Player.query.all(),PlayerStats=PlayerStats.query.all())


@app.route("/teams")
def teams_view():
    statement = db.select(Team).order_by(Team.id)
    results = db.session.execute(statement).scalars()
    return render_template("teams.html", teams=results)

@app.route(("/teams/<string:name>"))
def team_name(name):
    stmt1 = db.select(Team).where(Team.name == name)
    found_team = db.session.execute(stmt1).scalar()

    stmt2 = db.select(Player).where(Player.team_id == found_team.id)
    team_players = db.session.execute(stmt2).scalars()

    upcoming_stmt = (
    db.select(Match).where(Match.completed == False)
    .join(Team, or_(Match.team1_id == Team.id, Match.team2_id == Team.id))
    # .join(Player, Player.team_id == Team.id)
    .where(Team.name == name).order_by(Match.play_date)
)
    upcoming = db.session.execute(upcoming_stmt).scalars()

    completed_stmt = (
    db.select(Match).where(Match.completed == True)
    .join(Team, or_(Match.team1_id == Team.id, Match.team2_id == Team.id))
    # .join(Player, Player.team_id == Team.id)
    .where(Team.name == name).order_by(Match.play_date.desc())
)
    completed = db.session.execute(completed_stmt).scalars()
    
    return render_template(
       "team_details.html", 
       team=team_players, 
       name = ' '.join([word.capitalize() for word in name.split()]),
       upcoming_matches = upcoming, 
       completed_matches = completed
       )

@app.route("/players")
def players_view():
    statement = db.select(Player).order_by(Player.id)
    results = db.session.execute(statement).scalars()
    return render_template("players.html", players=results)

@app.route(("/players/<int:id>"))
def player_id(id):
    statement = db.select(Player).where(Player.id == id)
    player = db.session.execute(statement).scalar()

    upcoming_stmt = (
    db.select(Match).where(Match.completed == False)
    .join(Team, or_(Match.team1_id == Team.id, Match.team2_id == Team.id))
    .join(Player, Player.team_id == Team.id)
    .where(Player.id == id)
    .order_by(Match.play_date)
)
    upcoming = db.session.execute(upcoming_stmt).scalars()

    completed_stmt = (
    db.select(Match).where(Match.completed == True)
    .join(Team, or_(Match.team1_id == Team.id, Match.team2_id == Team.id))
    .join(Player, Player.team_id == Team.id)
    .where(Player.id == id)
    .order_by(Match.play_date.desc())
)
    completed = db.session.execute(completed_stmt).scalars()
    return render_template("playerid.html", player=player, upcoming_matches = upcoming, completed_matches = completed)

app.register_blueprint(api_bp, url_prefix="/api")


# Run on port 8888 (localhost:8888)
if __name__ == "__main__":
 app.run(debug=True, port=8888)



