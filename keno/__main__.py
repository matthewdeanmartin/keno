# coding=utf-8
"""
Code to allow launching module directly with python -m keno
"""
from keno.game_runner import GameRunner
def run():
    """
    Set up to keep variables out of global namespace
    :return:
    """
    runner = GameRunner(max_ticket_price=50,
                        max_ticket_types=5000,
                        max_plays_with_ticket_type=200,
                        max_loss=5000,
                        sufficient_winnings=10000,
                        max_generations=4)
    runner.run()
run()
