#!/usr/bin/python
import random

print("Hello from adpDrafter")
random.seed("seed123")

# If you check your AI against 11 ADP drafters, there are only 12 actual outcomes by drafting position.  To get a
# better idea of the proficiency of your AI, increase variance to allow for ADP drafters to select from the top X
# available players.  Set to 0, we will pick the highest ADP player.
variance = 3


def set_info(player_history_init):
    global player_history
    player_history = player_history_init


def draft_player(available_players, team):
    down_shift = random.randint(0, variance)
    for i in range(0, len(available_players) - down_shift):
        if team.is_position_open(player_history[available_players[i + down_shift]].position):
            return available_players[i + down_shift]
