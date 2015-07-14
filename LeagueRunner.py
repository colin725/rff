#!/usr/bin/python
import sys
import inspect
import random
import csv
import cProfile
import os


# Variables to change
year = "2014"
league_runs = 10000
debug_statements = False

# Not as likely to need changing
league_size = 12
weeks_in_season = 12
playoff_weeks_per_matchup = 2
num_playoff_teams = 4


robots = []
player_history = []
players_current_season = []
player_list = []


class Robot:
    def __init__(self, name, obj, num):
        self.name = name
        self.obj = obj
        self.num = num
        self.playoff_appearances = 0
        self.average_position = 0
        self.leagues_played = 0
        self.leagues_won = 0

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return str(self.name)

    def copy(self):
        return Robot(self.name, self.obj, self.num)

    def set_num(self, num):
        self.num = num

    def set_info(self):
        self.obj.set_info(player_history.copy())

    def draft_player(self, available_players, team):
        return self.obj.draft_player(available_players.copy(), team.copy())

    def made_playoffs(self):
        self.playoff_appearances += 1

    def playoffs_percent(self):
        return self.playoff_appearances / self.leagues_played * 100

    def won_league(self):
        self.leagues_won += 1

    def win_league_percent(self):
        return self.leagues_won / self.leagues_played * 100

    def position_played(self, draft_position):
        self.average_position = (self.average_position * self.leagues_played + draft_position)\
            / (self.leagues_played + 1)
        self.leagues_played += 1


