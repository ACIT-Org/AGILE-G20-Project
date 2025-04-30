from sqlalchemy import select
from models import Team, TeamMatch, Player, Match
from db import db
from app import app
import sys
import csv
import random
from datetime import datetime as dt
from datetime import timedelta

# This file was used to read data from a CSV which we can use to put a bunch of data into our database after we create our tables
# IGNORE THIS FILE FOR NOW

def create_tables():
    """Create all database tables based on the models."""
    db.create_all()

def drop_tables():
    """Drop all existing database tables."""
    db.drop_all()

# ------------------ Data Import Functions ------------------

def import_players():
    with open("players.csv", "r", encoding="utf-8") as file:
        data = csv.DictReader(file)  # Read each row as a dictionary.

        for line in data:
            # Check if the team already exists
            possible_team = db.session.execute(
                select(Team).where(Team.name == line["team"])).scalar()

            if not possible_team:
                team_obj = Team(name=line["team"])
                db.session.add(team_obj)  # Add new team
            else:
                category_obj = possible_team  # Reuse existing team

            # Create a new player linked to the category
            player = Player(
                name=line["name"],
                age=int(line["age"]),
                gamertag=line["gamertag"],
                team=team_obj
            )
            db.session.add(player)  # Add product to the session

        db.session.commit()  # Save all new categories and products

# def import_matches():
#     """Import customers from 'customers.csv' into the database."""
#     with open("matches.csv", "r", encoding="utf-8") as file:
#         data = csv.DictReader(file)

#         for line in data:
#             customer = Customer(
#                 name=line["name"],
#                 phone=line["phone"]
#             )
#             db.session.add(customer)  # Add each customer

#         db.session.commit()  # Save all new customers

# # ------------------ Random Data Generation ------------------

# def random_orders():
#     """Generate random orders for testing purposes."""
#     for _ in range(10):  # Create 10 random orders
#         # Select a random customer
#         random_customer = db.session.execute(
#             select(Customer).order_by(func.random())
#         ).scalar()

#         # Select a random number of products (4–6)
#         num_prods = randint(4, 6)
#         random_prods = db.session.execute(
#             select(Product).order_by(func.random()).limit(num_prods)
#         ).scalars()

#         # Generate a random creation timestamp within the past few days
#         created_time = dt.now() - timedelta(
#             days=randint(1, 3),
#             hours=randint(0, 15),
#             minutes=randint(0, 30)
#         )

#         # Create the order
#         order = Order(
#             customer=random_customer,
#             created=created_time
#         )

#         # Create product-order entries for the order
#         for prod in random_prods:
#             product_order = ProductOrder(
#                 order=order,
#                 product=prod,
#                 quantity=randint(4, 7)  # Random quantity per product
#             )
#             db.session.add(product_order)

#     db.session.commit()  # Save all new orders and items

# ------------------ Main Execution Block ------------------

if __name__ == "__main__":
    # Ensure the user provided an action argument
    if len(sys.argv) < 2:
        print("usage: python main.py <action>")
        sys.exit(1)

    choice = sys.argv[1]  # The action: "drop", "create", or "import"
    app.app_context().push()  # Push Flask app context so that 'db' can be accessed outside of server runtime

    if choice == "drop":
        drop_tables()
    elif choice == "create":
        create_tables()
    elif choice == "import":
        drop_tables()
        create_tables()
        import_players()
        # import_customers()
        # random_orders()
