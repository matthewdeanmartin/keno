# coding=utf-8
"""

The Keno game, independent of player.

"""
try:
    import numpy as np
    HAVE_NUMPY = True
except:
    print("We don't have numpy, simulation will be slower, but startup time might be a bit faster")
    HAVE_NUMPY = False

import random

EIGHTY_NUMBERS = list(range(1, 80))

class NumbersMachine(object):
    """
    Abstract number drawing machine.
    """
    def __init__(self, spots):
        """
        This maybe could be a Callable or a def.
        :type spots: int
        """
        if spots == 0 or spots > 21:
            raise TypeError("What game is this? {0}".format(spots))
        self.spots = spots


    def draw(self):
        """
        user picks 1 - 10, but lotto draws 20!
        :return:
        """
        global EIGHTY_NUMBERS

        # sample might be faster?
        if not HAVE_NUMPY:
            # slower
            random.shuffle(EIGHTY_NUMBERS)
        else:
            # faster
            np.random.shuffle(EIGHTY_NUMBERS)

        drawing = EIGHTY_NUMBERS[0:self.spots]
        list.sort(drawing)
        return drawing

class Keno(object):
    """
    Maryland Keno
    """

    @property
    def ticket_ranges(self):
        """
        Make sure this doesn't accidentally get mutated.
        :type: dict[str,list[int|bool]]
        """
        return self._ticket_ranges.copy()

    def __init__(self):
        self._ticket_ranges = {
            "spots": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "games": [1, 2, 3, 4, 5, 10, 20],
            "bet": [1, 2, 3, 45, 10, 20],
            "bonus": [True, False],
            "super_bonus": [True, False],
            # "constant_numbers": [True, False] # can't really do this!!
        }
        self.pay_off_chart = {
            # lose 40% in 1 million plays
            10: {
                10:100000,
                9:4000,
                8:400,
                7:50,
                6:10,
                5:2,
                0:4
            },
            9: {
                9:25000,
                8:2500,
                7:100,
                6:20,
                5:5,
                0:2
            },
            8: {
                8: 10000,
                7: 500,
                6: 50,
                5: 10,
                4: 2
            },
            7: {
                7: 2500,
                6: 100,
                5: 15,
                4: 3,
                3: 1
            },
            6: {
                6: 1000,
                5: 50,
                4: 5,
                3: 1
            },
            5: {
                5: 300,
                4: 15,
                3: 2
            },
            4: {
                4: 50,
                3: 5,
                2: 1
            },
            3: {
                3: 25,
                2: 2
            },
            2: {
                2: 10
            },
            1: {
                1: 2
            }
        }

    def can_i_win_this_much(self, ticket, jackpot):
        """

        :type ticket: Ticket
        :type jackpot: int
        :rtype: bool
        """
        max_value = 0
        for key, value in self.possible_pay_off_for_ticket_per_game(ticket).items():
            if isinstance(value, (set, list)):
                for inner_value in value:
                    max_value = max(max_value, inner_value)
            else:
                max_value = max(max_value, value)
        return max_value >= jackpot

    def possible_pay_off_for_ticket_per_game(self, ticket):
        """

        :type ticket: Ticket
        :return:
        """
        chart = self.pay_off_chart[ticket.spots].copy()

        for key, value in chart.items():
            chart[key] = value * ticket.bet

        if ticket.bonus:
            for key, value in chart.items():
                multipliers = [10, 5, 4, 3]
                totals = set()
                for m in multipliers:
                    totals.add(m * chart[key])
                chart[key] = totals
        elif ticket.super_bonus:
            for key, value in chart.items():
                multipliers= [20, 12, 10, 6, 5, 4, 3, 2]
                totals = set()
                for m in multipliers:
                    totals.add(m * chart[key])
                chart[key] = totals

        return chart



    def state_drawing(self):
        machine = NumbersMachine(20)
        return machine.draw()

    def check_single_winning(self, picks, state_drawing):
        """

        :type picks: list[int]|set[int]
        :type state_drawing: list[int]|set[int]
        :rtype: set[int]
        """
        matches = set()
        list.sort(picks)
        for pick in picks:
            if pick in state_drawing:
                matches.add(pick)
        return matches

    def check_for_bonus(self, ten_numbers):
        odds = {

            3: 3,
            4: 15,
            5: 40,
            10: 250
        }
        for key, value in odds.items():
            if random.randint(0, value * 10) < 10:
                return key
        # guaranteed some sort of mutliplier
        return 1
        # wrong
        # for i in [10, 5, 4, 3]:
        #     if i in ten_numbers:
        #         return i
        # return 1

    def check_for_super_bonus(self, ten_numbers):
        odds = {
            2:2.4,
            3:7.1,
            4:3.9,
            5:7.4,
            6:28.2,
            10:160,
            12:310.1,
            20:930.2
        }
        for key, value in odds.items():
            if random.randint(0, value * 10) < 10:
                return key
        # guaranteed some sort of mutliplier
        return 2

        # WRONG
        # return random.randint(0,len([20, 12, 10, 6, 5, 4, 3, 2]))
        # WRONG
        # for i in [20, 12, 10, 6, 5, 4, 3, 2]:
        #     if i in ten_numbers:
        #         return i
        # return 1
    def calculate_payoff_n_drawings(self, ticket):
        """
        A multi-game ticket, just like in MD.
        :type ticket: Ticket
        :return:
        """
        so_far =0
        for i in range(0, ticket.games):
            # each game is a new set of numbers.
            state_drawing = self.state_drawing()
            so_far += self.calculate_payoff_one_drawing(state_drawing, ticket)
            if i>ticket.games:
                raise  TypeError("1 off error")

        return so_far

    def calculate_payoff_one_drawing(self, state_drawing, ticket):
        """
        One drawing, a ticket can conver many drawings
        :type state_drawing: list[int]|set[int]
        :type ticket: Ticket
        :return:
        """
        matches = self.check_single_winning(ticket.numbers, state_drawing)
        try:
            winnings = self.pay_off_chart[ticket.spots][len(matches)]
        except KeyError:
            return 0

        if ticket.bonus:
            factor = self.check_for_bonus(state_drawing)
            return winnings * ticket.bet * factor
        elif ticket.super_bonus:
            factor = self.check_for_super_bonus(state_drawing)
            return winnings * ticket.bet * factor
        else:
            return winnings * ticket.bet