class League:
    def __init__(self):
        # self.available_players = player_list.copy()
        self.available_players = list(range(0, len(player_list)))
        self.robots = robots.copy()
        self.teams = {}
        self.snake_round = False

    def __repr__(self):
        repr_string = "League: \n"
        for robot_num in range(0, league_size):
            repr_string = repr_string + str(self.robots[robot_num].num) + " " + str(self.robots[robot_num].name) + "\n"
        return repr_string

    def teams_to_string(self):
        repr_string = "\n"
        for team in self.teams.values():
            repr_string += str(team) + "\n"
        return repr_string

    def set_up(self, debug_info):
        # Set draft order
        random.shuffle(self.robots)
        for i in range(0, len(self.robots)):
            self.robots[i].position_played(i)
        if debug_info:
            print(self.robots)

        # Create empty teams
        for teamless_robot in self.robots:
            self.teams[teamless_robot.num] = Team()

    # Complete a single round of drafting
    def draft_round(self, drafting_round, debug_info):
        this_round = []

        def select_player(robot_selector):
            selected_player_number = robot_selector.draft_player(self.available_players, self.teams[robot_selector.num])
            if selected_player_number not in self.available_players:
                raise ValueError("A player number was passed from draft_player"
                                 " that was not in the list of available players")
            self.available_players.remove(selected_player_number)
            self.teams[robot_selector.num].add_player(selected_player_number)
            return selected_player_number

        if debug_info:
            print("\nDrafting round " + str(drafting_round + 1) + ": ")
        if not self.snake_round:
            for robot_for_snake in self.robots:
                this_round.append(player_list[select_player(robot_for_snake)])
            self.snake_round = True
        else:
            for robot_for_snake in reversed(self.robots):
                this_round.append(player_list[select_player(robot_for_snake)])
            self.snake_round = False
        if debug_info:
            print("    " + str(this_round))

    # evaluate a week
    def evaluate_week(self, week_number):
        # Find match-ups for the week and evaluate each
        # Made for a 12 man league to make match-ups even, may or may not work for other sizes
        # In a 12 man league it works out to this:
        #
        #          Opponents over the regular season (12 weeks)
        # Team 1: 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  7
        # Team 2: 11, 10,  9,  8,  7,  6,  5,  4,  3,  8,  1, 12
        # Team 3: 10,  9,  8,  7,  6,  5,  4,  9,  2,  1, 12, 11
        # Team 4:  9,  8,  7,  6,  5, 10,  3,  2,  1, 12, 11, 10
        # Team 5:  8,  7,  6, 11,  4,  3,  2,  1, 12, 11, 10,  9
        # Team 6:  7, 12,  5,  4,  3,  2,  1, 12, 11, 10,  9,  8
        # Team 7:  6,  5,  4,  3,  2,  1, 12, 11, 10,  9,  8,  1
        # Team 8:  5,  4,  3,  2,  1, 12, 11, 10,  9,  2,  7,  6
        # Team 9:  4,  3,  2,  1, 12, 11, 10,  3,  8,  7,  6,  5
        # Team 10: 3,  2,  1, 12, 11,  4,  9,  8,  7,  6,  5,  4
        # Team 11: 2,  1, 12,  5, 10,  9,  8,  7,  6,  5,  4,  3
        # Team 12: 1,  6, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2

        evaluated = []
        for i in range(0, int(len(self.teams) / 2)):
            for j in range(0, int(len(self.teams) / 2)):
                if (i + j) not in evaluated:
                    opponent_number = (league_size - (((i + j) + week_number) % league_size)) % league_size
                    if opponent_number == i + j:
                        # Collision.  Scheduled against yourself, so swap with the other team against itself
                        opponent_number += int(league_size / 2)
                    evaluated.append(i + j)
                    evaluated.append(opponent_number)

                    # Match-up chosen, evaluate it...
                    team1_total = self.teams[self.robots[i+j].num].eval(week_number)
                    team2_total = self.teams[self.robots[opponent_number].num].eval(week_number)
                    if team1_total > team2_total:
                        if debug_statements:
                            print("   matchup " + str(team1_total) + " > " + str(team2_total))
                        self.teams[self.robots[i+j].num].wins += 1
                    else:
                        if debug_statements:
                            print("   matchup " + str(team1_total) + " < " + str(team2_total))
                        self.teams[self.robots[opponent_number].num].wins += 1
                    break

    def run_playoffs(self, debug_info):
        # We're taking the top records.  We don't have divisions.
        playoff_robots = []
        for i in range(0, len(self.robots)):
            unranked_robot = self.robots[i]
            for j in range(0, num_playoff_teams):
                if len(playoff_robots) <= j:
                    playoff_robots.append(unranked_robot)
                    break
                elif self.teams[unranked_robot.num].wins > self.teams[playoff_robots[j].num].wins or\
                        self.teams[unranked_robot.num].wins == self.teams[playoff_robots[j].num].wins and\
                        self.teams[unranked_robot.num].season_total() >\
                        self.teams[playoff_robots[j].num].season_total():
                    temp_robot = playoff_robots[j]
                    playoff_robots[j] = unranked_robot
                    unranked_robot = temp_robot

        if debug_info:
            print("Playoff teams:")
        for i in range(0, num_playoff_teams):
            playoff_robots[i].made_playoffs()
            if debug_info:
                print("#" + str(i) + ": " + playoff_robots[i].name + " (" + str(playoff_robots[i].num) + ")" +
                      " with record " + str(self.teams[playoff_robots[i].num].wins) + "-" +
                      str(weeks_in_season - self.teams[playoff_robots[i].num].wins))
        if debug_info:
            print()

        # We have the playoff teams, evaluate them
        scores = [0] * num_playoff_teams
        for playoff_week in range(0, playoff_weeks_per_matchup):
            for playoff_team in range(0, num_playoff_teams):
                scores[playoff_team] += self.teams[playoff_robots[playoff_team].num].eval(
                    weeks_in_season + playoff_week + 1)

        finals_robots = []
        for playoff_matchup in range(0, int(num_playoff_teams / 2)):
            finals_robots.append(playoff_robots[playoff_matchup] if scores[playoff_matchup] >
                                 scores[num_playoff_teams - playoff_matchup - 1] else
                                 playoff_robots[num_playoff_teams - playoff_matchup - 1])

        # We have our teams in the next round (finals)
        scores = [0] * len(finals_robots)
        for finals_week in range(0, playoff_weeks_per_matchup):
            for finals_team in range(0, len(finals_robots)):
                scores[finals_team] += self.teams[finals_robots[finals_team].num].eval(
                    weeks_in_season + playoff_weeks_per_matchup + finals_week + 1)

        winning_robot = finals_robots[0] if scores[0] > scores[1] else finals_robots[1]
        winning_robot.won_league()

    def print_regular_season_results(self):
        print("Regular season results:")
        for i in range(0, len(self.teams)):
            print(str(self.robots[i].num) + ": " + self.robots[i].name + "   " +
                  str(self.teams[self.robots[i].num].wins) + "-" + str(weeks_in_season -
                                                                       self.teams[self.robots[i].num].wins))
        print()


