class Team:
    def __init__(self, conference, division, team_name, team_int):
        self.conference = conference
        self.division = division
        self.games = []
        self.team_name = team_name
        self.team_int = team_int
        self.daily_game_check = [0] * 176
        self.games_in_row = 0
        self.no_game_count = 0
