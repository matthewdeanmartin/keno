#!/usr/bin/env python3
# coding=utf-8
"""Keno

Simulates keno to find the ticket that minimizes the odds gamblers ruin for a given goal and maximum loss. You will still probably lose your money.

Usage:
  play.py keno [--max_loss=<max_loss> --sufficient_winnings=<sufficient_winnings>] [options]
  play.py (-h | --help)
  play.py --version

Options:
  -h --help     Show this screen.
  --max_ticket_price=<max_ticket_price>                     Most you are willing to gamble on one ticket. Many states set to $100 [default: 50]
  --max_plays_with_ticket_type=<max_plays_with_ticket_type>  When to stop or defense against infinite loops [default: 5000]
  --max_loss=<max_loss>                                     Most you are willing to lose, i.e. gambler's ruin
  --sufficient_winnings=<sufficient_winnings>               When you will stop.
  --max_generations=<max_generations>                   How many generations for the genetic algorithm to run [default: 6]
  --mutation_percent=<mutation_percent>                 How many attributes to mutate each generation [default: 0.2]
  --fitness_bonus=<fitness_bonus>                       How many copies of most successful make it to next generation [default: 2]
  --max_ticket_types=<max_ticket_types>                 How many individuals (tickets) in initial population [default: 5000]

"""
from docopt import docopt

from keno.game_runner import GameRunner, Strategy, EvolutionParameters
from keno.stop_watch import Timer


def run(args):
    """
    Set up to keep variables out of global namespace
    :return:
    """

    t = Timer()
    if t is None:
        raise TypeError("WTF")
    print(t.start())
    args_strategy = Strategy(max_ticket_price=float(args["--max_ticket_price"]),
                             max_plays_with_ticket_type=int(args["--max_plays_with_ticket_type"]),
                             max_loss=float(args["--max_loss"]),
                             sufficient_winnings=float(args["--sufficient_winnings"]))
    runner = GameRunner(args_strategy,
                        EvolutionParameters(max_generations=int(args["--max_generations"]),
                                            mutation_percent=float(args["--mutation_percent"]),
                                            fitness_bonus=int(args["--fitness_bonus"]),
                                            max_ticket_types=int(args["--max_ticket_types"])))
    runner.run()
    print(t.elapsed("Done!"))


if __name__ == '__main__':
    args = docopt(__doc__, argv=None, help=False, version='Keno 1.0.0', options_first=False)
    run(args)
