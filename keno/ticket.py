# coding=utf-8
"""
All choice that a player makes when buying a ticket.

Some choices are "sucker's bets" and should not be played.
"""
import copy
import random

from keno.game import Keno
from keno.number_machine import StaticNumbersMachine

KENO = Keno()
class Ticket(object):
    """
    Represents all the choices you make on a real ticket.

    Assumes that the exact numbers are not a real choice, that one set of numbers is as good as the next.
    """
    def __init__(self):
        self.spots = -1
        self.games = -1
        self.bet = -1
        self.bonus = None
        self.super_bonus = None
        self._numbers = []
        self.state = None

        global KENO
        self.rules = KENO
        # actually... you can't buy multiple tickets against same game... hafta buy multiples
        # within same 3 mintues!!
        # self.constant_numbers = False

    @property
    def numbers(self):
        """
        Make sure this doesn't accidentally get mutated.
        :type: dict[str,list[int|bool]]
        """
        if len(self._numbers) == 0:
            self.pick()
        return self._numbers

    def pick(self):
        """
        Generate random numbers, but other strategic decisions.
        :return:
        """
        if self.spots < 1 or self.spots > 20:
            raise TypeError("Invalid spot range")
        machine = StaticNumbersMachine(self.spots)
        self._numbers = machine.draw()
        assert len(self.numbers) == self.spots

    def price(self):
        """
        How much does this ticket cost?
        :rtype: int
        """
        base = self.games * self.bet
        if self.bonus:
            return base * 2
        if self.super_bonus:
            return base * 3
        return base

    def randomize_ticket(self):
        """
        Randomize self
        :return:
        """

        validator = TicketValidator()

        i = 0
        while i == 0 or not validator.is_good_ticket(self):
            i += 1
            for key, value in self.rules.ticket_ranges.items():
                setattr(self, key, self.rules.ticket_ranges[key][random.randint(0, len(value)-1)])


            if self.bonus and self.super_bonus and self.state == "MD":
                if random.randint(0, 1) == 1:
                    self.bonus = True
                    self.super_bonus = False
                else:
                    self.bonus = False
                    self.super_bonus = True
            if self.state == "DC":
                self.super_bonus = False

            if i > 200:
                raise TypeError("Can't generate a good ticket!")

    def __str__(self):
        """
        Pretty printer
        :return:
        """
        result = "----- Ticket ------\n"
        md_keno = Keno()

        for key in sorted(md_keno.ticket_ranges):
            result += "{0}, {1}".format(key, getattr(self, key))
            result += "\n"
        return result

    def geneticly_merge_ticket(self, ticket, max_price):
        """
        Make this ticket 1/2 like the other ticket
        :type ticket: Ticket
        :type max_price: int
        :return:
        """
        if self == ticket:
            # crossing with a clone.
            return
        save_point = copy.deepcopy(self)

        keys = [x for x in self.rules.ticket_ranges.keys()]
        random.shuffle(keys)
        for key in keys:
            if random.randint(0, 1) == 1:
                setattr(self, key, getattr(ticket, key))

        try:
            # This mutant valid?
            validator = TicketValidator()
            validator.check_all_prizes_winnable(self)
            validator.check_ticket(self)
            if self.price() > max_price:
                raise TypeError("nope")
        except:
            # undo
            for key in keys:
                setattr(self, key, getattr(save_point, key))

    def mutate_ticket(self, percent):
        """
        Make this ticket change to random property for up to n percent
        :type percent:float
        :return:
        """
        save_point = copy.deepcopy(self)

        mutation_ticket = Ticket()
        mutation_ticket.randomize_ticket()

        features = len(self.rules.ticket_ranges)
        i = 0
        keys = [x for x in self.rules.ticket_ranges.keys()]
        random.shuffle(list(keys))
        for key in keys:
            i += 1
            setattr(self, key, getattr(mutation_ticket, key))
            if i/features > percent:
                break
        try:
            # This mutant valid?
            validator = TicketValidator()
            validator.check_all_prizes_winnable(self)
            validator.check_ticket(self)
        except:
            # undo
            for key in keys:
                setattr(self, key, getattr(save_point, key))


    def __eq__(self, other):
        """
        Check equality
        :type other:Ticket
        :rtype:bool
        """
        # numbers & rules ignored right now.
        return self.spots == other.spots and \
                self.games == other.games and \
                self.bet == other.bet and \
                self.bonus == other.bonus and \
                self.super_bonus == other.super_bonus and \
                self.state == other.state

    def __hash__(self):
        """
        Allow this to be in dictionary for histogram calculations
        :return:
        """
        return hash("".join(list(map(str, [self.spots, self.games, self.bet, self.bonus, self.super_bonus, self.state]))))


class TicketValidator(object):
    """
    Check if ticket is valid for MD Keno game
    """

    def __init__(self):
        self.md_keno = Keno()

    def is_good_ticket(self, ticket):
        """
        Boolean check
        :type ticket: Ticket
        :rtype: bool
        """
        try:
            self.check_ticket(ticket)
            self.check_all_prizes_winnable(ticket)
            return True
        except:
            return False

    def check_ticket(self, ticket):
        """
        Throws on bad tickets
        :type ticket: Ticket
        :rtype: None
        """
        if len(ticket.numbers) == 0:
            raise TypeError("numbers not initialized")
        if len(ticket.numbers) != ticket.spots:
            raise TypeError("numbers wrongly initialized")

        for key, value in self.md_keno.ticket_ranges.items():
            if getattr(ticket, key) not in self.md_keno.ticket_ranges[key]:
                raise TypeError("Bad ticket {0} can be {1}, but got".format(key, value, getattr(ticket, key)))

        # bonus rules
        if ticket.bonus and ticket.super_bonus:
            raise TypeError("Can't do bonus and super bonus at same time.")

        # max ticket rules
        # $100 is the maximum Keno wager per playslip.
        # $200 is the maximum Keno wager per playslip when the Bonus option is selected.
        # $300 is the maximum Keno wager per playslip when the Super Bonus option is selected.
        if ticket.bet * ticket.games > 100:
            raise TypeError("Too much for this slip! ${0}".format(ticket.bet * ticket.games))
        if ticket.bonus and ticket.bet * 2 * ticket.games > 200:
            raise TypeError("Too much for this slip! ${0}".format(ticket.bet * 2 * ticket.games))
        if ticket.super_bonus and ticket.bet * 3 * ticket.games > 300:
            raise TypeError("Too much for this slip ${0}".format(ticket.bet * 3 * ticket.games))

    def check_all_prizes_winnable(self, ticket):
        """
        Throws on bad tickets
        :type ticket: Ticket
        :rtype: None
        """
        # don't bet if max prize is unwinnable (
        if ticket.bonus and self.md_keno.pay_off_chart(ticket.state)[ticket.spots][ticket.spots] * ticket.bet * 10 > 100000:
            raise TypeError("Why? Max payout is 100K")
        if ticket.bonus and self.md_keno.pay_off_chart(ticket.state)[ticket.spots][ticket.spots] * ticket.bet * 20 > 100000:
            raise TypeError("Why? Max payout is 100K")
