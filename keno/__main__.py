# coding=utf-8
"""
Code to allow launching module directly with python -m keno
"""
from keno.game_runner import GameRunner, Strategy, EvolutionParameters
from keno.stop_watch import Timer

def run():
    """
    Set up to keep variables out of global namespace
    :return:
    """

    t = Timer()
    if t is None:
        raise TypeError("WTF")
    print(t.start())
    runner = GameRunner(Strategy(max_ticket_price=50,
                                 max_plays_with_ticket_type=1000,
                                 max_loss=180,
                        sufficient_winnings=5000),
                        EvolutionParameters(max_generations=8,
                                            mutation_percent=.25,
                                            fitness_bonus=3,
                                            max_ticket_types=10000))
    runner.run()
    print(t.elapsed("Done!"))
run()
