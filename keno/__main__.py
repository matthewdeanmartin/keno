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
                        max_ticket_types=1050,
                        max_plays_with_ticket_type=365,
                        max_loss=2500,
                        sufficient_winnings=2500,
                        max_generations=8)
    runner.run()
run()
