from flask import Flask, render_template, redirect, url_for, request
from pathlib import Path
from models import Match, Player, Team
from db import db
from routes.api import api_bp
from sqlalchemy import desc
from datetime import datetime as dt
from datetime import timedelta

app = Flask(__name__)

# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///i_copy_pasted_this.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()

@app.route("/")
def home():
 return render_template("home.html", my_list=["Tim", "Bob", "Alice"])

@app.route("/matches")
def product_view():
    statement = db.select(Match).order_by(Match.id)
    results = db.session.execute(statement).scalars()
    return render_template("products.html", products=results)

@app.route("/teams")
def product_view():
    statement = db.select(Match).order_by(Match.id)
    results = db.session.execute(statement).scalars()
    return render_template("products.html", products=results)

@app.route(("/teams/<string:name>"))
def category_detail(name):
    stmt1 = db.select(Team).where(Team.name == name)
    found_team = db.session.execute(stmt1).scalar()

    stmt2 = db.select(Player).where(Player.team_id == found_team.id)
    team_players = db.session.execute(stmt2).scalars()
    return render_template("categorysort.html", category=team_players, name=name.capitalize())

db.init_app(app)

app.register_blueprint(api_bp, url_prefix="/api")


# Run on port 8888 (localhost:8888)
if __name__ == "__main__":
 app.run(debug=True, port=8888)



