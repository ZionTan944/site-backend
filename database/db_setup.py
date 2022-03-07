import sqlite3
from flask import g

from sqlite3 import Error
from database.sql_script import sql_set_up_tables
from services.json_services import read_json_file
from services.soccer_services import insert_new_league, insert_new_team


def create_connection(
    db_file="C:/Users/DELL/Desktop/Random/More/Site/site-backend/database.db"
):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)

    return conn


def set_up_database(conn, create_table_sql):
    try:
        c = conn.cursor()
        for sql_script in create_table_sql.split("--"):
            c.execute(sql_script)
    except Error as e:
        print(e)


def main():
    database = "C:/Users/DELL/Desktop/Random/More/Site/site-backend/database.db"
    conn = create_connection(database)

    if conn is not None:
        # Create Tables
        set_up_database(conn, sql_set_up_tables)

        soccer_data = read_json_file("database/soccer_data.json")
        for league in soccer_data["leagues"]:
            league_id = insert_new_league(
                conn, league["name"], str(league["meta"]).replace("'", '"')
            )
            for team in league["teams"]:
                insert_new_team(
                    conn, team["name"], team["int"], team["rate"], league_id
                )

    else:
        print("Error! database setup failed")


if __name__ == "__main__":
    main()
