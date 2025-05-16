from flask import Flask, render_template, redirect, url_for, request, session
from pathlib import Path
from models import Match, Player, Team, PlayerStats, MatchVOD, Admins
from db import db
from routes.api import api_bp
from sqlalchemy import desc, or_
from datetime import datetime as dt
from datetime import timedelta
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "sfkjshgdkjhdsagkjhaiueshoighdsaiughiudsagiudsahiuv"

# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()
db.init_app(app)

@app.route("/")
def home():
    statement = db.select(Match).where(Match.completed == False).order_by(Match.play_date)
    results = db.session.execute(statement).scalars()

    statement = db.select(Match).where(Match.completed == True).order_by(Match.play_date.desc())
    results2 = db.session.execute(statement).scalars()
    return render_template("home.html", upcoming_matches=results, completed_matches=results2)

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
    return render_template("match_details.html",matches=match,teams=Team.query.all(),players=Player.query.all(),PlayerStats=PlayerStats.query.all(),vod=MatchVOD.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admins = db.session.execute(db.select(Admins).where(Admins.username == username)).scalar()

        if admins and check_password_hash(admins.password, password):
            session['admin_id'] = admins.id
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('home'))

@app.route("/admin")
def admin():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    statement = db.select(Player).order_by(Player.id)
    results = db.session.execute(statement).scalars()
    return render_template("admin.html", players=results)

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    age = request.form['age']
    gamertag = request.form['gamertag']
    team_name = request.form['team']

    team = Team.query.filter_by(name=team_name).first()
    if not team:
        team = Team(name=team_name)
        db.session.add(team)
        db.session.commit()

    new_player = Player(name=name, age=age, gamertag=gamertag, team_id=team.id)
    db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('admin_view'))

@app.route('/update', methods=['POST'])
def update():
    player_id = request.form['id']
    player = Player.query.get(player_id)
    if player:
        player.name = request.form['name']
        player.age = request.form['age']
        player.gamertag = request.form['gamertag']
        team_name = request.form['team']

        team = Team.query.filter_by(name=team_name).first()
        if not team:
            team = Team(name=team_name)
            db.session.add(team)

        player.team = team
        db.session.commit()

    return redirect(url_for('admin_view'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('admin_view'))

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
       winrate = found_team.winrate,
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



