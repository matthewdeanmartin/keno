# coding=utf-8
"""
Exercise player code
"""

from keno.player import Player
from keno.ticket import Ticket


def test_player():
    """
    Basic call
    """
    for i in range(0, 10):
        player = Player(max_loss=160, stop_at=2000, max_tickets=365)
        ticket = Ticket()
        ticket.randomize_ticket()
        player.ticket = ticket

        player.go()
        print("winning: " + str(player.history))
        print("bank: " + str(player.history_running_bank))


def test_player_str():
    """
    Basic call
    """
    player = Player(100, 100, 100)

    assert "" != str(player)
