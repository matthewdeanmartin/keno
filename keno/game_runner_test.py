# coding=utf-8
"""
# TODO: This will haunt me until I write the tests.
"""

from keno.game_runner import GameRunner
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