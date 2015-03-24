#!/usr/bin/python

print("hello from robot2")


def draft_player(available_players, team):
    for player in available_players:
        if team.is_position_open(player.position):
            return player