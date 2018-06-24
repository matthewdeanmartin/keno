# coding=utf-8
"""
Represents a player with a particular strategy.
"""
from typing import Union, Tuple, List

from keno.game import Keno
from keno.strategy import Strategy
from keno.ticket import Ticket
from keno.ticket import TicketValidator


class Player(object):
    """
    Person who plays keno until they lose too much money or win their target.

    Stops after certain number of games because a positive expectation value game
    is useless if it takes 1 million years. Or more than a few weeks tbh.
    """

    def __init__(self, strategy: Strategy) -> None:
        """

        :type strategy: Strategy
        """
        self.ticket: Ticket

        # strategy
        self.max_loss = strategy.max_loss
        self.stop_at = strategy.sufficient_winnings
        self.max_tickets_bought = strategy.max_plays_with_ticket_type
        self.strategy = strategy

        # state
        self.winnings = 0.0
        self.expenses = 0.0
        self.net_winnings = 0.0
        self.tickets_played = 0

        self.history = []  # type: List[Union[float,str]]
        self.fitness = 0.0  # SHOULD BE TICKET PROPRETY!!
        self.history_running_bank = []  # type: List[float]
        self.md_keno = Keno()

    def good_game(self) -> bool:
        """
        Did we hit the goal. Period.
        :return:
        """
        if self.ticket is None:
            raise TypeError("Uninitialized ticket.")
        if self.ticket.to_go and self.net_winnings >= self.stop_at:
            print(str(self.ticket))
        self.fitness = self.evolutionary_fitness()
        self.ticket.fitness = self.fitness
        return self.net_winnings >= self.stop_at

    def evolutionary_fitness(self) -> float:
        """
        Did we over-fulfill the goal, how bad were our losses
        :return:
        """
        return self.net_winnings

    def can_stop_any_time_i_want_to(self) -> bool:
        """
        Stop when won enough, lost too much, or game taking too long.
        :return:
        """

        if self.net_winnings < 0 and abs(self.net_winnings) > self.max_loss:
            # print("lost enough")
            self.history.append("lost more than max_loss")
            return True
        if self.net_winnings > self.stop_at:
            # print("won enough")
            self.history.append("won goal")
            return True
        if self.tickets_played > self.max_tickets_bought:
            self.history.append("played enough tickets")
            return True
        return False

    def go(self) -> Tuple[float, int]:
        """
        Keep playing same ticket type until a stop condition is met.
        :return:
        """
        if self.ticket is None:
            raise TypeError("ticket not set")

        if self.ticket.history:
            ticket_history_generation = max(self.ticket.history.keys()) + 1
        else:
            ticket_history_generation = 1
        i = 0
        while not self.can_stop_any_time_i_want_to():
            i += 1
            self.tickets_played += 1

            validator = TicketValidator()
            validator.check_all_prizes_winnable(self.ticket)
            validator.check_ticket(self.ticket)

            self.expenses += self.ticket.price()

            won = self.md_keno.calculate_payoff_n_drawings(self.ticket, self.strategy)
            self.history.append(won)
            self.ticket.history.setdefault(ticket_history_generation, []).append(won)

            self.winnings += won

            # TODO: derived column, gets out of sync?
            self.net_winnings = self.winnings - self.expenses
            self.history_running_bank.append(self.net_winnings)

            if i > self.max_tickets_bought + 1:
                # This shouldn't happen.
                raise TypeError("Why so slow?")
        # house stats.
        return -self.net_winnings, self.tickets_played * self.ticket.games

    def __str__(self) -> str:
        result = "---- Player ----\n"
        result += "Winnings : {0}\n".format(self.winnings)
        result += "Losses : {0}\n".format(self.expenses)
        result += "Net : {0}\n\n".format(self.net_winnings)
        result += "Tickets Played : {0}".format(self.tickets_played)
        return result
