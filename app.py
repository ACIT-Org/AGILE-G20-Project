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

db.init_app(app)

app.register_blueprint(api_bp, url_prefix="/api")


# Run on port 8888 (localhost:8888)
if __name__ == "__main__":
 app.run(debug=True, port=8888)



