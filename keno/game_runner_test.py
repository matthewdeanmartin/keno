# coding=utf-8
"""
# TODO: This will haunt me until I write the tests.
"""

from keno.game_runner import GameRunner, Strategy, EvolutionParameters


def xxx_slow_game() -> None:
    """
    Set up to keep variables out of global namespace
    :return:
    """
    runner = GameRunner(Strategy(max_ticket_price=50,
                                 max_plays_with_ticket_type=75,
                                 max_loss=160,  # double average per capita annual play in md
                                 sufficient_winnings=2500,
                                 state_range=["MD"],
                                 min_ticket_price=10,
                                 evade_taxes=True),
                        EvolutionParameters(max_generations=8,
                                            max_ticket_types=5000,  # Almost all possible
                                            mutation_percent=.25,
                                            fitness_bonus=2))  # 1 ticket type dominates by about 8
    runner.run()

def test_fast_game() -> None:
    """
    Set up to keep variables out of global namespace
    :return:
    """
    # 1/2 second game on my mac
    runner = GameRunner(Strategy(state_range=["DC", "MD"],
                                 min_ticket_price=0,
                                 max_ticket_price=25,
                                 max_plays_with_ticket_type=50,
                                 max_loss=25,
                                 sufficient_winnings=25,
                                 evade_taxes=True),
                        EvolutionParameters(max_generations=2,
                                            mutation_percent=.25,
                                            fitness_bonus=2,
                                            max_ticket_types=500))
    runner.run()
