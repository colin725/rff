
class TeamYear:
    def __init__(self, head_coach, bye_week):
        self.head_coach = head_coach
        self.bye_week = bye_week


class Team:
    def __init__(self):
        self.years = {}

    def set_year(self, year, team_year):
        self.years[year] = team_year

    def get_year(self, year):
        return self.years[year]


class TeamData:
    teams = {}

    @staticmethod
    def get_team_data(team, year):
        return TeamData.teams[team].get_year(year)

    # ARI
    teams["ARI"] = Team()
    teams["ARI"].set_year(2015, TeamYear("Bruce Arians", 9))
    teams["ARI"].set_year(2014, TeamYear("Bruce Arians", 4))
    teams["ARI"].set_year(2013, TeamYear("Bruce Arians", 9))

    # ATL
    teams["ATL"] = Team()
    teams["ATL"].set_year(2015, TeamYear("Dan Quinn", 10))
    teams["ATL"].set_year(2014, TeamYear("Mike Smith", 9))
    teams["ATL"].set_year(2013, TeamYear("Mike Smith", 6))

    # BAL
    teams["BAL"] = Team()
    teams["BAL"].set_year(2015, TeamYear("John Harbaugh", 9))
    teams["BAL"].set_year(2014, TeamYear("John Harbaugh", 11))
    teams["BAL"].set_year(2013, TeamYear("John Harbaugh", 8))

    # BUF
    teams["BUF"] = Team()
    teams["BUF"].set_year(2015, TeamYear("Rex Ryan", 8))
    teams["BUF"].set_year(2014, TeamYear("Doug Maronne", 9))
    teams["BUF"].set_year(2013, TeamYear("Doug Maronne", 12))

    # CAR
    teams["CAR"] = Team()
    teams["CAR"].set_year(2015, TeamYear("Ron Rivera", 5))
    teams["CAR"].set_year(2014, TeamYear("Ron Rivera", 12))
    teams["CAR"].set_year(2013, TeamYear("Ron Rivera", 4))

    # CHI
    teams["CHI"] = Team()
    teams["CHI"].set_year(2015, TeamYear("John Fox", 7))
    teams["CHI"].set_year(2014, TeamYear("Marc Trestman", 9))
    teams["CHI"].set_year(2013, TeamYear("Marc Trestman", 8))

    # CIN
    teams["CIN"] = Team()
    teams["CIN"].set_year(2015, TeamYear("Marvin Lewis", 7))
    teams["CIN"].set_year(2014, TeamYear("Marvin Lewis", 4))
    teams["CIN"].set_year(2013, TeamYear("Marvin Lewis", 12))

    # CLE
    teams["CLE"] = Team()
    teams["CLE"].set_year(2015, TeamYear("Mike Pettine", 11))
    teams["CLE"].set_year(2014, TeamYear("Mike Pettine", 4))
    teams["CLE"].set_year(2013, TeamYear("Rob Chudzinski", 10))

    # DAL
    teams["DAL"] = Team()
    teams["DAL"].set_year(2015, TeamYear("Jason Garrett", 6))
    teams["DAL"].set_year(2014, TeamYear("Jason Garrett", 11))
    teams["DAL"].set_year(2013, TeamYear("Jason Garrett", 11))

    # DEN
    teams["DEN"] = Team()
    teams["DEN"].set_year(2015, TeamYear("Gary Kubiak", 7))
    teams["DEN"].set_year(2014, TeamYear("John Fox", 4))
    teams["DEN"].set_year(2013, TeamYear("John Fox", 9))

    # DET
    teams["DET"] = Team()
    teams["DET"].set_year(2015, TeamYear("Jim Caldwell", 9))
    teams["DET"].set_year(2014, TeamYear("Jim Caldwell", 9))
    teams["DET"].set_year(2013, TeamYear("Jim Schwartz", 9))

    # GB
    teams["GB"] = Team()
    teams["GB"].set_year(2015, TeamYear("Mike McCarthy", 7))
    teams["GB"].set_year(2014, TeamYear("Mike McCarthy", 9))
    teams["GB"].set_year(2013, TeamYear("Mike McCarthy", 4))

    # HOU
    teams["HOU"] = Team()
    teams["HOU"].set_year(2015, TeamYear("Bill O'Brien", 9))
    teams["HOU"].set_year(2014, TeamYear("Bill O'Brien", 10))
    teams["HOU"].set_year(2013, TeamYear("Gary Kubiak ", 8))

    # IND
    teams["IND"] = Team()
    teams["IND"].set_year(2015, TeamYear("Chuck Pagano", 10))
    teams["IND"].set_year(2014, TeamYear("Chuck Pagano", 10))
    teams["IND"].set_year(2013, TeamYear("Chuck Pagano", 8))

    # JAC
    teams["JAC"] = Team()
    teams["JAC"].set_year(2015, TeamYear("Gus Bradley", 8))
    teams["JAC"].set_year(2014, TeamYear("Gus Bradley", 11))
    teams["JAC"].set_year(2013, TeamYear("Gus Bradley", 9))

    # KC
    teams["KC"] = Team()
    teams["KC"].set_year(2015, TeamYear("Andy Reid", 9))
    teams["KC"].set_year(2014, TeamYear("Andy Reid", 6))
    teams["KC"].set_year(2013, TeamYear("Andy Reid", 10))

    # MIA
    teams["MIA"] = Team()
    teams["MIA"].set_year(2015, TeamYear("Joe Philbin", 5))
    teams["MIA"].set_year(2014, TeamYear("Joe Philbin", 5))
    teams["MIA"].set_year(2013, TeamYear("Joe Philbin", 6))

    # MIN
    teams["MIN"] = Team()
    teams["MIN"].set_year(2015, TeamYear("Mike Zimmer", 5))
    teams["MIN"].set_year(2014, TeamYear("Mike Zimmer", 10))
    teams["MIN"].set_year(2013, TeamYear("Leslie Frazier", 5))

    # NE
    teams["NE"] = Team()
    teams["NE"].set_year(2015, TeamYear("Bill Belichick", 4))
    teams["NE"].set_year(2014, TeamYear("Bill Belichick", 10))
    teams["NE"].set_year(2013, TeamYear("Bill Belichick", 10))

    # NO
    teams["NO"] = Team()
    teams["NO"].set_year(2015, TeamYear("Sean Payton", 11))
    teams["NO"].set_year(2014, TeamYear("Sean Payton", 6))
    teams["NO"].set_year(2013, TeamYear("Sean Payton", 7))

    # NYG
    teams["NYG"] = Team()
    teams["NYG"].set_year(2015, TeamYear("Tom Coughlin", 11))
    teams["NYG"].set_year(2014, TeamYear("Tom Coughlin", 8))
    teams["NYG"].set_year(2013, TeamYear("Tom Coughlin", 9))

    # NYJ
    teams["NYJ"] = Team()
    teams["NYJ"].set_year(2015, TeamYear("Todd Bowles", 5))
    teams["NYJ"].set_year(2014, TeamYear("Rex Ryan", 11))
    teams["NYJ"].set_year(2013, TeamYear("Rex Ryan", 10))

    # OAK
    teams["OAK"] = Team()
    teams["OAK"].set_year(2015, TeamYear("Jack Del Rio", 6))
    teams["OAK"].set_year(2014, TeamYear("Dennis Allen", 5))
    teams["OAK"].set_year(2013, TeamYear("Dennis Allen", 7))

    # PHI
    teams["PHI"] = Team()
    teams["PHI"].set_year(2015, TeamYear("Chip Kelly", 8))
    teams["PHI"].set_year(2014, TeamYear("Chip Kelly", 7))
    teams["PHI"].set_year(2013, TeamYear("Chip Kelly", 12))

    # PIT
    teams["PIT"] = Team()
    teams["PIT"].set_year(2015, TeamYear("Mike Tomlin", 11))
    teams["PIT"].set_year(2014, TeamYear("Mike Tomlin", 12))
    teams["PIT"].set_year(2013, TeamYear("Mike Tomlin", 5))

    # SD
    teams["SD"] = Team()
    teams["SD"].set_year(2015, TeamYear("Mike McCoy", 10))
    teams["SD"].set_year(2014, TeamYear("Mike McCoy", 10))
    teams["SD"].set_year(2013, TeamYear("Mike McCoy", 8))

    # SF
    teams["SF"] = Team()
    teams["SF"].set_year(2015, TeamYear("Jim Tomsula", 10))
    teams["SF"].set_year(2014, TeamYear("Jim Harbaugh", 8))
    teams["SF"].set_year(2013, TeamYear("Jim Harbaugh", 9))

    # SEA
    teams["SEA"] = Team()
    teams["SEA"].set_year(2015, TeamYear("Pete Carroll", 9))
    teams["SEA"].set_year(2014, TeamYear("Pete Carroll", 4))
    teams["SEA"].set_year(2013, TeamYear("Pete Carroll", 12))

    # STL
    teams["STL"] = Team()
    teams["STL"].set_year(2015, TeamYear("Jeff Fisher", 6))
    teams["STL"].set_year(2014, TeamYear("Jeff Fisher", 4))
    teams["STL"].set_year(2013, TeamYear("Jeff Fisher", 11))

    # TB
    teams["TB"] = Team()
    teams["TB"].set_year(2015, TeamYear("Lovie Smith", 6))
    teams["TB"].set_year(2014, TeamYear("Lovie Smith", 7))
    teams["TB"].set_year(2013, TeamYear("Greg Schiano", 5))

    # TEN
    teams["TEN"] = Team()
    teams["TEN"].set_year(2015, TeamYear("Ken Whisenhunt", 4))
    teams["TEN"].set_year(2014, TeamYear("Ken Whisenhunt", 9))
    teams["TEN"].set_year(2013, TeamYear("Mike Munchak", 8))

    # WAS
    teams["WAS"] = Team()
    teams["WAS"].set_year(2015, TeamYear("Jay Gruden", 8))
    teams["WAS"].set_year(2014, TeamYear("Jay Gruden", 10))
    teams["WAS"].set_year(2013, TeamYear("Mike Shanahan", 5))
