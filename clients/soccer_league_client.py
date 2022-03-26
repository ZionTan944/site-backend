import random
import math
from copy import deepcopy

from .soccer_team_client import SoccerTeamClient
from .table_sorter import run_merge_sort


class SoccerLeagueClient:
    def __init__(self, league_name, team_list, meta):
        self.match_time_range = 95
        self.match_week = 1
        self.league_name = league_name
        self.team_list = team_list
        # key: team_name, value: index for team in team_list
        self.team_list_mapping = {}
        self.schedule = []
        self.meta = meta

    def return_team_by_name(self, name):
        return self.team_list[self.team_list_mapping[name]]

    def reset_season(self, team_list, meta):
        self.team_list = deepcopy(team_list)
        self.match_week = 1
        self.meta = meta

    def randomise_team_list(self):
        random_counter = len(self.team_list) // 2
        while True:
            random_team = random.randint(0, len(self.team_list) - 1)
            self.team_list.append(self.team_list.pop(random_team))
            if random.randint(0, random_counter) == 0:
                break
            random_counter -= 1

        self.team_list.insert(0, SoccerTeamClient("REST1", "RES", 0, 0))
        self.team_list.append(SoccerTeamClient("REST2", "RES", 0, 0))

        for team_index in range(len(self.team_list)):
            self.team_list_mapping[self.team_list[team_index].team_name] = team_index

    def set_extra_info(self, team, extra_stats):
        if team.form > extra_stats["hot"][1]["value"]:
            if team.form > extra_stats["hot"][0]["value"]:
                extra_stats["hot"] = [
                    {
                        "team_name": team.team_name,
                        "team_int": team.team_int,
                        "value": team.form,
                        "latest_game": team.scheduled_games[self.match_week - 1],
                    },
                    extra_stats["hot"][0],
                ]
            else:
                extra_stats["hot"] = [
                    extra_stats["hot"][0],
                    {
                        "team_name": team.team_name,
                        "team_int": team.team_int,
                        "value": team.form,
                        "latest_game": team.scheduled_games[self.match_week - 1],
                    },
                ]
        if team.form < extra_stats["cold"][1]["value"]:
            if team.form <= extra_stats["cold"][0]["value"]:
                extra_stats["cold"] = [
                    {
                        "team_name": team.team_name,
                        "team_int": team.team_int,
                        "value": team.form,
                        "latest_game": team.scheduled_games[self.match_week - 1],
                    },
                    extra_stats["cold"][0],
                ]
            else:
                extra_stats["cold"] = [
                    extra_stats["cold"][0],
                    {
                        "team_name": team.team_name,
                        "team_int": team.team_int,
                        "value": team.form,
                        "latest_game": team.scheduled_games[self.match_week - 1],
                    },
                ]

    def set_schedule(self, schedule, forward_schedule, return_schedule):
        # Combine Schedules in format  [f1, r-1, f2, r-2 ...]
        for index, _ in enumerate(forward_schedule):
            schedule.append(forward_schedule[index])
            schedule.append(return_schedule[-index - 1])

        self.schedule = schedule
        # Set individual team's schedule
        for index, match_week in enumerate(self.schedule):
            for match in match_week:
                home_team = self.return_team_by_name(match["home_team_name"])
                away_team = self.return_team_by_name(match["away_team_name"])
                home_team.scheduled_games.append(
                    {
                        "opponent_name": away_team.team_name,
                        "opponent": away_team.team_int,
                        "location": "H",
                        "result": "NP",
                        "gf": None,
                        "ga": None,
                        "match_week": index + 1,
                    }
                )
                away_team.scheduled_games.append(
                    {
                        "opponent_name": home_team.team_name,
                        "opponent": home_team.team_int,
                        "location": "A",
                        "result": "NP",
                        "gf": None,
                        "ga": None,
                        "match_week": index + 1,
                    }
                )

    def generate_schedule(self):
        schedule = []
        forward_schedule = []
        return_schedule = []
        # Number of match week
        for match_week in range(1, len(self.team_list)):
            weekly_matches = []
            return_weekly_matches = []
            # Number of matches per week
            for match_index in range(len(self.team_list) // 2):
                weekly_matches.append(
                    {
                        "home_team_name": self.team_list[match_index].team_name,
                        "away_team_name": self.team_list[
                            (len(self.team_list) - 1) - match_index
                        ].team_name,
                        "home_team": self.team_list[match_index].team_int,
                        "away_team": self.team_list[
                            (len(self.team_list) - 1) - match_index
                        ].team_int,
                        "home_goals": None,
                        "away_goals": None,
                    }
                )
                return_weekly_matches.append(
                    {
                        "away_team_name": self.team_list[match_index].team_name,
                        "home_team_name": self.team_list[
                            (len(self.team_list) - 1) - match_index
                        ].team_name,
                        "away_team": self.team_list[match_index].team_int,
                        "home_team": self.team_list[
                            (len(self.team_list) - 1) - match_index
                        ].team_int,
                        "home_goals": None,
                        "away_goals": None,
                    }
                )
            self.team_list.insert(1, self.team_list.pop())
            forward_schedule.append(
                weekly_matches if match_week % 2 == 0 else return_weekly_matches
            )
            return_schedule.append(
                return_weekly_matches if match_week % 2 == 0 else weekly_matches
            )

        self.set_schedule(schedule, forward_schedule, return_schedule)

    def play_match(self, match_index, home_team, away_team, knockout=False):
        if home_team.team_int == "RES" or away_team.team_int == "RES":
            home_team.fitness = 100
            away_team.fitness = 100
            return None

        home_rate = int(
            home_team.team_rate
            * (
                1
                + ((home_team.form - 140) / 300)
                + ((home_team.fitness - 60) / 400)
                + 0.1
            )
        )
        away_rate = int(
            away_team.team_rate
            * (1 + ((away_team.form - 140) / 300) + ((away_team.fitness - 60) / 400))
        )

        goal_range = (home_rate * 33) + (away_rate * 33)

        home_goals = 0
        away_goals = 0
        for _ in range(self.match_time_range):
            goal_sum = random.randint(0, goal_range)

            if goal_sum >= 0 and goal_sum <= away_rate:
                away_goals += 1
            elif goal_sum >= (goal_range - home_rate):
                home_goals += 1

        home_team.record_stats(match_index, home_goals, away_goals)
        away_team.record_stats(match_index, away_goals, home_goals)
        match_str = f"{home_team.form}{home_team.team_int}({home_team.team_rate}/{home_rate}) {home_goals} - {away_goals} ({away_team.team_rate}/{away_rate}){away_team.team_int}{away_team.form}"
        print(match_str)

        return {"home_goals": home_goals, "away_goals": away_goals}

    def run_match_week(self):
        extra_stats = {
            "hot": [{"team_name": "", "value": 0}, {"team_name": "", "value": 0}],
            "cold": [
                {"team_name": "", "value": 1000},
                {"team_name": "", "value": 1000},
            ],
        }
        if self.match_week <= self.season_length:  # while
            match_index = self.match_week - 1
            print("Match Week:", self.match_week)
            match_results = []
            for match in self.schedule[match_index]:
                home_team = self.return_team_by_name(match["home_team_name"])
                away_team = self.return_team_by_name(match["away_team_name"])
                result = self.play_match(match_index, home_team, away_team)

                if result is not None:
                    match_results.append(result)
                    match["home_goals"] = result["home_goals"]
                    match["away_goals"] = result["away_goals"]
                    self.set_extra_info(home_team, extra_stats)
                    self.set_extra_info(away_team, extra_stats)

            self.match_week += 1

        return extra_stats

    def sort_league_table(self, in_season=True):
        unsorted_table = self.team_list[1:-1] if in_season is True else self.team_list
        sorted_dict = run_merge_sort(unsorted_table)

        sorted_table = []
        historical_table = []
        for index, _ in enumerate(sorted_dict):
            if (index + 1) > sorted_dict[index].current_placing:
                team_movement = "˅"
            elif (index + 1) < sorted_dict[index].current_placing:
                team_movement = "˄"
            else:
                team_movement = "="

            sorted_dict[index].current_placing = index + 1
            sorted_dict[index].historical_placing.append(index + 1)
            historical_table.append(sorted_dict[index].historical_placing)
            sorted_table.append(
                {
                    "Placing": index + 1,
                    "Team Name": sorted_dict[index].team_name,
                    "Logo": sorted_dict[index].team_int,
                    "Games Played": sorted_dict[index].games_played,
                    "Wins": sorted_dict[index].wins,
                    "Draws": sorted_dict[index].draws,
                    "Losses": sorted_dict[index].losses,
                    "Goals For": sorted_dict[index].goals_for,
                    "Goals Against": sorted_dict[index].goals_against,
                    "Goal Difference": sorted_dict[index].goal_difference,
                    "Points": sorted_dict[index].points,
                    "Team Movement": team_movement,
                }
            )
        # for row in sorted_table:
        #     print(row)

        self.sorted_dict = sorted_dict
        return sorted_table, historical_table

    def prepare_season(self):
        table, _ = self.sort_league_table(in_season=False)
        self.randomise_team_list()
        self.generate_schedule()
        self.season_length = (len(self.team_list) * 2) - 2

        return table, self.schedule

    def run_season(self):
        if self.match_week <= self.season_length:
            extra_stats = self.run_match_week()
            table, table_history = self.sort_league_table()

            return extra_stats, table, self.schedule, table_history, self.match_week - 1

        return {}, [], [], []
