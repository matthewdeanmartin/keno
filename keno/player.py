# coding=utf-8
"""
Represents a player with a particular strategy.
"""
from keno.game import Keno
from keno.ticket import Ticket, TicketValidator


class Player(object):
    """
    Person who plays keno until they lose too much money or win their target.

    Stops after certain number of games because a positive expectation value game
    is useless if it takes 1 million years. Or more than a few weeks tbh.
    """

    def __init__(self, max_loss, stop_at, max_tickets):
        """

        :type max_loss: int
        :type stop_at: int
        :type max_tickets:int
        """
        self.ticket = None
        #self.ticket.randomize_ticket()
        self.max_loss = max_loss
        self.stop_at = stop_at
        self.winnings = 0
        self.expenses = 0
        self.net_winnings = 0
        self.tickets_played = 0
        self.max_tickets_bought = max_tickets
        self.history = []
        self.history_running_bank = []
        self.md_keno = Keno()

    def good_game(self):
        """
        If a game took too long or lost too much, it ended poorly.
        :return:
        """
        return self.net_winnings >= self.stop_at

    def can_stop_any_time_i_want_to(self):
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

    def go(self):
        if self.ticket is None:
            raise TypeError("ticket not set")
        i = 0
        while not self.can_stop_any_time_i_want_to():
            i += 1
            self.tickets_played += 1


            validator = TicketValidator()
            validator.check_all_prizes_winnable(self.ticket)
            validator.check_ticket(self.ticket)

            self.expenses += self.ticket.price()

            won = self.md_keno.calculate_payoff_n_drawings(self.ticket)
            self.history.append(won)

            self.winnings += won

            # TODO: derived column, gets out of sync?
            self.net_winnings = self.winnings - self.expenses
            self.history_running_bank.append(self.net_winnings)

            if i > 500:
                # This shouldn't happen.
                raise TypeError("Why so slow?")

    def __str__(self):
        result = "---- Player ----\n"
        result += "Winnings : {0}\n".format(self.winnings)
        result += "Losses : {0}\n".format(self.expenses)
        result += "Net : {0}\n\n".format(self.net_winnings)
        result += "Tickets Played : {0}".format(self.tickets_played)
        return result
