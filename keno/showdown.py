# coding=utf-8
"""
Ticket showdown between 2 tickets
"""
import multiprocessing
from typing import Tuple

from keno.player import Player
from keno.strategy import Strategy
from keno.ticket import Ticket


def playone(strategy_ticket: Tuple[Strategy, Ticket]) -> int:
    """

    :type strategy_ticket: (Strategy, Ticket)
    :rtype: int
    """
    strategy = strategy_ticket[0]
    ticket = strategy_ticket[1]
    player = Player(strategy)
    player.ticket = ticket
    player.go()
    if player.good_game():
        if False:
            print("winning: " + str(player.history))
            print("bank: " + str(player.history_running_bank))
        return 1
    return 0


def simulate_one(ticket: Ticket, strategy: Strategy, trials: int) -> float:
    """

    :param ticket:
    :return:
    """
    diagnostics = False
    workers = multiprocessing.cpu_count()
    things = [(strategy, ticket) for x in range(0, trials)]

    chunksize = int(len(things) / workers)

    with multiprocessing.Pool(processes=workers) as pool:
        results = pool.map(playone, things, chunksize)

    return sum(results) / trials


def showdown(first: Ticket, second: Ticket, strategy: Strategy) -> None:
    """

    :type first: Ticket
    :type second: Ticket
    :type strategy: Strategy
    :return:
    """
    trials = 30000
    first_result = simulate_one(first, strategy, trials)
    second_result = simulate_one(second, strategy, trials)
    if first_result > second_result:
        print("First better {0} vs {1}".format(first_result, second_result))
        print(str(first))
    else:
        print("Second better {0} vs {1}".format(first_result, second_result))
        print(str(second))


if __name__ == "__main__":
    def go() -> None:
        strategy = Strategy(state_range=["MD"],
                            min_ticket_price=14,
                            max_ticket_price=16,
                            max_plays_with_ticket_type=5000,  # defense against infinite loops?
                            max_loss=250,
                            sufficient_winnings=2500,
                            evade_taxes=True)
        first = Ticket()
        first.bet = 5
        first.spots = 5
        first.super_bonus = True
        first.bonus = False
        first.games = 1
        first.state = "MD"
        first.to_go = False

        # # some other $15 ticket
        # first = Ticket()
        # first.bet = 5
        # first.super_bonus = True
        # first.bonus = False
        # first.games = 1
        # first.spots = 5
        # first.state = "MD"
        # first.to_go = False

        # optimal
        second = Ticket()
        second.bet = 3
        second.super_bonus = False
        second.bonus = False
        second.games = 5
        second.spots = 6
        second.state = "MD"
        second.to_go = False

        showdown(first, second, strategy)


    go()
