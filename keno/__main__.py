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

    timer = Timer()
    print(timer.start())
    s1 = Strategy(max_ticket_price=50,
                  max_plays_with_ticket_type=1000,
                  max_loss=180,
                  sufficient_winnings=5000)
    s2 = Strategy(max_ticket_price=100,
                  max_plays_with_ticket_type=1000,
                  max_loss=150,
                  sufficient_winnings=25_000)
    s3 = Strategy(max_ticket_price=50,
                  max_plays_with_ticket_type=1000,
                  max_loss=50,
                  sufficient_winnings=10_000)
    runner = GameRunner(s1,
                        EvolutionParameters(max_generations=3,
                                            mutation_percent=.20,
                                            fitness_bonus=3,
                                            max_ticket_types=10000))
    runner.run()
    print(timer.elapsed("Done!"))
run()
