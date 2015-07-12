#!/usr/bin/python

print("hello from robot1")

# This is where you are free to implement your own AI drafter.  To start out with we have a basic drafter taking the
# player by draft position, but you can adjust the down_shift to have it pick players X spots back from the top
# average draft position and see how it changes the results.
down_shift = 0


def set_info(player_list_init):
    global player_list
    player_list = player_list_init


def draft_player(available_players, team):
    for i in range(0, len(available_players) - down_shift):
        if team.is_position_open(player_list[available_players[i + down_shift]].position):
            return available_players[i + down_shift]