class Team:
    starting_slots = {"QB": 1, "RB": 2, "WR": 2, "TE": 1, "FLEX": 1, "K": 1, "DEF": 1}

    def __init__(self):
        self.available_player_slots = Team.starting_slots.copy()
        self.players = []
        self.wins = 0
        self.evaluated = {}

    def set_fields(self, player_slots, players, wins, evaluated):
        self.available_player_slots = player_slots
        self.players = players
        self.wins = wins
        self.evaluated = evaluated
        return self

    def copy(self):
        return Team().set_fields(self.available_player_slots.copy(), self.players.copy(),
                                 self.wins, self.evaluated.copy())

    def __repr__(self):
        repr_string = ""
        rb_found = 0
        wr_found = 0
        te_found = 0
        flex = ""
        for repr_position in Team.starting_slots.keys():
            if not repr_position == "FLEX":
                repr_string += repr_position + ": \n"
                for player in self.players:
                    if player.position == repr_position:
                        if repr_position == "RB":
                            if rb_found == Team.starting_slots["RB"]:
                                flex = player_list[player.adp - 1]
                                break
                            rb_found += 1
                        elif repr_position == "WR":
                            if wr_found == Team.starting_slots["WR"]:
                                flex = player_list[player.adp - 1]
                                break
                            wr_found += 1
                        elif repr_position == "TE":
                            if te_found == Team.starting_slots["TE"]:
                                flex = player_list[player.adp - 1]
                                break
                            te_found += 1
                        repr_string += "  " + player_list[player.adp - 1] + "\n"
        repr_string += "Flex:\n  " + flex + "\n"
        repr_string += "\n"
        return repr_string

    def available_spots(self, available_position):
        return self.available_player_slots[available_position]

    def add_player(self, player_number):
        self.players.append(players_current_season[player_number])
        if self.available_player_slots[players_current_season[player_number].position] == 0:
            if self.available_player_slots["FLEX"] > 0 and players_current_season[player_number].position in\
                    ["RB", "WR", "TE"]:
                self.available_player_slots["FLEX"] -= 1
            else:
                raise ValueError("A " + str(players_current_season[player_number].position) +
                                 " was drafted when the team was already full.")
        else:
            self.available_player_slots[players_current_season[player_number].position] -= 1

    def is_position_open(self, position_questioned):
        if self.available_player_slots[position_questioned] > 0:
            return True
        elif self.available_player_slots["FLEX"] > 0 and position_questioned in ["RB", "WR", "TE"]:
            return True
        else:
            return False

    def eval(self, eval_week):
        total = self.evaluated.get(eval_week, 0)
        if total == 0:
            for player in self.players:
                if players_current_season[player.adp] is not None:
                    total += players_current_season[player.adp].get_week_score(eval_week)
            self.evaluated[eval_week] = total
        return total

    def season_total(self):
        points = 0
        for eval_week in range(1, weeks_in_season + 1):
            points += self.eval(eval_week)
        return points

    @staticmethod
    def size():
        size = 0
        for slots in Team.starting_slots.values():
            size += slots
        return size


