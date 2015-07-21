
class PlayerHistory:
    def __init__(self, position, self_adp, file_content, year):
        self.position = position
        self.adp = self_adp
        self.yearly_data = {}
        self.current_year = year

        def is_int(string):
            try:
                int(string)
                return True
            except ValueError:
                return False

        year_found = None
        for line in file_content:
            if "season " in line:
                if is_int(line.split()[1]):
                    if "(Projected)" in line:
                        if int(line.split()[1]) == year:
                            year_found = "Projected"
                        else:
                            year_found = None
                    else:
                        year_found = int(line.split()[1])
                    if year_found is not None:
                        if year_found == "Projected" or year_found < year:
                            self.yearly_data[year_found] = PlayerYear(position)
                            self.yearly_data[year_found].add_season_totals(line.split())
            else:
                if not line.isspace():
                    if is_int(line.split()[1]) and year_found in self.yearly_data:
                        week_number = int(line.split()[1])
                        self.yearly_data[year_found].add_week_data(week_number, line.split())

    def __repr__(self):
        represent_self = "PlayerHistory for Player " + str(self.adp) + ", position: " + self.position + "\n"
        if "Projected" in self.yearly_data:
            represent_self += "    Projected year (" + str(self.current_year) + ") " + str(self.yearly_data["Projected"]) + "\n"
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
    def __init__(self, position, player_adp, file_content, year):
        self.position = position
        self.adp = player_adp
        self.weekly_scores = [0]*18

        found_season = False
        for line in file_content:
            if "season " + str(year) in line and "(Projected)" not in line:
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