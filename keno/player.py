# coding=utf-8
"""

"""
from keno.ticket import Ticket
from keno.game import Keno, TicketValidator


class Player(object):
    """
    Person who plays keno until they lose too much money or win their target.

    Stops after certain number of games because a positive expectation value game
    is useless if it takes 1 million years. Or more than a few weeks tbh.
    """

    def __init__(self, max_loss, stop_at, max_tickets):
        self.ticket = Ticket()
        self.ticket.randomize_ticket()
        self.max_loss = max_loss
        self.stop_at = stop_at
        self.winnings = 0
        self.expenses = 0
        self.net_winnings = 0
        self.tickets_played = 0
        self.max_tickets_bought = max_tickets

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
        self.net_winnings = self.winnings - self.expenses
        if self.net_winnings < 0 and self.max_loss > abs(self.net_winnings):
            # print("lost enough")
            return True
        if self.net_winnings > self.stop_at:
            # print("won enough")
            return True
        if self.tickets_played > self.max_tickets_bought:
            return True
        return False

    def go(self):
        i = 0
        while not self.can_stop_any_time_i_want_to():
            i += 1
            self.tickets_played += 1
            md_keno = Keno()
            tv = TicketValidator()
            tv.check_all_prizes_winnable(self.ticket)
            tv.check_ticket(self.ticket)
            self.expenses += self.ticket.price()
            won = md_keno.calculate_payoff_n_drawings(self.ticket)
            if won > 0:
                if False:
                    print("Won {0} on game {1}".format(won, i))
            self.winnings += won

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