class Player:
    def __init__(self, name, personal_adp, personal_position, team):
        self.name = name
        self.adp = personal_adp
        self.position = personal_position
        self.team = team

    def __repr__(self):
        return str(self.name)


class PlayerHistory:
    def __init__(self, position, self_adp, file_content):
        self.position = position
        self.adp = self_adp
        self.yearly_data = {}
        year_found = None

        def is_int(string):
            try:
                int(string)
                return True
            except ValueError:
                return False

        for line in file_content:
            if "season " in line:
                if is_int(line.split()[1]):
                    if "(Projected)" in line:
                        year_found = "Projected"
                    else:
                        year_found = int(line.split()[1])
                    if year_found != year:
                        self.yearly_data[year_found] = PlayerYear(position)
                        self.yearly_data[year_found].add_season_totals(line.split())
            else:
                if is_int(line.split()[1]):
                    week_number = int(line.split()[1])
                    self.yearly_data[year_found].add_week_data(week_number, line.split())

    def __repr__(self):
        represent_self = "PlayerHistory for " + player_list[self.adp - 1].name + ", position: " + self.position + "\n"
        for repr_year in range(2050, 1990, -1):
            if repr_year in self.yearly_data:
                represent_self += "    Year " + str(repr_year) + " " + str(self.yearly_data[repr_year]) + "\n"
        return represent_self


class PlayerYear:
    def __init__(self, position):
        self.position = position
        self.season_totals = None
        self.weekly_data = {}

    def add_season_totals(self, season_data):
        self.season_totals = PlayerSeasonStats(season_data, self.position)

    def add_week_data(self, week_number, week_data):
        self.weekly_data[week_number] = PlayerWeeklyStats(week_data, self.position)

    def __repr__(self):
        represent_self = "Season totals \n" + str(self.season_totals) + "\n"
        for week in range(17):
            if week in self.weekly_data:
                represent_self += "      and week " + str(week) + "   " + str(self.weekly_data[week]) + "\n"
        return represent_self


