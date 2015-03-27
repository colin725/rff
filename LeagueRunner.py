#!/usr/bin/python
import sys
import inspect
import random
import csv
import cProfile

league_size = 12
weeks_in_season = 16
year = "2014"

robots = []
player_list = []
player_names = []

weekly_scores = {}


class Robot:
    def __init__(self, name, obj, num):
        self.name = name
        self.obj = obj
        self.num = num
        self.playoff_appearances = 0
        self.average_position = 0
        self.leagues_played = 0

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return str(self.name)

    def copy(self):
        return Robot(self.name, self.obj, self.num)

    def set_num(self, num):
        self.num = num

    def draft_player(self, available_players, team):
        return self.obj.draft_player(available_players, team)

    def made_playoffs(self):
        self.playoff_appearances += 1

    def position_played(self, draft_position):
        self.average_position = (self.average_position * self.leagues_played + draft_position)\
            / (self.leagues_played + 1)
        self.leagues_played += 1


class League:
    def __init__(self):
        self.available_players = player_list.copy()
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
        for robot in self.robots:
            self.teams[robot.num] = Team()

    # Complete a single round of drafting
    def draft_round(self, drafting_round, debug_info):
        this_round = []

        def select_player(robot_selector):
            selected = robot_selector.draft_player(self.available_players, self.teams[robot_selector.num])
            self.available_players.remove(selected)
            self.teams[robot_selector.num].add_player(selected)
            return selected

        if debug_info:
            print("\nDrafting round " + str(drafting_round + 1) + ": ")
        if not self.snake_round:
            for robot in self.robots:
                this_round.append(select_player(robot))
            self.snake_round = True
        else:
            for robot in reversed(self.robots):
                this_round.append(select_player(robot))
            self.snake_round = False
        if debug_info:
            print("    " + str(this_round))

    # evaluate a week
    def evaluate_week(self, week_number):
        # Find match-ups for the week and evaluate each
        # Made for a 12 man league specifically to make match-ups even, may or may not work for other sizes
        # It might have been slightly ridiculous to codify this, but for a 12 man league it works out to this:
        #
        #    Opponents over the 16 weeks (last 3 weeks have a slightly different pattern)
        # Team 1: 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  7, 12, 11, 10,  9
        # Team 2: 11, 10,  9,  8,  7,  6,  5,  4,  3,  8,  1, 12, 11, 10,  9,  5
        # Team 3: 10,  9,  8,  7,  6,  5,  4,  9,  2,  1, 12, 11, 10,  6,  8,  7
        # Team 4:  9,  8,  7,  6,  5, 10,  3,  2,  1, 12, 11, 10,  9,  8,  7,  6
        # Team 5:  8,  7,  6, 11,  4,  3,  2,  1, 12, 11, 10,  9,  8,  7,  6,  2
        # Team 6:  7, 12,  5,  4,  3,  2,  1, 12, 11, 10,  9,  8,  7,  3,  5,  4
        # Team 7:  6,  5,  4,  3,  2,  1, 12, 11, 10,  9,  8,  1,  6,  5,  4,  3
        # Team 8:  5,  4,  3,  2,  1, 12, 11, 10,  9,  2,  7,  6,  5,  4,  3, 11
        # Team 9:  4,  3,  2,  1, 12, 11, 10,  3,  8,  7,  6,  5,  4, 12,  2,  1
        # Team 10: 3,  2,  1, 12, 11,  4,  9,  8,  7,  6,  5,  4,  3,  2,  1, 12
        # Team 11: 2,  1, 12,  5, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1, 12,  8
        # Team 12: 1,  6, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  9, 11, 10

        evaluated = []
        for i in range(0, int(len(self.teams) / 2)):
            for j in range(0, int(len(self.teams) / 2)):
                if (i + j) not in evaluated:
                    opponent_number = (league_size - (((i + j) + week_number) % league_size)) % league_size
                    if week_number <= league_size + 1:
                        # Collision (scheduled against yourself) for weeks 1 through [league_size + 1]
                        if opponent_number == i + j:
                            opponent_number += int(league_size / 2)
                    elif week_number % 2 == 0:
                        # Create new collision scheduling (see weeks 14-16 above) to avoid playing an opponent 3 times
                        if ((i + j + 1) + int((week_number - (league_size + 1)) / 2)) % 3 == 0:
                            opponent_number = i + j + 3

                    # print(str(i + j + 1) + " vs " + str(opponent_number + 1))
                    evaluated.append(i + j)
                    evaluated.append(opponent_number)

                    # Match up chosen, evaluate it...
                    team1_total = self.teams[self.robots[i+j].num].eval(week_number)
                    team2_total = self.teams[self.robots[opponent_number].num].eval(week_number)
                    if team1_total > team2_total:
                        self.teams[self.robots[i+j].num].wins += 1
                    else:
                        self.teams[self.robots[opponent_number].num].wins += 1
                    break

    def run_playoffs(self, debug_info):
        # TODO tie breakers!!!!!
        playoff_robots = []
        for i in range(0, len(self.robots)):
            unranked_robot = self.robots[i]
            for j in range(0, 4):
                if len(playoff_robots) <= j:
                    playoff_robots.append(unranked_robot)
                    break
                elif self.teams[unranked_robot.num].wins > self.teams[playoff_robots[j].num].wins:
                    temp_robot = playoff_robots[j]
                    playoff_robots[j] = unranked_robot
                    unranked_robot = temp_robot
        if debug_info:
            print("Playoff teams:")
        for i in range(0, 4):
            playoff_robots[i].made_playoffs()
            if debug_info:
                print("#" + str(i) + ": " + playoff_robots[i].name + " (" + str(playoff_robots[i].num) + ")" +
                      " with record " + str(self.teams[playoff_robots[i].num].wins) + "-" +
                      str(weeks_in_season - self.teams[playoff_robots[i].num].wins))
        if debug_info:
            print()

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
        self.player_slots = Team.starting_slots.copy()
        self.players = []
        self.wins = 0

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
                                flex = player_names[player.adp - 1]
                                break
                            rb_found += 1
                        elif repr_position == "WR":
                            if wr_found == Team.starting_slots["WR"]:
                                flex = player_names[player.adp - 1]
                                break
                            wr_found += 1
                        elif repr_position == "TE":
                            if te_found == Team.starting_slots["TE"]:
                                flex = player_names[player.adp - 1]
                                break
                            te_found += 1
                        repr_string += "  " + player_names[player.adp - 1] + "\n"
        repr_string += "Flex:\n  " + flex + "\n"
        repr_string += "\n"
        return repr_string

    def available_spots(self, available_position):
        return self.player_slots[available_position]

    def add_player(self, player):
        self.players.append(player)
        if self.player_slots[player.position] == 0:
            if self.player_slots["FLEX"] > 0 and player.position in ["RB", "WR", "TE"]:
                self.player_slots["FLEX"] -= 1
            else:
                raise ValueError("A " + str(player.position) + " was drafted when the team was already full.")
        else:
            self.player_slots[player.position] -= 1

    def is_position_open(self, position_questioned):
        if self.player_slots[position_questioned] > 0:
            return True
        elif self.player_slots["FLEX"] > 0 and position_questioned in ["RB", "WR", "TE"]:
            return True
        else:
            return False

    def eval(self, eval_week):
        total = 0
        for player in self.players:
            total += int(weekly_scores.get(player.position + player_names[player.adp - 1] + str(eval_week), 0))
        return total

    @staticmethod
    def size():
        size = 0
        for slots in Team.starting_slots.values():
            size += slots
        return size


