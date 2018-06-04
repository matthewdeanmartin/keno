# coding=utf-8
"""

The Keno game, independent of player.

"""
import random
from collections import OrderedDict

from keno.number_machine import NumbersMachine


class Keno(object):
    """
    Maryland/DC Keno
    """

    @property
    def ticket_ranges(self):
        """
        Make sure this doesn't accidentally get mutated.
        :type: dict[str,list[int|bool]]
        """
        return self._ticket_ranges.copy()

    def __init__(self):
        # When cached, this turns into a singleton!
        self.machine = NumbersMachine(20)

        self._ticket_ranges = {
            "spots": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "games": [1, 2, 3, 4, 5, 10, 20],
            "bet": [1, 2, 3, 4, 5, 10, 20],
            "bonus": [True, False],
            "super_bonus": [True, False],
            "state": ["MD", "DC"]
            # "constant_numbers": [True, False] # can't really do this!!
        }
        self.dc_pay_off_chart = {
            10: {
                10: 100000,
                9: 5000,
                8: 500,
                7: 46,
                6: 10,
                5: 2,
                0: 5
            },
            9: {
                9: 20000,
                8: 2000,
                7: 100,
                6: 15,
                5: 5,
                4: 1,
                0: 2
            },
            8: {
                8: 10000,
                7: 500,
                6: 50,
                5: 7,
                4: 1,
                0: 2
            },
            7: {
                7: 1500,
                6: 150,
                5: 20,
                4: 2,
                0: 1
            },
            6: {
                6: 1500,
                5: 53,
                4: 5,
                3: 1
            },
            5: {
                5: 400,
                4: 10,
                3: 3
            },
            4: {
                4: 65,
                3: 5,
                2: 1
            },
            3: {
                3: 23,
                2: 2
            },
            2: {
                2: 10
            },
            1: {
                1: 2.50
            }

        }
        self.md_pay_off_chart = {
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

    def pay_off_chart(self, state):
        if state == "MD":
            return self.md_pay_off_chart

        if state == "DC":
            return self.dc_pay_off_chart

        raise TypeError("Don't know that state")


    def can_i_win_this_much(self, ticket, jackpot):
        """

        :type ticket: Ticket
        :type jackpot: int
        :rtype: bool
        """
        max_value = 0
        for value in self.possible_pay_off_for_ticket_per_game(ticket).values():
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
        chart = self.pay_off_chart(ticket.state)[ticket.spots].copy()

        for key, value in chart.items():
            chart[key] = value * ticket.bet

        if ticket.bonus:
            for key, value in chart.items():
                multipliers = [10, 5, 4, 3]
                totals = set()
                for multiplier in multipliers:
                    totals.add(multiplier * chart[key])
                chart[key] = totals
        elif ticket.super_bonus:
            for key, value in chart.items():
                multipliers = [20, 12, 10, 6, 5, 4, 3, 2]
                totals = set()
                for multiplier in multipliers:
                    totals.add(multiplier * chart[key])
                chart[key] = totals

        return chart


    def state_drawing(self):
        """
        The numbers drawn by state, the winning numbers
        :type:
        """
        return self.machine.draw()

    def check_single_winning(self, picks, state_drawing):
        """
        Which numbers in picks are in state drawing?
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

    def check_for_bonus(self, state):
        """
        Rule confusing...I think this is determined as a function of drawying and/or user selections
        :rtype: int
        """
        md_odds = {

            3: 3,
            4: 15,
            5: 40,
            10: 250
        }
        dc_odds = {
            1: 0.4008703648066716,
            2: 0.4246870419432078,
            3: 0.06193246478937354,
            4: 0.06255701526780105,
            5: 0.0375841003650798,
            10: 0.012367191980990358
        }

        if state == "DC":
            cummulative_prob = OrderedDict([(1, 0.4008703648066716),
                                            (2, 0.8255574067498794),
                                            (3, 0.887489871539253),
                                            (4, 0.950046886807054),
                                            (5, 0.9876309871721337),
                                            (10, 0.9999981791531241)])
            spin = random.uniform(0, 1)
            for key, value in cummulative_prob.items():
                if key < value:
                    return key
            return 1

        if state == "MD":
            for key, value in md_odds.items():
                if random.randint(0, value * 10) < 10:
                    return key
            # guaranteed some sort of mutliplier
            return 1
        raise TypeError("Don't know this state")
        # wrong
        # for i in [10, 5, 4, 3]:
        #     if i in ten_numbers:
        #         return i
        # return 1

    def check_for_super_bonus(self, state):
        """
        Rule confusing...I think this is determined as a function of drawying and/or user selections
        :rtype: int
        """
        if state == "DC":
            return 1
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

    def calculate_payoff_n_drawings(self, ticket):
        """
        A multi-game ticket, just like in MD.
        :type ticket: Ticket
        :return:
        """
        so_far = 0
        for i in range(0, ticket.games):
            # each game is a new set of numbers.
            state_drawing = self.state_drawing()
            so_far += self.calculate_payoff_one_drawing(state_drawing, ticket)
            if i > ticket.games:
                raise  TypeError("1 off error")

        return so_far

    def calculate_payoff_one_drawing(self, state_drawing, ticket):
        """
        One drawing, a ticket can conver many drawings
        :type state_drawing: list[int]|set[int]
        :type ticket: Ticket
        :rtype: int
        """
        # print(state_drawing, ticket.numbers)
        if len(ticket.numbers) == 0:
            raise TypeError("uninitialized ticket numbers")
        if len(ticket.numbers) != ticket.spots:
            raise TypeError("wrongly initialized ticket numbers - expected len(n) to match spots")
        matches = self.check_single_winning(ticket.numbers, state_drawing)
        try:
            winnings = self.pay_off_chart(ticket.state)[ticket.spots][len(matches)]
        except KeyError:
            return 0

        if ticket.bonus:
            factor = self.check_for_bonus(ticket.state)
            return winnings * ticket.bet * factor

        if ticket.super_bonus:
            factor = self.check_for_super_bonus(ticket.state)
            return winnings * ticket.bet * factor

        return winnings * ticket.bet

