#!/usr/bin/python

print("hello from robot1")

# This is where you are free to implement your own AI drafter.  To start out with we have a basic drafter taking the
# player by draft position, but you can adjust the down_shift to have it pick players X spots back from the top
# average draft position and see how it changes the results.
down_shift = 0


def set_info(player_history_init, year):
    global player_history
    global current_year
    player_history = player_history_init
    current_year = year

    # ##   To help visualize the data given on player history uncomment this block to see it printed out
    # ##   once for each position.
    #
    # first_pos = {"QB": True, "RB": True, "WR": True, "TE": True, "K": True, "DEF": True}
    # for player in player_history:
    #     if first_pos[player.position]:
    #         print(str(player))
    #         first_pos[player.position] = False


def draft_player(available_players, team):
    global current_year
    for i in range(0, len(available_players) - down_shift):

        # Access the players projections as well as past yearly and weekly stats to make your decision
        player = player_history[available_players[i]]
        projection = player.yearly_data["Projected"].season_totals
        last_season = player.yearly_data[current_year - 1].season_totals

        if team.is_position_open(player_history[available_players[i + down_shift]].position):
            return available_players[i + down_shift]