class PlayerStats:
    # Passing
    completions_position = {"QB": 0, "RB": None, "WR": None, "TE": None, "K": None, "DEF": None}
    attempts_position = {"QB": 1, "RB": None, "WR": None, "TE": None, "K": None, "DEF": None}
    completion_percent_position = {"QB": 2, "RB": None, "WR": None, "TE": None, "K": None, "DEF": None}
    passing_yards_position = {"QB": 3, "RB": None, "WR": None, "TE": None, "K": None, "DEF": None}
    passing_td_position = {"QB": 4, "RB": None, "WR": None, "TE": None, "K": None, "DEF": None}
    interceptions_thrown_position = {"QB": 5, "RB": None, "WR": None, "TE": None, "K": None, "DEF": None}

    # Rushing
    rushing_attempts_position = {"QB": 6, "RB": 0, "WR": 5, "TE": None, "K": None, "DEF": None}
    rushing_yards_position = {"QB": 7, "RB": 1, "WR": 6, "TE": None, "K": None, "DEF": None}
    rushing_avg_position = {"QB": 8, "RB": 2, "WR": 7, "TE": None, "K": None, "DEF": None}
    rushing_td_position = {"QB": 9, "RB": 3, "WR": 8, "TE": None, "K": None, "DEF": None}

    # Receiving
    receiving_targets_position = {"QB": None, "RB": 4, "WR": 0, "TE": 0, "K": None, "DEF": None}
    receiving_receptions_position = {"QB": None, "RB": 5, "WR": 1, "TE": 1, "K": None, "DEF": None}
    receiving_yards_position = {"QB": None, "RB": 6, "WR": 2, "TE": 2, "K": None, "DEF": None}
    receiving_avg_position = {"QB": None, "RB": 7, "WR": 3, "TE": 3, "K": None, "DEF": None}
    receiving_td_position = {"QB": None, "RB": 8, "WR": 4, "TE": 4, "K": None, "DEF": None}

    # Kicking
    fg_make_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": 0, "DEF": None}
    fg_attempt_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": 1, "DEF": None}
    fg_percent_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": 2, "DEF": None}
    ep_made_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": 3, "DEF": None}
    ep_attempt_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": 4, "DEF": None}

    # Defense
    sacks_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 0}
    fumble_recovery_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 1}
    interception_caught_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 2}
    defensive_td_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 3}
    points_allowed_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 4}
    passing_yards_allowed_per_game_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 5}
    rushing_yards_allowed_per_game_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 6}
    safeties_position = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 7}
    kick_return_td = {"QB": None, "RB": None, "WR": None, "TE": None, "K": None, "DEF": 8}

    # General
    points_position = {"QB": 10, "RB": 9, "WR": 9, "TE": 5, "K": 5, "DEF": 9}

    def __init__(self, data, position):
        def if_number(string):
            try:
                float(string)
                return float(string)
            except ValueError:
                return None

        # Passing
        if self.completions_position[position] is not None:
            self.completions = if_number(data[self.completions_position[position]])
        else:
            self.completions = None
        if self.attempts_position[position] is not None:
            self.attempts = if_number(data[self.attempts_position[position]])
        else:
            self.attempts = None
        if self.completion_percent_position[position] is not None:
            self.completion_percent = if_number(data[self.completion_percent_position[position]])
        else:
            self.completion_percent = None
        if self.passing_yards_position[position] is not None:
            self.passing_yards = if_number(data[self.passing_yards_position[position]])
        else:
            self.passing_yards = None
        if self.passing_td_position[position] is not None:
            self.passing_td = if_number(data[self.passing_td_position[position]])
        else:
            self.passing_td = None
        if self.interceptions_thrown_position[position] is not None:
            self.interceptions_thrown = if_number(data[self.interceptions_thrown_position[position]])
        else:
            self.interceptions_thrown = None

        # Rushing
        if self.rushing_attempts_position[position] is not None:
            self.rushing_attempts = if_number(data[self.rushing_attempts_position[position]])
        else:
            self.rushing_attempts = None
        if self.rushing_yards_position[position] is not None:
            self.rushing_yards = if_number(data[self.rushing_yards_position[position]])
        else:
            self.rushing_yards = None
        if self.rushing_avg_position[position] is not None:
            self.rushing_avg = if_number(data[self.rushing_avg_position[position]])
        else:
            self.rushing_avg = None
        if self.rushing_td_position[position] is not None:
            self.rushing_td = if_number(data[self.rushing_td_position[position]])
        else:
            self.rushing_td = None

        # Receiving
        if self.receiving_targets_position[position] is not None:
            self.receiving_targets = if_number(data[self.receiving_targets_position[position]])
        else:
            self.receiving_targets = None
        if self.receiving_receptions_position[position] is not None:
            self.receiving_receptions = if_number(data[self.receiving_receptions_position[position]])
        else:
            self.receiving_receptions = None
        if self.receiving_yards_position[position] is not None:
            self.receiving_yards = if_number(data[self.receiving_yards_position[position]])
        else:
            self.receiving_yards = None
        if self.receiving_avg_position[position] is not None:
            self.receiving_avg = if_number(data[self.receiving_avg_position[position]])
        else:
            self.receiving_avg = None
        if self.receiving_td_position[position] is not None:
            self.receiving_td = if_number(data[self.receiving_td_position[position]])
        else:
            self.receiving_td = None

        # Kicking
        if self.fg_make_position[position] is not None:
            self.fg_make = if_number(data[self.fg_make_position[position]])
        else:
            self.fg_make = None
        if self.fg_attempt_position[position] is not None:
            self.fg_attempt = if_number(data[self.fg_attempt_position[position]])
        else:
            self.fg_attempt = None
        if self.fg_percent_position[position] is not None:
            self.fg_percent = if_number(data[self.fg_percent_position[position]].replace("%", ""))
        else:
            self.fg_percent = None
        if self.ep_made_position[position] is not None:
            self.ep_made = if_number(data[self.ep_made_position[position]])
        else:
            self.ep_made = None
        if self.ep_attempt_position[position] is not None:
            self.ep_attempt = if_number(data[self.ep_attempt_position[position]])
        else:
            self.ep_attempt = None

        # Defense
        if self.sacks_position[position] is not None:
            self.sacks = if_number(data[self.sacks_position[position]])
        else:
            self.sacks = None
        if self.fumble_recovery_position[position] is not None:
            self.fumble_recovery = if_number(data[self.fumble_recovery_position[position]])
        else:
            self.fumble_recovery = None
        if self.interception_caught_position[position] is not None:
            self.interception_caught = if_number(data[self.interception_caught_position[position]])
        else:
            self.interception_caught = None
        if self.defensive_td_position[position] is not None:
            self.defensive_td = if_number(data[self.defensive_td_position[position]])
        else:
            self.defensive_td = None
        if self.points_allowed_position[position] is not None:
            self.points_allowed = if_number(data[self.points_allowed_position[position]])
        else:
            self.points_allowed = None
        if self.passing_yards_allowed_per_game_position[position] is not None:
            self.passing_yards_allowed_per_game =\
                if_number(data[self.passing_yards_allowed_per_game_position[position]])
        else:
            self.passing_yards_allowed_per_game = None
        if self.rushing_yards_allowed_per_game_position[position] is not None:
            self.rushing_yards_allowed_per_game =\
                if_number(data[self.rushing_yards_allowed_per_game_position[position]])
        else:
            self.rushing_yards_allowed_per_game = None
        if self.safeties_position[position] is not None:
            self.safeties = if_number(data[self.safeties_position[position]])
        else:
            self.safeties = None
        if self.kick_return_td[position] is not None:
            self.kick_return_td = if_number(data[self.kick_return_td[position]])
        else:
            self.kick_return_td = None

        # General
        self.points = if_number(data[self.points_position[position]])

    def __repr__(self):
        represent_self = "Score: " + str(self.points) + "\n"
        represent_self += "        Passing [ "
        if self.completions is not None:
            represent_self += "completions: " + str(self.completions) + ", "
        if self.attempts is not None:
            represent_self += "attempts: " + str(self.attempts) + ", "
        if self.completion_percent is not None:
            represent_self += "completion_percent: " + str(self.completion_percent) + ", "
        if self.passing_yards is not None:
            represent_self += "passing_yards: " + str(self.passing_yards) + ", "
        if self.passing_td is not None:
            represent_self += "passing_td: " + str(self.passing_td) + ", "
        if self.interceptions_thrown is not None:
            represent_self += "interceptions_thrown: " + str(self.interceptions_thrown) + ", "
        represent_self += "]\n"

        represent_self += "        Rushing [ "
        if self.rushing_attempts is not None:
            represent_self += "rushing_attempts: " + str(self.rushing_attempts) + ", "
        if self.rushing_yards is not None:
            represent_self += "rushing_yards: " + str(self.rushing_yards) + ", "
        if self.rushing_avg is not None:
            represent_self += "rushing_avg: " + str(self.rushing_avg) + ", "
        if self.rushing_td is not None:
            represent_self += "rushing_td: " + str(self.rushing_td) + ", "
        represent_self += "]\n"

        represent_self += "        Receiving [ "
        if self.receiving_targets is not None:
            represent_self += "receiving_targets: " + str(self.receiving_targets) + ", "
        if self.receiving_receptions is not None:
            represent_self += "receiving_receptions: " + str(self.receiving_receptions) + ", "
        if self.receiving_yards is not None:
            represent_self += "receiving_yards: " + str(self.receiving_yards) + ", "
        if self.receiving_avg is not None:
            represent_self += "receiving_avg: " + str(self.receiving_avg) + ", "
        if self.receiving_td is not None:
            represent_self += "receiving_td: " + str(self.receiving_td) + ", "
        represent_self += "]\n"

        represent_self += "        Kicking [ "
        if self.fg_make is not None:
            represent_self += "fg_make: " + str(self.fg_make) + ", "
        if self.fg_attempt is not None:
            represent_self += "fg_attempt: " + str(self.fg_attempt) + ", "
        if self.fg_percent is not None:
            represent_self += "fg_percent: " + str(self.fg_percent) + ", "
        if self.ep_made is not None:
            represent_self += "ep_made: " + str(self.ep_made) + ", "
        if self.ep_attempt is not None:
            represent_self += "ep_attempt: " + str(self.ep_attempt) + ", "
        represent_self += "]\n"

        represent_self += "        Defense [ "
        if self.sacks is not None:
            represent_self += "sacks: " + str(self.sacks) + ", "
        if self.fumble_recovery is not None:
            represent_self += "fumble_recovery: " + str(self.fumble_recovery) + ", "
        if self.interception_caught is not None:
            represent_self += "interception_caught: " + str(self.interception_caught) + ", "
        if self.defensive_td is not None:
            represent_self += "defensive_td: " + str(self.defensive_td) + ", "
        if self.points_allowed is not None:
            represent_self += "points_allowed: " + str(self.points_allowed) + ", "
        if self.passing_yards_allowed_per_game is not None:
            represent_self += "passing_yards_allowed_per_game: " + str(self.passing_yards_allowed_per_game) + ", "
        if self.rushing_yards_allowed_per_game is not None:
            represent_self += "rushing_yards_allowed_per_game: " + str(self.rushing_yards_allowed_per_game) + ", "
        if self.safeties is not None:
            represent_self += "safeties: " + str(self.safeties) + ", "
        if self.kick_return_td is not None:
            represent_self += "kick_return_td: " + str(self.kick_return_td) + ", "
        represent_self += "]\n"

        represent_self = represent_self.replace("        Passing [ ]\n", "")
        represent_self = represent_self.replace("        Rushing [ ]\n", "")
        represent_self = represent_self.replace("        Receiving [ ]\n", "")
        represent_self = represent_self.replace("        Kicking [ ]\n", "")
        represent_self = represent_self.replace("        Defense [ ]\n", "")
        represent_self = represent_self.replace(", ]", " ]")
        return represent_self


