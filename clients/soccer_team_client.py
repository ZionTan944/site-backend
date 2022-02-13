class SoccerTeamClient:
    def __init__(self, team_name, team_int, team_rate, index):
        self.scheduled_games = []
        self.team_name = team_name
        self.team_int = team_int
        self.team_rate = team_rate
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.points = 0
        self.current_placing = index
        self.historical_placing = []

    def record_stats(self, match_index, goals_for, goals_against, meta=None):

        self.games_played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        self.goal_difference = self.goal_difference + goals_for - goals_against
        self.scheduled_games[match_index]["gf"] = goals_for
        self.scheduled_games[match_index]["ga"] = goals_against

        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
            self.scheduled_games[match_index]["result"] = "W"
        elif goals_for < goals_against:
            self.losses += 1
            self.scheduled_games[match_index]["result"] = "L"
        else:
            self.draws += 1
            self.points += 1
            self.scheduled_games[match_index]["result"] = "D"

    def __str__(self):
        return self.team_name
