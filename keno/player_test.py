# coding=utf-8
"""
Exercise player code
"""

from keno.player import Player


def test_player():
    """
    Basic call
    """
    player = Player(100, 100, 100)
    player.go()


def test_player_str():
    """
    Basic call
    """
    player = Player(100, 100, 100)
    assert "" != str(player)
