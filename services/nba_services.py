from clients.nba_team_client import Team


def insert_nba_team(
    conn, team_name, team_int, team_rating, conference_key, division_key
):
    conn.execute(
        f"""INSERT INTO nba_teams (team_name, team_int, team_rating, conference_key, division_key)
         VALUES ('{team_name}','{team_int}',{team_rating},'{conference_key}','{division_key}');"""
    )
    conn.commit()
    return True


def group_nba_teams(nba_teams):
    nba_teams_dict = {
        "East": {"Atlantic": {}, "Central": {}, "Southeast": {}},
        "West": {"Northwest": {}, "Pacific": {}, "Southwest": {}},
    }
    nba_teams_class_dict = {
        "East": {"Atlantic": {}, "Central": {}, "Southeast": {}},
        "West": {"Northwest": {}, "Pacific": {}, "Southwest": {}},
    }
    for nba_team in nba_teams:
        nba_teams_dict[nba_team["conference_key"]][nba_team["division_key"]][
            nba_team["team_int"]
        ] = nba_team

        nba_teams_class_dict[nba_team["conference_key"]][nba_team["division_key"]][
            nba_team["team_int"]
        ] = Team(
            nba_team["conference_key"],
            nba_team["division_key"],
            nba_team["team_int"],
            nba_team["team_name"],
        )

    return nba_teams_dict, nba_teams_class_dict


def get_all_nba_teams(conn):
    cursor = conn.execute("SELECT * FROM nba_teams;")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    return group_nba_teams(result)
