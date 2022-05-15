from clients.soccer_team_client import SoccerTeamClient


def get_all_leagues(conn):
    cursor = conn.execute("SELECT * FROM soccer_leagues;")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    return result


def get_league_by_id(conn, league_id):
    cursor = conn.execute(f"SELECT * FROM soccer_leagues WHERE id = {league_id};")
    row = cursor.fetchone()
    return dict(row)


def get_all_teams_by_league(conn, league_id):
    cursor = conn.execute(
        f"SELECT * FROM soccer_teams WHERE league_id = {league_id} ORDER BY team_rating;"
    )
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    return result


def insert_new_league(conn, league_name, meta_json=""):
    cursor = conn.execute(
        f"INSERT INTO soccer_leagues (league_name, meta_json) VALUES ('{league_name}','{meta_json}');"
    )
    conn.commit()
    league_id = cursor.lastrowid
    return league_id


def insert_new_team(conn, team_name, team_int, team_rating, league_id):
    conn.execute(
        f"""INSERT INTO soccer_teams (team_name, team_int, team_rating, league_id)
         VALUES ('{team_name}','{team_int}',{team_rating},{league_id});"""
    )
    conn.commit()
    return True


def set_up_soccer_teams(conn, league_id):
    league = get_league_by_id(conn, league_id)
    teams = get_all_teams_by_league(conn, league_id)
    team_class_list = []
    index = 1
    for team in teams:
        team_class_list.append(
            SoccerTeamClient(
                team["team_name"],
                team["team_int"],
                team["team_rating"],
                (len(teams) + 1) - index,
            )
        )
        index += 1

    return league["league_name"], team_class_list, league["meta_json"]
