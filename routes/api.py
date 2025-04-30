from flask import Blueprint, jsonify, render_template, redirect, url_for, request
from models import Match, TeamMatch, Player, Team
from db import db
from werkzeug.exceptions import BadRequest
from datetime import datetime as dt

api_bp = Blueprint("api", __name__)

@api_bp.route("/test")
def example_api():
 return jsonify(["a", {"example": True, "other": "yes"}, ("value", "123")])


    