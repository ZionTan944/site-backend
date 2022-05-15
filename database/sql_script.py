SQL_TABLES_SETUP = """
DROP TABLE IF EXISTS soccer_leagues;
--
DROP TABLE IF EXISTS soccer_teams;
--
 CREATE TABLE IF NOT EXISTS soccer_leagues (
    id integer PRIMARY KEY,
    league_name varchar(255) NOT NULL,
    meta_json TEXT
);
--
CREATE TABLE IF NOT EXISTS soccer_teams (
    id integer PRIMARY KEY,
    team_name varchar(255) NOT NULL,
    team_int varchar(255) NOT NULL,
    team_rating integer,
    league_id integer NOT NULL,
    FOREIGN KEY (team_rating) REFERENCES soccer_league (id)
);
--
CREATE TABLE IF NOT EXISTS nba_teams (
    id integer PRIMARY KEY,
    team_name varchar(255) NOT NULL,
    team_int varchar(255) NOT NULL,
    team_rating integer,
    conference_key varchar(255) NOT NULL,
    division_key varchar(255) NOT NULL
);
"""