class PlayerSeasonStats(PlayerStats):
    def __init__(self, data, position):
        shift = 0
        if "(Projected)" in data:
            shift = 1
            self.games_played = None
            self.points_per_game = float(data[len(data) - 2]) / 16
        else:
            self.games_played = data[3]
            self.points_per_game = data[len(data) - 1]
        if "DEF" not in str(position):
            self.team = data[2 + shift]
        else:
            self.team = None  # todo, match up defense with team abbreviation
            shift -= 2
        if "K" in str(position):
            shift -= 1
        super(PlayerSeasonStats, self).__init__(data[5 + shift: -1], position)

    def __repr__(self):
        represent_self = "      "
        if self.team is not None:
            represent_self += "Team: " + str(self.team) + " "
        if self.games_played is not None:
            represent_self += "Games played: " + str(self.games_played) + " "
        represent_self += super(PlayerSeasonStats, self).__repr__()
        return represent_self


class PlayerWeeklyStats(PlayerStats):
    def __init__(self, data, position):
        super(PlayerWeeklyStats, self).__init__(data[5:], position)
        self.home_game = "@" in data[2]
        self.opponent = data[2].replace("@", "")
        self.team_won = "W" in data[3]
        self.team_score = data[4][:data[4].find("-")]
        self.opponent_score = data[4][data[4].find("-") + 1:]

    def __repr__(self):
        represent_self = "      H/A: "
        if self.home_game:
            represent_self += "Home"
        else:
            represent_self += "Away"
        represent_self += ", Opponent: " + self.opponent
        represent_self += ", Win?: " + str(self.team_won)
        represent_self += " " + str(self.team_score) + "-" + str(self.opponent_score) + ", "
        represent_self += super(PlayerWeeklyStats, self).__repr__()
        return represent_self


