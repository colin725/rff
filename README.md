# Robot Fantasy Football (working title) readme

## Getting started

Run LeagueRunner.py to simulate fantasy football leagues.
robots/Robot1.py is the example class that you can add your own logic to (and rename)

The idea for the first season is that the robots only handle drafting, so you only need to implement the one method: draft_players
The method takes in a list of available players and your currently drafted team.
Players are sorted by average draft position, you can think of their adp as an identifier to replace name.
Before any leagues are ran the AI is passed a list of player stats and projections, also listed by adp.
Use these stats, projections, and player's average draft position to determine your optimal draft selection.

To evaluate run LeagueRunner.py and the output indicates the percent of playoffs made and percent of leagues won.
The league runner fills in the other 

Feel free to make any improvements to the code (while avoiding breaking existing APIs) or documentation and submit them.

## Entering this season

To enter your AI just implement the drafting AI and submit your .py file
For the first season it would be great to open source the AIs, but we should be able to work with .pyc if needed.

## Details of simulated leagues

* League size is set to 12
* Scoring is the standard found at sites like ESPN, but with 0.5 points per reception
* There are 12 regular season weeks
* The top four teams by wins and then points scored go to playoffs
* No divisions
* Playoff match-ups are 2 weeks long
* Decimal scoring is used

## Data

Yearly data is given for all years that a players has played
Weekly data is given for the past 3 seasons
Make sure to check for None being returned anywhere if there is no data for a player

Uncomment the block in robot1.py to see the data printed out for one player of each position.

## API

Player stats passed as a list of PlayerHistory (player_history_init)

PlayerHistory
    .position  => string in {"QB", "RB", "WR", "TE", "K", "DEF"}
    .adp
    .current_year
    .yearly_data => PlayerYear

PlayerYear
    .season_totals => PlayerSeasonStats
    .weekly_data => PlayerWeeklyStats

PlayerSeasonStats extends PlayerStats
    .games_played
    .points_per_game
    .team

PlayerWeeklyStats extends PlayerStats
    .home_game => true/false
    .opponent => string
    .team_won => true/false
    .team_score
    .opponent_score

PlayerStats
    .points

    .completions
    .attempts
    .completion_percent
    .passing_yards
    .passing_td
    .interceptions_thrown

    .rushing_attempts
    .rushing_yards
    .rushing_avg
    .rushing_td

    .receiving_targets
    .receiving_receptions
    .receiving_yards
    .receiving_avg
    .receiving_td

    .fg_make
    .fg_attempt
    .fg_percent
    .ep_made
    .ep_attempt

    .sacks
    .fumble_recovery
    .interception_caught
    .defensive_td
    .points_allowed
    .passing_yards_allowed_per_game
    .rushing_yards_allowed_per_game
    .safeties
    .kick_return_td

And again any of the above will return None if there wasn't data for it.

(See PlayerClasses.py to dig in further)

## Rules

* No player names, the idea of creating these AIs is to evaluate players more anonymously based on data which should allow crossover from year to year
* No random so that we can get consistent results

## Limitations

* No in season management means no injury subs, no benches, no waivers, etc