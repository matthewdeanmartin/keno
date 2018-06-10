#!/usr/bin/env python3
# coding=utf-8
"""Keno

Simulates keno to find the ticket that minimizes the odds gamblers ruin for a given goal and maximum loss. You will still probably lose your money.

Usage:
  play.py  [options]
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
  --min_ticket_price=<min_ticket_price>     Attempt to guarantee a Be Bold strategy [default: 0]
  --state_range=<state_range>               Comma delimted, e.g. MD or MD,DC [default: MD]
  --evade_taxes=<evade_taxes>               Assume taxes not paid if state doesn't withhold, e.g. small prizes[default: 1]
"""
from argopt import argopt
__version__ = "0.1.0"

# gooey doesn't work on mac with venv, it demands to use the global pythonw!
# and not regular python3!
from gooey import Gooey

@Gooey
def main():
    # works, but without anything 'fancy'
    argparser =argopt(__doc__, version=__version__)
    args = argparser.parse_args()
    print(args)

if __name__ == '__main__':
    main()