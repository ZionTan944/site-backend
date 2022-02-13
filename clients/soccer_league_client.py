import random
import math
from copy import deepcopy

from .soccer_team_client import SoccerTeamClient
from .soccer_match_client import SoccerMatchClient
from .table_sorter import run_merge_sort

soccer_match_client = SoccerMatchClient()


class SoccerLeagueClient:
    def __init__(self, league_name, team_list):
        self.match_week = 1
        self.league_name = league_name
        self.team_list = team_list
        # key: team_name, value: index for team in team_list
        self.team_list_mapping = {}
        self.schedule = []

    def return_team_by_name(self, name):
        return self.team_list[self.team_list_mapping[name]]

    def reset_season(self, team_list):
        self.team_list = deepcopy(team_list)

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

    def set_schedule(self, schedule, forward_schedule, return_schedule):
        # Combine Schedules in format  [f1, r-1, f2, r-2 ...]
        for index, _ in enumerate(forward_schedule):
            schedule.append(forward_schedule[index])
            schedule.append(return_schedule[-index - 1])

        self.schedule = schedule
        # Set individual team's schedule
        for match_week in self.schedule:
            for match in match_week:
                home_team = self.return_team_by_name(match[0])
                away_team = self.return_team_by_name(match[1])
                home_team.scheduled_games.append(
                    {
                        "opponent_name": away_team.team_name,
                        "opponent": away_team.team_int,
                        "location": "H",
                        "result": "NP",
                        "gf": None,
                        "ga": None,
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
                    [
                        self.team_list[match_index].team_name,
                        self.team_list[
                            (len(self.team_list) - 1) - match_index
                        ].team_name,
                    ]
                )
                return_weekly_matches.append(
                    [
                        self.team_list[
                            (len(self.team_list) - 1) - match_index
                        ].team_name,
                        self.team_list[match_index].team_name,
                    ]
                )
            self.team_list.insert(1, self.team_list.pop())
            forward_schedule.append(
                weekly_matches if match_week % 2 == 0 else return_weekly_matches
            )
            return_schedule.append(
                return_weekly_matches if match_week % 2 == 0 else weekly_matches
            )

        self.set_schedule(schedule, forward_schedule, return_schedule)

    def run_match_week(self):
        if self.match_week <= self.season_length:  # while
            match_index = self.match_week - 1
            print("Match Week:", self.match_week)
            match_results = []
            for match in self.schedule[match_index]:
                home_team = self.return_team_by_name(match[0])
                away_team = self.return_team_by_name(match[1])
                result = soccer_match_client.play_match(
                    match_index, home_team, away_team
                )
                match_results.append(result)

            self.match_week += 1
            return match_results

    def sort_league_table(self, in_season=True):
        unsorted_table = self.team_list[1:-1] if in_season is True else self.team_list
        sorted_dict = run_merge_sort(unsorted_table)

        sorted_table = []
        for index, _ in enumerate(sorted_dict):
            if (index + 1) > sorted_dict[index].current_placing:
                team_movement = "˅"
            elif (index + 1) < sorted_dict[index].current_placing:
                team_movement = "˄"
            else:
                team_movement = "="

            sorted_dict[index].current_placing = index + 1
            sorted_dict[index].historical_placing.append(index + 1)

            sorted_table.append(
                {
                    "Placing": index + 1,
                    "Team Name": sorted_dict[index].team_name,
                    "Games Played": sorted_dict[index].games_played,
                    "Wins": sorted_dict[index].wins,
                    "Draws": sorted_dict[index].draws,
                    "Losses": sorted_dict[index].losses,
                    "Goals For": sorted_dict[index].goals_for,
                    "Goals Against": sorted_dict[index].goals_against,
                    "Goal Difference": sorted_dict[index].goal_difference,
                    "Points": sorted_dict[index].points,
                    "Movement": team_movement,
                }
            )
        for row in sorted_table:
            print(row)

        self.sorted_dict = sorted_dict
        return sorted_table

    def prepare_season(self):
        table = self.sort_league_table(in_season=False)
        self.randomise_team_list()
        self.generate_schedule()
        self.season_length = (len(self.team_list) * 2) - 2

        return table

    def run_season(self):
        if self.match_week <= self.season_length:
            match_results = self.run_match_week()
            table = self.sort_league_table()

            return table, match_results, self.match_week

        return [], [], self.match_week
