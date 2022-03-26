import json

from flask import request

from index import app
from database.db_setup import create_connection
from services.soccer_services import get_all_leagues, set_up_soccer_teams
from clients.soccer_league_client import SoccerLeagueClient

conn = create_connection()
league_name, teams_lst, meta = set_up_soccer_teams(conn, 1)
soccer_league = SoccerLeagueClient(league_name, teams_lst, meta)
soccer_league.prepare_season()


@app.route("/test_soccer_league", methods=["POST"])
def test():
    if request.method == "POST":
        data = get_all_leagues(conn)

    return {"leagues": data}


@app.route("/soccer_league/reset", methods=["POST"])
def set_up_soccer_league():
    if request.method == "POST":
        league_id = json.loads(request.data).get("league_id")
        league_name, teams_lst, meta = set_up_soccer_teams(conn, league_id)
        soccer_league.reset_season(teams_lst, meta)
        table, schedule = soccer_league.prepare_season()
        return {
            "league_table": table,
            "match_week": 0,
            "league_name": league_name,
            "total_weeks": soccer_league.season_length,
            "meta": json.loads(meta),
            "match_results": schedule,
        }


@app.route("/soccer_league/run", methods=["POST"])
def run_soccer_league():
    if request.method == "POST":
        (
            extra_stats,
            table,
            match_results,
            table_history,
            match_week,
        ) = soccer_league.run_season()
        return {
            "league_table": table,
            "match_results": match_results,
            "match_week": match_week,
            "extra_stats": extra_stats,
            "table_history": table_history,
        }


@app.route("/soccer_league/get_team", methods=["POST"])
def get_soccer_team_schedule():
    if request.method == "POST":
        response = []
        team_names = json.loads(request.data).get("team_names")
        for team_name in team_names:
            if team_name == "":
                response.append({"schedule": [{}], "team_data": {}})
                continue
            team = soccer_league.return_team_by_name(team_name)
            team_schedule = team.scheduled_games
            team_data = {
                "team_int": team.team_int,
                "form": team.form,
                "fitness": team.fitness,
                "place": team.current_placing,
                "w": team.wins,
                "l": team.losses,
                "d": team.draws,
                "gf": team.goals_for,
                "ga": team.goals_against,
                "gd": team.goal_difference,
                "gp": team.games_played,
                "ex": team.expected_placing,
            }
            response.append({"schedule": team_schedule, "team_data": team_data})

        return {"response": response}
