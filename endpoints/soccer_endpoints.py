from flask import request

from index import app
from database.db_setup import create_connection
from services.soccer_services import get_all_leagues, set_up_soccer_teams
from clients.soccer_league_client import SoccerLeagueClient

conn = create_connection()
league_name, teams_lst = set_up_soccer_teams(conn, 1)
soccer_league = SoccerLeagueClient(league_name, teams_lst)
soccer_league.prepare_season()


@app.route("/test_soccer_league", methods=["GET"])
def test():
    if request.method == "GET":
        data = get_all_leagues(conn)

    return {"leagues": data}


@app.route("/soccer_league/reset", methods=["GET"])
def set_up_soccer_league():
    conn = create_connection()
    if request.method == "GET":
        league_id = request.get_json().get("league_id")
        league_name, teams_lst = set_up_soccer_teams(conn, league_id)
        soccer_league.reset_season(teams_lst)
        table = soccer_league.prepare_season()
        return {"data": table}


@app.route("/soccer_league/run", methods=["GET"])
def run_soccer_league():
    conn = create_connection()
    if request.method == "GET":
        league_id = request.get_json().get("league_id")
        table = soccer_league.run_season()
        return {"data": table}
