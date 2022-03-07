import random


class SoccerMatchClient:
    def __init__(self):
        self.match_time_range = 90
        self.overtime_range = 30

    def play_match(self, match_index, home_team, away_team, knockout=False):
        if home_team.team_int == "RES" or away_team.team_int == "RES":
            return None

        home_rate = int(home_team.team_rate * 1.1)
        away_rate = away_team.team_rate

        goal_range = (home_rate * 27) + (away_rate * 27)

        home_goals = 0
        away_goals = 0
        for _ in range(self.match_time_range):
            goal_sum = random.randint(0, goal_range)

            if goal_sum >= 0 and goal_sum <= away_team.team_rate:
                away_goals += 1
            elif goal_sum >= (goal_range - home_team.team_rate):
                home_goals += 1

        print(home_team.team_int, home_goals, "-", away_goals, away_team.team_int)

        home_team.record_stats(match_index, home_goals, away_goals)
        away_team.record_stats(match_index, away_goals, home_goals)

        return {
            "home_team_name": home_team.team_name,
            "home_team": home_team.team_int,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "away_team": away_team.team_int,
            "away_team_name": away_team.team_name,
        }
