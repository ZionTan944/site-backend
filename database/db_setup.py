import sqlite3

from sqlite3 import Error
from database.sql_script import SQL_TABLES_SETUP
from services.json_services import read_json_file
from services.soccer_services import insert_new_league, insert_new_team
from services.nba_services import insert_nba_team


def create_connection(
    db_file="C:/Users/DELL/Desktop/Random/More/Site/site-backend/database.db",
):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as error:
        print(error)

    return conn


def set_up_database(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        for sql_script in create_table_sql.split("--"):
            cursor.execute(sql_script)
    except Error as error:
        print(error)


def setup_soccer_data(conn):
    soccer_data = read_json_file("database/soccer_data.json")
    for league in soccer_data["leagues"]:
        league_id = insert_new_league(
            conn, league["name"], str(league["meta"]).replace("'", '"')
        )
        for team in league["teams"]:
            insert_new_team(conn, team["name"], team["int"], team["rate"], league_id)


def setup_nba_data(conn):
    soccer_data = read_json_file("database/nba_data.json")
    for conference_key, conference in soccer_data.items():
        for division_key, division in conference.items():
            for team_key, team in division.items():
                insert_nba_team(
                    conn, team["Name"], team_key, 0, conference_key, division_key
                )


def main():
    database = "C:/Users/DELL/Desktop/Random/More/Site/site-backend/database.db"
    conn = create_connection(database)

    if conn is not None:
        # Create Tables
        set_up_database(conn, SQL_TABLES_SETUP)

        setup_soccer_data(conn)
        setup_nba_data(conn)

    else:
        print("Error! database setup failed")


if __name__ == "__main__":
    main()
