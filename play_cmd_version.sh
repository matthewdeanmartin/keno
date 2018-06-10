#!/usr/bin/env bash

play_with_all_opts()
{

#  --max_ticket_price=<max_ticket_price>                     Most you are willing to gamble on one ticket. Many states set to $100 [default: 50]
#  --max_plays_with_ticket_type=<max_plays_with_ticket_type>  When to stop or defense against infinite loops [default: 5000]
#  --max_loss=<max_loss>                                     Most you are willing to lose, i.e. gambler's ruin
#  --sufficient_winnings=<sufficient_winnings>               When you will stop.
#  --max_generations=<max_generations>                   How many generations for the genetic algorithm to run [default: 6]
#  --mutation_percent=<mutation_percent>                 How many attributes to mutate each generation [default: 0.2]
#  --fitness_bonus=<fitness_bonus>                       How many copies of most successful make it to next generation [default: 2]
#  --max_ticket_types=<max_ticket_types>                 How many individuals (tickets) in initial population [default: 5000]
pipenv run ./play.py keno --max_loss=500 --sufficient_winnings=5000 --max_ticket_price=100 \
    --max_plays_with_ticket_type=10000 \
    --max_generations=4 --mutation_percent=0 \
    --fitness_bonus=3 --max_ticket_types=15000
}


pipenv run ./play.py keno --max_loss=500 --sufficient_winnings=5000