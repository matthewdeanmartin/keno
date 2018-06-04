# coding=utf-8
"""
# TODO: This will haunt me until I write the tests.
"""

from keno.game_runner import GameRunner
def xxx_slow_game():
    """
    Set up to keep variables out of global namespace
    :return:
    """
    # 1/2 second game on my mac
    runner = GameRunner(max_ticket_price=50,
                        max_ticket_types=5000, # Almost all possible
                        max_plays_with_ticket_type=75,
                        max_loss=160, # double average per capita annual play in md
                        sufficient_winnings=2500,
                        max_generations=100) # 1 ticket type dominates by about 8
    runner.run()

def test_fast_game():
    """
    Set up to keep variables out of global namespace
    :return:
    """
    # 1/2 second game on my mac
    runner = GameRunner(max_ticket_price=500,
                        max_ticket_types=500,
                        max_plays_with_ticket_type=50,
                        max_loss=25,
                        sufficient_winnings=25,
                        max_generations=2)
    runner.run()