class SoccerTeamClient:
    def __init__(self, team_name, team_int, team_rate, index):
        self.scheduled_games = []
        self.team_name = team_name
        self.team_int = team_int
        self.team_rate = team_rate
        self.fitness = 100
        self.form = 140
        self.consecutive_form = [0, 0]
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.points = 0
        self.expected_placing = index
        self.current_placing = index
        self.historical_placing = []

    def record_stats(self, match_index, goals_for, goals_against, meta=None):

        self.games_played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        self.goal_difference = self.goal_difference + goals_for - goals_against
        self.scheduled_games[match_index]["gf"] = goals_for
        self.scheduled_games[match_index]["ga"] = goals_against
        self.fitness = max(self.fitness - 4, 20)

        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
            self.scheduled_games[match_index]["result"] = "W"
            self.consecutive_form[0] += 1
            self.form = min(
                self.form
                + (goals_for - goals_against)
                + min(self.consecutive_form[0], 5)
                + min(self.consecutive_form[1], 5),
                200,
            )
            self.consecutive_form[1] = 0

        elif goals_for < goals_against:
            self.losses += 1
            self.scheduled_games[match_index]["result"] = "L"
            self.consecutive_form[1] += 1
            self.form = max(
                self.form
                - (goals_against - goals_for)
                - min(self.consecutive_form[1], 5)
                - min(self.consecutive_form[0], 5),
                80,
            )
            self.consecutive_form[0] = 0

        else:
            self.draws += 1
            self.points += 1
            self.scheduled_games[match_index]["result"] = "D"
            self.consecutive_form[0] = 0
            self.consecutive_form[1] = 0
            self.form = max(self.form - ((max(1, goals_against)) * 1), 80)

    def __str__(self):
        return self.team_name