class PlayerCurrentSeason:
    def __init__(self, position, player_adp, file_content):
        self.position = position
        self.adp = player_adp
        self.weekly_scores = [0]*18

        found_season = False
        for line in file_content:
            if "season " + year in line:
                found_season = True
            elif found_season:
                if "season " in line:
                    break
                else:
                    def is_int(number):
                        try:
                            int(number)
                            return True
                        except ValueError:
                            return False
                    if is_int(line[9:11]):
                        self.weekly_scores[int(line[9:11]) - 1] = float(line[line.rfind(" ") + 1:])

    def get_week_score(self, week_number):
        return self.weekly_scores[int(week_number) - 1]


def new_imports(exclude):
    import_list = []
    import_count = 0
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        robot_import = Robot(name, obj, import_count)
        if inspect.ismodule(obj) and robot_import not in exclude:
            import_list.append(robot_import)
            import_count += 1
    return import_list


# Create a league of 12 robots
def simulate_league(debug_info):
    league = League()
    if debug_info:
        print(league)

        print("\nRunning league sim, draft order:")
    league.set_up(debug_info)

    for round_num in range(0, Team.size()):
        league.draft_round(round_num, debug_info)

    if debug_info:
        print("\nResults:")
    for league_week in range(0, weeks_in_season):
        if debug_statements:
            print(" Eval week " + str(league_week + 1))
        league.evaluate_week(league_week + 1)
    if debug_info:
        league.print_regular_season_results()

    league.run_playoffs(debug_info)


