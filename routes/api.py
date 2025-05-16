from flask import Blueprint, jsonify, render_template, redirect, url_for, request
from models import Match, Player, Team
from db import db
from werkzeug.exceptions import BadRequest
from datetime import datetime as dt

api_bp = Blueprint("api", __name__)

@api_bp.route("/test")
def example_api():
 return jsonify(["a", {"example": True, "other": "yes"}, ("value", "123")])

@api_bp.route("/createplayer", methods=["POST"])
def create_player_api():
    data = request.json
    fields = ["name", "age", "gamertag"]

    for field in fields:
        if field not in data:
            return jsonify({"message": "Required Fields missing"}), 400
    
    if not isinstance(data["age"], int) or data["age"] <= 0:
        return jsonify({"message": f"{data["age"]} must be positive float"}), 400
    
    if not isinstance(data["name"], str):
        return jsonify({"message": f"{data["name"]} must be a populated string"}), 400
    
    if not isinstance(data["gamertag"], str):
        return jsonify({"message": f"{data["gamertag"]} must be a valid gamertag"}), 400
    

    if "team" in data:
        if not isinstance(data["team"], str):
            return jsonify({"message": f"{data["team"]} must be a populated string."}), 400
        
        #searching for team
        stmt = db.select(Team).where(Team.name == data["team"])
        team_search = db.session.execute(stmt).scalar()
        
        if not team_search:
            return jsonify({"message": f"Team {data["team"]} doesn't exist"})
        else:
            team_obj = team_search
    else:
        team_obj=None

    stmt = db.select(Player).where(Player.gamertag == data["gamertag"])
    player_search = db.session.execute(stmt).scalar()
        
    if player_search:
        return jsonify({"message": f"{data["gamertag"]} already exists"}), 400
    


    player = Player(name=data["name"],gamertag=data["gamertag"], age=int(data["age"]), team=team_obj)
    db.session.add(player)

    db.session.commit()
    return jsonify(player.to_json()), 200


    