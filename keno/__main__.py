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
    strategies = {
        1: Strategy(state_range=["MD"],
                    min_ticket_price=14,
                    max_ticket_price=16,
                    max_plays_with_ticket_type=5000,  # defense against infinite loops?
                    max_loss=250,
                    sufficient_winnings=2500),
        2: Strategy(state_range=["MD"],
                    min_ticket_price=15,
                    max_ticket_price=100,
                    max_plays_with_ticket_type=1000,
                    max_loss=150,
                    sufficient_winnings=25_000),
        3: Strategy(state_range=["MD"],
                    min_ticket_price=15,
                    max_ticket_price=50,
                    max_plays_with_ticket_type=1000,
                    max_loss=50,
                    sufficient_winnings=10_000),
        4: Strategy(state_range=["MD"], # three buck chuck
                    min_ticket_price=3,
                    max_ticket_price=3,
                    max_plays_with_ticket_type=5000,  # defense against infinite loops?
                    max_loss=3,
                    sufficient_winnings=2500),
    }
    runner = GameRunner(strategies[4],
                        EvolutionParameters(max_generations=6,  # increase if final isn't optimal
                                            mutation_percent=0,  # decrease if a batch of winners turns into nothing
                                            fitness_bonus=3,  # increase if slow to converge
                                            max_ticket_types=6500))  # increase if initial batches full of losers.
    runner.run()
    print(timer.elapsed("Done!"))
run()
