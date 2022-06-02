class Team:
    def __init__(self, conference, division, team_name, team_int):
        self.conference = conference
        self.division = division
        self.games = []
        self.team_name = team_name
        self.team_int = team_int
        self.games_in_row = 0
        self.no_game_count = 0
        self.schedule = []

    def add_game_to_schedule(self, game, day):

        current_season_length = len(self.schedule)
        while day > current_season_length + 1:
            self.schedule.append({})
            current_season_length += 1

        self.schedule.append({"game": game, "day": day})