def run_many_leagues(number_of_leagues, debug_info):
    for _ in range(number_of_leagues):
        simulate_league(debug_info)
        # Try to better distribute our random by shuffling the list...
        random.shuffle(robots)


# Create list robots and fill in robots
print("\nImporting robot players...\n")
ignore_list = new_imports([])
# noinspection PyUnresolvedReferences
from robots import *
robot_list = new_imports(ignore_list)
print("Robots playing: " + str(robot_list) + "\n")
# noinspection PyUnresolvedReferences
from defaultrobots import *
fill_in_list = new_imports(ignore_list + robot_list)
print("Robots filling in: " + str(fill_in_list) + "\n")

# Set our 12 robots playing
count = 0
while count < league_size:
    if len(robot_list) > 0:
        # Add available robots first
        robots.append(robot_list[0])
        robot_list.pop(0)
    else:
        fill_in_robot = fill_in_list[(count - len(robot_list)) % len(fill_in_list)].copy()
        fill_in_robot.set_num(count)
        robots.append(fill_in_robot)
    count += 1

# Import player adp and history
with open("data/adp" + year + ".csv", 'rt') as adp_csv:
    adp_reader = csv.reader(adp_csv, delimiter=',', quotechar='|', skipinitialspace=True)
    adp = 1
    for row in adp_reader:
        player_name = row[0]
        player_team = row[1]
        player_position = row[2]
        player_list.append(Player(player_name, adp, player_position, player_team))
        player_file_path = "data/players/" + player_position + "/" + player_name + ".csv"
        if os.path.isfile(player_file_path):
            with open(player_file_path) as current_file:
                player_history.append(PlayerHistory(player_position, adp, current_file))
                current_file.seek(0, 0)
                players_current_season.append(PlayerCurrentSeason(player_position, adp, current_file))
        elif debug_statements:
            print("!! Missing player file: " + player_name + " !!")
        adp += 1

# Give the robots the information on players
for robot in robots:
    robot.set_info()

print("Our 12 robots playing:")
print(robots)
print("\nCrunching leagues...\n")
random.seed("rff seed")
cProfile.run('run_many_leagues(league_runs, debug_statements)')

for robot_ in robots:
    print(robot_.name + " made playoffs " + str(robot_.playoffs_percent()) + "%")
print()

for robot_ in robots:
    print(robot_.name + " won the league " + str(robot_.win_league_percent()) + "%")
