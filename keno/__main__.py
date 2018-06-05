# coding=utf-8
"""
Code to allow launching module directly with python -m keno
"""
from keno.game_runner import GameRunner, Strategy, EvolutionParameters


def run():
    """
    Set up to keep variables out of global namespace
    :return:
    """
    runner = GameRunner(Strategy(max_ticket_price=100,
                        max_plays_with_ticket_type=200,
                        max_loss=500,
                        sufficient_winnings=5000),
                        EvolutionParameters(max_generations=8,
                                            mutation_percent=.25,
                                            fitness_bonus=3,
                                            max_ticket_types=5000))
    runner.run()
run()
