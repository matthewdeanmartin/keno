# coding=utf-8
"""
All choice that a player makes when buying a ticket.

Some choices are "sucker's bets" and should not be played.
"""
import copy

from keno.game import Keno, NumbersMachine, TicketValidator
import random

class Ticket(object):
    def __init__(self):
        self.spots = 1
        self.games = 1
        self.bet = 2
        self.bonus = False
        self.super_bonus = False
        self.numbers = []
        self.rules = Keno()
        # actually... you can't buy multiple tickets against same game... hafta buy multiples
        # within same 3 mintues!!
        # self.constant_numbers = False

    def pick(self):
        machine = NumbersMachine(self.spots)
        self.numbers = machine.draw()

    def price(self):
        base = self.games * self.bet
        if self.bonus:
            return base * 2
        if self.super_bonus:
            return base * 3
        return base

    def randomize_ticket(self):

        tv = TicketValidator()

        i = 0
        while i == 0 or not tv.is_good_ticket(self):
            i+=1
            for key, value in self.rules.ticket_ranges.items():
                setattr(self, key, self.rules.ticket_ranges[key][random.randint(0, len(value)-1)])

            if self.bonus and self.super_bonus:
                if random.randint(0, 1)==1:
                    self.bonus = True
                    self.super_bonus = False
                else:
                    self.bonus = False
                    self.super_bonus = True
            if i>100:
                raise TypeError("Can't generate a good ticket!")




    def __str__(self):
        result = "----- Ticket ------\n"
        md_keno = Keno()

        for key, value in sorted(md_keno.ticket_ranges.items()):
            result += "{0}, {1}".format(key,  getattr(self, key))
            result += "\n"
        return result

    def geneticly_merge_ticket(self, ticket, max_price):
        if self == ticket:
            # crossing with a clone.
            return
        save_point = copy.deepcopy(self)

        keys = [x for x in self.rules.ticket_ranges.keys()]
        random.shuffle(keys)
        for key in keys:
            if random.randint(0,1)==1:
                setattr(self, key, getattr(ticket, key))

        try:
            # This mutant valid?
            tv = TicketValidator()
            tv.check_all_prizes_winnable(self)
            tv.check_ticket(self)
            if self.price()> max_price:
                raise TypeError("nope")
        except:
            # undo
            for key in keys:
                setattr(self, key, getattr(save_point, key))

    def mutate_ticket(self, percent):
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
            tv = TicketValidator()
            tv.check_all_prizes_winnable(self)
            tv.check_ticket(self)
        except:
            # undo
            for key in keys:
                setattr(self, key, getattr(save_point, key))


    def __eq__(self, other):
        """

        :type other:Ticket
        :rtype:bool
        """
        # numbers & rules ignored right now.
        return self.spots == other.spots and \
                self.games == other.games and \
                self.bet == other.bet and \
                self.bonus == other.bonus and \
                self.super_bonus == other.super_bonus

    def __hash__(self):
        return hash("".join(list(map(str,[self.spots, self.games, self.bet, self.bonus, self.super_bonus]))))

