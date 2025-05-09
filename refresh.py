import time
from datetime import datetime as dt, timedelta
from db import db
from app import app
from models.matches import Match


def check_all_matches():
    with app.app_context():  # needed if you're outside request context
        stmt = db.select(Match).where(Match.completed == False)
        results = db.session.execute(stmt).scalars().all()

        print("Match checking being refreshed...")
        print(len(results))
        for i, match in enumerate(results):
            print(i)
            match.completed_check()
        db.session.commit()


if __name__ == "__main__":
    while True:
        check_all_matches()
        time.sleep(10)