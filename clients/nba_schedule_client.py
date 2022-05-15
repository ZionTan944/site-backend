import random
from services.common_services import flatten_list

# Each team plays:
# 16G = 4 games against 4 teams in same division SIMPLE ROTATIONAL 2A 2H
# 24G = 4 games against 6 teams in same conference, different division   SIMPLE ROTATIONAL 2A 2H
# 12G = 3 games against 4 teams in same conference, different division (1H, 2A) or (2H,1A) random
# 30G = 2 games against 15 teams in opposite conference 1H 1A
# USE i-1, i-2, i+1, i+2 as teams to play this format, NEEDS 2 TEAMS FOR (1H,2A) and 2 for (2H,1A)
# LIST NEEDS TO BE IN FORMAT OF alternating divisions, (1 2 3 1 2 3 ....)


# Total 41 home 41 away
class NbaScheduling:
    def __init__(self, team_lst):
        """
        team_lst : {
                    "East": {
                        "Atlantic": {
                            "PHI": TeamClass(Philadelphia 76ers),
                            ...
                        },
                        "Central": {5 teams in Central},
                        "Southeast": {5 teams in Southeast}
                    },
                    "West": {
                        "Northwest": {5 teams in Northwest},
                        "Pacific": {5 teams in Pacific},
                        "Southwest": {5 teams in Southwest}
                    },
        }"""
        self.team_lst = team_lst
        self.conferences = list(self.team_lst.keys())
        self.divisions = [
            list(self.team_lst["East"].keys()),
            list(self.team_lst["West"].keys()),
        ]
        self.teams = [
            [
                list(self.team_lst["East"]["Atlantic"].keys()),
                list(self.team_lst["East"]["Central"].keys()),
                list(self.team_lst["East"]["Southeast"].keys()),
            ],
            [
                list(self.team_lst["West"]["Northwest"].keys()),
                list(self.team_lst["West"]["Pacific"].keys()),
                list(self.team_lst["West"]["Southwest"].keys()),
            ],
        ]
        self.games_lst = []
        self.season_length = 182
        self.schedule = [[] for i in range(self.season_length)]
        self.season_game_length_days_count = [
            15,
            12,
            16,
            18,
            22,
            24,
            20,
            15,
            15,
            11,
            9,
            7,
            5,
        ]
        self.season_allowed_game_length_days = [
            0,
            2,
            3,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
        ]

    def randomise_teams(self):
        return None

    # 2 games against 15 teams in opposing conference
    def map_inter_conference_games(self, conference):
        opponent_conference = "West" if conference == "East" else "East"
        for division_key, division in self.team_lst[conference].items():
            for team_key in division.keys():
                for opponent_division_key, opponent_division in self.team_lst[
                    opponent_conference
                ].items():
                    for opponent_team_key in opponent_division.keys():
                        self.games_lst.append(
                            [
                                [conference, division_key, team_key],
                                [
                                    opponent_conference,
                                    opponent_division_key,
                                    opponent_team_key,
                                ],
                            ]
                        )

    # 3 games against 4 teams in same conference, different division (1H, 2A) or (2H,1A) random
    def map_conference_games(self, conference):
        conference_index = self.conferences.index(conference)

        for division_key, division in self.team_lst[conference].items():
            for team_key in division.keys():
                division_index = self.divisions[conference_index].index(division_key)
                team_index = self.teams[conference_index][division_index].index(
                    team_key
                )
                # 2H and 1A games against divisionindex +1
                self.games_lst.append(
                    [
                        [conference, division_key, team_key],
                        [
                            conference,
                            self.divisions[conference_index][(division_index + 1) % 3],
                            self.teams[conference_index][(division_index + 1) % 3][
                                (team_index + 1) % 5
                            ],
                        ],
                    ]
                )

                self.games_lst.insert(
                    0,
                    [
                        [conference, division_key, team_key],
                        [
                            conference,
                            self.divisions[conference_index][(division_index + 1) % 3],
                            self.teams[conference_index][(division_index + 1) % 3][
                                (team_index + 1) % 5
                            ],
                        ],
                    ],
                )

                self.games_lst.insert(
                    len(self.games_lst) // 2,
                    [
                        [
                            conference,
                            self.divisions[conference_index][(division_index + 1) % 3],
                            self.teams[conference_index][(division_index + 1) % 3][
                                (team_index + 1) % 5
                            ],
                        ],
                        [conference, division_key, team_key],
                    ],
                )

                # 1H and 2A games against divisionindex +2
                self.games_lst.append(
                    [
                        [conference, division_key, team_key],
                        [
                            conference,
                            self.divisions[conference_index][(division_index + 2) % 3],
                            self.teams[conference_index][(division_index + 2) % 3][
                                (team_index + 1) % 5
                            ],
                        ],
                    ]
                )

                self.games_lst.insert(
                    0,
                    [
                        [
                            conference,
                            self.divisions[conference_index][(division_index + 2) % 3],
                            self.teams[conference_index][(division_index + 2) % 3][
                                (team_index + 1) % 5
                            ],
                        ],
                        [conference, division_key, team_key],
                    ],
                )

                self.games_lst.insert(
                    len(self.games_lst) // 2,
                    [
                        [
                            conference,
                            self.divisions[conference_index][(division_index + 2) % 3],
                            self.teams[conference_index][(division_index + 2) % 3][
                                (team_index + 1) % 5
                            ],
                        ],
                        [conference, division_key, team_key],
                    ],
                )

                for opponent_division_key, opponent_division in self.team_lst[
                    conference
                ].items():
                    for opponent_team_key in opponent_division:
                        opponent_division_index = self.divisions[
                            conference_index
                        ].index(opponent_division_key)
                        opponent_team_index = self.teams[conference_index][
                            opponent_division_index
                        ].index(opponent_team_key)
                        # Check not same team
                        if (
                            opponent_team_key == team_key
                            and opponent_division_key == division_key
                        ):
                            continue
                        if (
                            opponent_team_index == (team_index + 1) % 5
                            and opponent_division_index == (division_index + 1) % 3
                            or opponent_team_index == (team_index + 1) % 5
                            and opponent_division_index == (division_index + 2) % 3
                        ):
                            continue

                        self.games_lst.append(
                            [
                                [conference, division_key, team_key],
                                [
                                    conference,
                                    opponent_division_key,
                                    opponent_team_key,
                                ],
                            ]
                        )

    # 4 games against 4 teams in same division SIMPLE ROTATIONAL 2A 2H
    def map_divisional_games(self, conference, division):
        for team_key in self.team_lst[conference][division].keys():
            for opponent_team_key in self.team_lst[conference][division].keys():
                if team_key == opponent_team_key:
                    continue

                # Total 2H 2A, other two H and A games will be appended on opponents index
                self.games_lst.append(
                    [
                        [
                            conference,
                            division,
                            opponent_team_key,
                        ],
                        [
                            conference,
                            division,
                            team_key,
                        ],
                    ]
                )
                self.games_lst.append(
                    [
                        [
                            conference,
                            division,
                            team_key,
                        ],
                        [
                            conference,
                            division,
                            opponent_team_key,
                        ],
                    ]
                )

    def schedule_games(self):

        current_games_lst = self.games_lst[:]
        added_games_count = 0
        previous_selected_game_length_day = 0
        for day_index in range(len(self.schedule)):
            updated_games_lst = current_games_lst[:]

            selected_game_limit = random.randint(
                0, len(self.season_allowed_game_length_days) - 1
            )
            while (
                self.season_game_length_days_count[selected_game_limit] == 0
                or (
                    previous_selected_game_length_day
                    + self.season_allowed_game_length_days[selected_game_limit]
                    == 0
                )
                or (
                    previous_selected_game_length_day
                    + self.season_allowed_game_length_days[selected_game_limit]
                    > 25
                )
            ):
                selected_game_limit = random.randint(
                    0, len(self.season_allowed_game_length_days) - 1
                )
            self.season_game_length_days_count[selected_game_limit] -= 1
            previous_selected_game_length_day = self.season_allowed_game_length_days[
                selected_game_limit
            ]

            for game in updated_games_lst:
                if day_index >= 2:
                    if game[0] in flatten_list(self.schedule[day_index - 2]) and game[
                        0
                    ] in flatten_list(self.schedule[day_index - 1]):
                        continue
                    elif game[1] in flatten_list(self.schedule[day_index - 2]) and game[
                        1
                    ] in flatten_list(self.schedule[day_index - 1]):
                        continue

                if (
                    len(self.schedule[day_index])
                    >= self.season_allowed_game_length_days[selected_game_limit]
                ):
                    break
                elif game[0] in flatten_list(self.schedule[day_index]) or game[
                    1
                ] in flatten_list(self.schedule[day_index]):
                    continue

                else:

                    self.schedule[day_index].append(game)
                    current_games_lst.remove(game)
                    added_games_count += 1

    def start_league(self):

        self.randomise_teams()

        # create league game schedule
        for conference in self.team_lst.keys():
            self.map_inter_conference_games(conference)
            self.map_conference_games(conference)
            for division in self.team_lst[conference].keys():
                self.map_divisional_games(conference, division)

        # Total length should be 1230
        # print(len(self.games_lst))

        self.schedule_games()
