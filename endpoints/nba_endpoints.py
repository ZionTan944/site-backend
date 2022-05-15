from flask import request

from index import app
from database.db_setup import create_connection
from services.nba_services import get_all_nba_teams
from clients.nba_schedule_client import NbaScheduling

conn = create_connection()


@app.route("/test_nba", methods=["POST"])
def test_nba():
    if request.method == "POST":
        data, class_data = get_all_nba_teams(conn)
        league = NbaScheduling(class_data)
        league.start_league()

    return {"result": data}
