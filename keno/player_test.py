# coding=utf-8
"""
Exercise player code
"""
from keno.game_runner import Strategy
from keno.player import Player
from keno.ticket import Ticket

def test_three_six_ticket():
    """
    Basic call
    """
    plays = 0
    gg = 0
    for _ in range(0, 1000):
        player = Player(Strategy(max_ticket_price=100,
                                 max_loss=160,
                                 sufficient_winnings=2000,
                                 max_plays_with_ticket_type=365))
        ticket = Ticket()
        ticket.randomize_ticket()
        ticket.bet = 3
        ticket.bonus = False
        ticket.super_bonus = False
        ticket.spots = 6
        ticket.pick()
        ticket.games = 10
        ticket.state = "MD"
        player.ticket = ticket

        player.go()
        print("winning: " + str(player.history))
        print("bank: " + str(player.history_running_bank))
        if player.good_game():
            gg +=1
        plays +=1
    print("Percent time good game")
    print(gg/plays)
def test_player():
    """
    Basic call
    """
    for i in range(0, 10):
        player = Player(Strategy(max_ticket_price=100,
                                 max_loss=160,
                                 sufficient_winnings=2000,
                                 max_plays_with_ticket_type=365))
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
    player = Player(Strategy(max_ticket_price=100,
                                 max_loss=160,
                                 sufficient_winnings=2000,
                                 max_plays_with_ticket_type=365))

    assert str(player) != ""
