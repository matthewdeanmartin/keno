# keno
Maryland Keno simulations

Badges
------
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE) ![Read the Docs](https://img.shields.io/readthedocs/pip.svg) ![Travis](https://img.shields.io/travis/USER/REPO.svg)


Motivation
----------
Unlike a numbers game (i.e. picking a number from 000 to 999), keno has many choices:

You have to choose # of spots to play, # of consecutive games to play, amout to bet and two variations on if you want to double cost of bet for chance to double, triple, etc, called bonus and super bonus.

You also have to choose how much money you want to win, how much you are willing to lose, how long you're willing to wait.

But you say "Wait, all numbers are equally likely to win." Yes, but the pay off chart for the 1 spot is a suckers game with low expected value and maximum risk of gambler's ruin. 5 spot with super bonus doesn't perform the same as say, 4 spot with bonus.

In stats books, the chapter on "Gamblers Ruin" will tell you the optimal way to gamble is to make 1 large bet and stop. That is way to maximize the odds that you end up ahead. Making many small bets maximizes the chance that you hit gambler's ruin and run out of money. So we'd expect this simulator to choose the ticket that is the least awful odds and bumping up against the maximum ticket price.

[Article on Gamblers Ruin](http://people.math.umass.edu/~lr7q/ps_files/teaching/math456/Chapter4.pdf) - Skip to conclusion- to minimize the odds of Gamblers ruin and maximize odds of reaching a goal, "be bold"

Genetic Algorithm
-----------------
Right now it takes n randomly generated tickets, give them to a player and simulate playing until a constraint is hit (max loss, won enough or max number of plays). 

If a ticket gets through that, it is a "good game" and we keep the ticket in the pool. Tickets are then "crossed" with each other to create hybrid tickets. If a ticket becomes invalid, I undo the crossing. Crossing generally improved the pool of tickets.

I added dupes of hybrid tickets when the population of tickets gets too low, otherwise the tickets all die out and the simulation ends early.

I tried a mutator, randomly changing a ticket feature, but that usually created highly suboptimal tickets and at most I could mutate half the population when the population was large enough. Otherwise, mutations were too deadly and caused optimal tickets to all become junk.

Finally, the gentically optimal ticket is the most common ticket by the end of the simulation.

If it is working, we'd expect it to at "be bold", i.e. bet the maximum amount, on tickets that have the best expected value, which could vary slightly from ticket type to ticket type.

Programming Gotchas
-------------------
This is python3.

Brand new drawings are expensive random.shuffle, random.sample are slow. The numpy version of the same is faster. Fastest
is to pre-calculate drawings. This creates a large 8GB file

My factoring of things into classes probably is a bit dodgy.


TODO:
-----
Strategies based on rounding errors- prizes are rounded to nearest 5, 100, 1000 but probabilities are exact. So some
bets must have a slightly higher expected value.

Strategies based on reporting level- Winning a buck less than the reporting limit is better than winning a buck more
than the reporting cut off.