class Player:
    def __init__(self, player_adp, player_position, team):
        self.adp = player_adp
        self.position = player_position
        self.team = team

    def __repr__(self):
        return str(player_names[self.adp - 1])


def new_imports(exclude):
    import_list = []
    import_count = 0
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        robot = Robot(name, obj, import_count)
        if inspect.ismodule(obj) and robot not in exclude:
            import_list.append(robot)
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
print("\nImporting robot players...\n\n")
ignore_list = new_imports([])
from robots import *
robot_list = new_imports(ignore_list)
print("Robots playing: " + str(robot_list) + "\n\n")
from defaultrobots import *
fill_in_list = new_imports(ignore_list + robot_list)
print("Robots filling in: " + str(fill_in_list) + "\n\n")

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


# Import player adp and weekly scores
with open("data/players/" + year + "/adp.csv", 'rt') as adp_csv:
    adp_reader = csv.reader(adp_csv, delimiter=',', quotechar='|', skipinitialspace=True)
    adp = 1
    for row in adp_reader:
        player_list.append(Player(adp, row[2], row[1]))
        player_names.append(row[0])
        adp += 1

for week in range(0, weeks_in_season):
    for position in Team.starting_slots.keys():
        if position != "FLEX":
            weekly_score_file = "data/players/" + year + "/week" + str(week + 1) + "/" + position + ".csv"
            for player_score in csv.reader(open(weekly_score_file, 'rt'),
                                           delimiter=',', quotechar='|', skipinitialspace=True):
                weekly_scores[position + player_score[0] + str(week)] = player_score[2]


league_runs = 10000
debug_statements = False
random.seed("rff seed")
cProfile.run('run_many_leagues(league_runs, debug_statements)')

for robot_ in robots:
    print(robot_.name + " made playoffs " + str(robot_.playoff_appearances / league_runs) + "%")
    if debug_statements:
        print("            avg pos: " + str(robot_.average_position))