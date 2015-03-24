#!/usr/bin/python
import sys
import inspect
import random
import csv

league_size = 12
weeks_in_season = 16
player_list = []
player_names = []
year = "2014"

weekly_scores = {}


class Robot:
    def __init__(self, name, obj, num):
        self.name = name
        self.obj = obj
        self.num = num

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


class League:
    teams = {}
    robots = []
    available_players = []
    snake_round = False

    def __init__(self, robots, players):
        self.robots = robots
        self.available_players = players

    def __eq__(self, other):
        return self.robots == other.robots

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

    def set_up(self):
        ordered_robots = []

        # Set draft order
        while len(self.robots) > 0:
            next_team = int(random.random() * (len(self.robots) - 1))
            ordered_robots.append(self.robots[next_team])
            self.robots.pop(next_team)
        self.robots = ordered_robots
        print(self.robots)

        # Create empty teams
        for robot in self.robots:
            self.teams[robot.num] = Team()

    # Complete a single round of drafting
    def draft_round(self, drafting_round):
        this_round = []

        def select_player(robot_selector):
            selected = robot_selector.draft_player(self.available_players, self.teams[robot_selector.num])
            self.available_players.remove(selected)
            self.teams[robot_selector.num].add_player(selected)
            return selected

        print("\nDrafting round " + str(drafting_round + 1) + ": ")
        if not self.snake_round:
            for robot in self.robots:
                this_round.append(select_player(robot))
            self.snake_round = True
        else:
            for robot in reversed(self.robots):
                this_round.append(select_player(robot))
            self.snake_round = False
        print("    " + str(this_round))

    # evaluate a week
    def evaluate_week(self, week_number):
        # Find match-ups for the week and evaluate each
        # Made for a 12 man league specifically to make match-ups even, may or may not work for other sizes
        evaluated = []
        for i in range(0, int(len(self.teams) / 2)):
            for j in range(0, int(len(self.teams) / 2)):
                if (i + j) not in evaluated:
                    opponent_number = (league_size - (((i + j) + week_number) % league_size)) % league_size
                    if week_number <= league_size + 1:
                        if opponent_number == i + j:
                            opponent_number += int(league_size / 2)
                    elif week_number % 2 == 0:
                        # Create new collision scheduling to avoid playing an opponent 3 times
                        if ((i + j + 1) + int((week_number - (league_size + 1)) / 2)) % 3 == 0:
                            opponent_number = i + j + 3

                    # print(str(i + j + 1) + " vs " + str(opponent_number + 1))
                    evaluated.append(i + j)
                    evaluated.append(opponent_number)

                    # Match up chosen, evaluate it...
                    team1_total = self.teams[i+j].eval(week_number)
                    team2_total = self.teams[opponent_number].eval(week_number)
                    if team1_total > team2_total:
                        self.teams[i+j].wins += 1
                    else:
                        self.teams[opponent_number].wins += 1
                    break

    def print_results(self):
        for i in range(0, len(self.teams)):
            print(str(i + 1) + ": " + self.robots[i].name + "   " + str(self.teams[i].wins) + "-" + str(weeks_in_season - self.teams[i].wins))


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
        for position in Team.starting_slots.keys():
            if not position == "FLEX":
                repr_string += position + ": \n"
                for player in self.players:
                    if player.position == position:
                        if position == "RB":
                            if rb_found == Team.starting_slots["RB"]:
                                flex = player_names[player.adp - 1]
                                break
                            rb_found += 1
                        elif position == "WR":
                            if wr_found == Team.starting_slots["WR"]:
                                flex = player_names[player.adp - 1]
                                break
                            wr_found += 1
                        elif position == "TE":
                            if te_found == Team.starting_slots["TE"]:
                                flex = player_names[player.adp - 1]
                                break
                            te_found += 1
                        repr_string += "  " + player_names[player.adp - 1] + "\n"
        repr_string += "Flex:\n  " + flex + "\n"
        repr_string += "\n"
        return repr_string

    def available_spots(self, position):
        return self.player_slots[position]

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
            for possible_match in csv.reader(open(weekly_scores[player.position + str(eval_week - 1)], 'rt'),
                                             delimiter=',', quotechar='|', skipinitialspace=True):
                if possible_match[0] == player_names[player.adp - 1]:
                    total += int(possible_match[2])
                    break
        return total

    @staticmethod
    def size():
        size = 0
        for slots in Team.starting_slots.values():
            size += slots
        return size


class Player:
    def __init__(self, adp, position, team):
        self.adp = adp
        self.position = position
        self.team = team

    def __repr__(self):
        return str(player_names[self.adp - 1])


def new_imports(exclude):
    import_list = []
    count = 0
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        robot = Robot(name, obj, count)
        if inspect.ismodule(obj) and robot not in exclude:
            import_list.append(robot)
            count += 1
    return import_list


# Create list robots and fill in robots
print("\nImporting robot players...\n\n")
ignore_list = new_imports([])
from robots import *
robot_list = new_imports(ignore_list)
print("Robots playing: " + str(robot_list) + "\n\n")
from defaultrobots import *
fill_in_list = new_imports(ignore_list + robot_list)
print("Robots filling in: " + str(fill_in_list) + "\n\n")


# Create a league of 12 robots
def create_league():
    robots = []
    extras = 0

    # Set robots playing
    count = 0
    while count < league_size:
        if len(robot_list) > 0:
            # Add available robots first
            robots.append(robot_list[0])
            robot_list.pop(0)
        else:
            fill_in_robot = fill_in_list[extras % len(fill_in_list)].copy()
            fill_in_robot.set_num(count)
            robots.append(fill_in_robot)
            extras += 1
        count += 1

    return League(robots, player_list)


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
            weekly_scores[position + str(week)] =\
                "data/players/" + year + "/week" + str(week + 1) + "/" + position + ".csv"

# PLayers imported, create a league #
league = create_league()
print(league)

print("\nRunning league sim, draft order:")
random.seed(0)
league.set_up()

for round_num in range(0, Team.size()):
    league.draft_round(round_num)

# print("\nAnd final teams:")
# print(league.teams_to_string())

print("\nResults:")
for league_week in range(0, weeks_in_season):
    league.evaluate_week(league_week + 1)

league.print_results()