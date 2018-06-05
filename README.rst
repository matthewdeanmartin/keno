keno
====

Maryland Keno simulations

Motivation
----------

Unlike a numbers game (i.e. picking a number from 000 to 999), keno has
many choices:

You have to choose # of spots to play, # of consecutive games to play,
amout to bet and two variations on if you want to double cost of bet for
chance to double, triple, etc, called bonus and super bonus.

You also have to choose how much money you want to win, how much you are
willing to lose, how long you’re willing to wait.

But you say “Wait, all numbers are equally likely to win.” Yes, but the
pay off chart for the 1 spot is a suckers game with low expected value
and maximum risk of gambler’s ruin. 5 spot with super bonus doesn’t
perform the same as say, 4 spot with bonus.

In stats books, the chapter on “Gamblers Ruin” will tell you the optimal
way to gamble is to make 1 large bet and stop. That is way to maximize
the odds that you end up ahead. Making many small bets maximizes the
chance that you hit gambler’s ruin and run out of money. So we’d expect
this simulator to choose the ticket that is the least awful odds and
bumping up against the maximum ticket price.

`Article on Gamblers
Ruin <http://people.math.umass.edu/~lr7q/ps_files/teaching/math456/Chapter4.pdf>`__
- Skip to conclusion- to minimize the odds of Gamblers ruin and maximize
odds of reaching a goal, “be bold”

Genetic Algorithm
-----------------

Right now it takes n randomly generated tickets, give them to a player
and simulate playing until a constraint is hit (max loss, won enough or
max number of plays).

If a ticket gets through that, it is a “good game” and we keep the
ticket in the pool. Tickets are then “crossed” with each other to create
hybrid tickets. If a ticket becomes invalid, I undo the crossing.
Crossing generally improved the pool of tickets.

I added dupes of hybrid tickets when the population of tickets gets too
low, otherwise the tickets all die out and the simulation ends early.

I tried a mutator, randomly changing a ticket feature, but that usually
created highly suboptimal tickets and at most I could mutate half the
population when the population was large enough. Otherwise, mutations
were too deadly and caused optimal tickets to all become junk.

Finally, the gentically optimal ticket is the most common ticket by the
end of the simulation.

If it is working, we’d expect it to at “be bold”, i.e. bet the maximum
amount, on tickets that have the best expected value, which could vary
slightly from ticket type to ticket type.

Programming Gotchas
-------------------

This is python3.

One quarter of time is spent simulating drawings. This is very slow
unless numpy is installed. random.shuffle is slow. numpy appears to add
a startup cost. Nothing else is especially expensive.

As of right now, no user input and the go() method should be broken into
classes.

My factoring of things into classes probably is a bit dodgy.

I ran out of time to add all the project niceties, like a build script.
