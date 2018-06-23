# coding=utf-8
"""

The Keno game, independent of player.

"""
import random
from collections import OrderedDict
from typing import Dict, Union, List, Set

from keno.number_machine import NumbersMachine


# CYCLICAL REFS!!
# from keno.ticket import Ticket
# from keno.ticket import Strategy


class Keno(object):
    """
    Maryland/DC Keno
    """

    # @property
    def ticket_ranges(self, to_go: bool) -> Dict[str, object]:
        """
        Make sure this doesn't accidentally get mutated.
        :type to_go: bool
        :rtype: dict[str,list[int|bool]]
        """
        if to_go:
            return self._to_go_ranges.copy()
        return self._ticket_ranges.copy()

    def __init__(self) -> None:
        """
        Set up general parameters that state chose
        """

        # When cached, this turns into a singleton!
        self.machine = NumbersMachine(20)

        self._to_go_ranges = {
            "to_go": [True, False],  # .25 cent games
            "spots": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "games": [20, 40, 60, 80, 100],
            "bet": [0.25],
            "bonus": [True, False],
            "super_bonus": [True, False],
            "state": ["MD"]  # , "WV", "OH" ... other states not ready yet.
            # "constant_numbers": [True, False] # can't really do this!!
        }
        self._ticket_ranges = {
            "to_go": [True, False],  # .25 cent games
            "spots": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "games": [1, 2, 3, 4, 5, 10, 20],
            "bet": [1, 2, 3, 4, 5, 10, 20],
            "bonus": [True, False],
            "super_bonus": [True, False],
            "state": ["MD", "DC"]  # , "WV", "OH" ... other states not ready yet.
            # "constant_numbers": [True, False] # can't really do this!!
        }
        self.dc_pay_off_chart = {
            10: {
                10: 100_000.0,
                9: 5_000.0,
                8: 500.0,
                7: 46.0,
                6: 10.0,
                5: 2.0,
                0: 5.0
            },
            9: {
                9: 20_000.0,
                8: 2_000.0,
                7: 100.0,
                6: 15.0,
                5: 5.0,
                4: 1.0,
                0: 2.0
            },
            8: {
                8: 10_000.0,
                7: 500.0,
                6: 50.0,
                5: 7.0,
                4: 1.0,
                0: 2.0
            },
            7: {
                7: 1_500.0,
                6: 150.0,
                5: 20.0,
                4: 2.0,
                0: 1.0
            },
            6: {
                6: 1_500.0,
                5: 53.0,
                4: 5.0,
                3: 1.0
            },
            5: {
                5: 400.0,
                4: 10.0,
                3: 3.0
            },
            4: {
                4: 65.0,
                3: 5.0,
                2: 1.0
            },
            3: {
                3: 23.0,
                2: 2.0
            },
            2: {
                2: 10.0
            },
            1: {
                1: 2.50
            }

        }
        self.md_to_go_pay_off_chart = {
            10: {
                10: 25_000.0,
                9: 1_000.0,
                8: 100.0,
                7: 12.50,
                6: 2.50,
                5: 0.50,
                0: 1.0
            },
            9: {
                9: 6_250.0,
                8: 625.0,
                7: 25.0,
                6: 5.0,
                5: 1.25,
                0: .50
            },
            8: {
                8: 2_500.0,
                7: 125.0,
                6: 12.50,
                5: 3.75,
                4: .50
            },
            7: {
                7: 625.0,
                6: 25.0,
                5: 3.75,
                4: .75,
                3: .25
            },
            6: {
                6: 250.0,
                5: 12.50,
                4: 3.75,
                3: .25
            },
            5: {
                5: 75.0,
                4: 3.75,
                3: .50
            },
            4: {
                4: 12.50,
                3: 1.25,
                2: .25
            },
            3: {
                3: 6.25,
                2: .50
            },
            2: {
                2: 2.50
            },
            1: {
                1: .50
            }
        }
        self.md_pay_off_chart = {
            # lose 40% in 1 million plays
            10: {
                10: 100000.0,
                9: 4000.0,
                8: 400.0,
                7: 50.0,
                6: 10.0,
                5: 2.0,
                0: 4.0
            },
            9: {
                9: 25000.0,
                8: 2500.0,
                7: 100.0,
                6: 20.0,
                5: 5.0,
                0: 2.0
            },
            8: {
                8: 10000.0,
                7: 500.0,
                6: 50.0,
                5: 10.0,
                4: 2.0
            },
            7: {
                7: 2500.0,
                6: 100.0,
                5: 15.0,
                4: 3.0,
                3: 1.0
            },
            6: {
                6: 1000.0,
                5: 50.0,
                4: 5.0,
                3: 1.0
            },
            5: {
                5: 300.0,
                4: 15.0,
                3: 2.0
            },
            4: {
                4: 50.0,
                3: 5.0,
                2: 1.0
            },
            3: {
                3: 25.0,
                2: 2.0
            },
            2: {
                2: 10.0
            },
            1: {
                1: 2.0
            }
        }
        # 25.0% federal tax
        # 8.75% state tax for Maryland residents
        # 7.5% state tax for non-Maryland residents
        self.taxes ={
            "MD":{
                "limit":5000,
                "rate" :.25+.087
            }
        }
        self.wv_pay_off_chart = {
            10:{
                10: 100000.0,
                9: 4000.0,
                8: 400.0,
                7: 50.0,
                6: 10.0,
                5: 2.0,
                0: 4.0
            },
            9: {
                9: 25000.0,
                8: 2500.0,
                7: 200.0,
                6: 25.0,
                5: 4.0,
                0: 2.0
            },
            8: {
                8: 10000.0,
                7: 500.0,
                6: 50.0,
                5: 10.0,
                4: 2.0
            },
            7: {
                7: 2500.0,
                6: 125.0,
                5: 15.0,
                4: 2.0,
                3: 1.0
            },
            6: {
                6: 1500.0,
                5: 50.0,
                4: 5.0,
                3: 1.0
            },
            5: {
                5: 400.0,
                4: 15.0,
                3: 2.0
            },
            4: {
                4: 50.0,
                3: 5.0,
                2: 1.0
            },
            3: {
                3: 25.0,
                2: 2.0
            },
            2: {
                2: 10.0
            },
            1: {
                1: 2.0
            }
        }
        self.oh_pay_off_chart = {
            10: {
                10: 100_000.0,
                9: 5_000.0,
                8: 500.0,
                7: 50.0,
                6: 10.0,
                5: 2.0,
                0: 5.0
            },
            9: {
                9: 25_000.0,
                8: 2_000.0,
                7: 100.0,
                6: 20.0,
                5: 5.0,
                0: 2.0
            },
            8: {
                8: 10_000.0,
                7: 300.0,
                6: 50.0,
                5: 15.0,
                4: 2.0
            },
            7: {
                7: 2000.0,
                6: 100.0,
                5: 11.0,
                4: 5.0,
                3: 1.0
            },
            6: {
                6: 1100.0,
                5: 57.0,
                4: 7.0,
                3: 1.0
            },
            5: {
                5: 410.0,
                4: 18.0,
                3: 2.0
            },
            4: {
                4: 72.0,
                3: 5.0,
                2: 1.0
            },
            3: {
                3: 27.0,
                2: 2.0
            },
            2: {
                2: 11.0
            },
            1: {
                1: 2.0
            }
        }

    def pay_off_chart(self, ticket: "Ticket") -> Dict[int, Dict[int, float]]:
        """

        :type ticket: Ticket
        :type: dict[dict[int,float]]
        """
        state = ticket.state
        to_go = ticket.to_go

        if state == "MD" and not to_go:
            # wrong place to apply taxes...
            return self.md_pay_off_chart

        if state == "MD" and to_go:
            return self.md_to_go_pay_off_chart

        if state == "DC":
            return self.dc_pay_off_chart

        if state == "WV":
            return self.wv_pay_off_chart
        if state == "OH":
            return self.wv_pay_off_chart
        raise TypeError("Don't know that state")

    def can_i_win_this_much(self, ticket: "Ticket", jackpot: float) -> bool:
        """

        :type ticket: Ticket
        :type jackpot: int|float
        :rtype: bool
        """
        max_value = 0.0
        for value in self.possible_pay_off_for_ticket_per_game(ticket).values():
            if isinstance(value, (set, list)):
                for inner_value in value:
                    max_value = max(max_value, inner_value)
            else:
                max_value = max(max_value, value)
        return max_value >= jackpot

    def possible_pay_off_for_ticket_per_game(self, ticket: "Ticket") -> Dict[
        int, Union[int, float, List[float]]]:
        """

        :type ticket: Ticket
        :return:
        """
        chart = self.pay_off_chart(ticket)[ticket.spots].copy()

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

    def state_drawing(self) -> List[int]:
        """
        The numbers drawn by state, the winning numbers
        :type:
        """
        return self.machine.draw()

    def check_single_winning(self,
                             picks: Union[List[int], Set[int]],
                             state_drawing: Union[List[int], Set[int]]) -> Set[int]:
        """
        Which numbers in picks are in state drawing?
        :type picks: list[int]|set[int]
        :type state_drawing: list[int]|set[int]
        :rtype: set[int]
        """
        matches = set()
        # list.sort(picks)
        for pick in picks:
            if pick in state_drawing:
                matches.add(pick)
        return matches

    def check_for_bonus(self, state: str) -> int:
        """
        Rule confusing...I think this is determined as a function of drawying and/or user selections
        :rtype: int
        """

        if state == "DC":
            cummulative_prob = OrderedDict([(1, 0.4008703648066716),
                                            (2, 0.8255574067498794),
                                            (3, 0.887489871539253),
                                            (4, 0.950046886807054),
                                            (5, 0.9876309871721337),
                                            (10, 0.9999981791531241)])
            spin = random.uniform(0, 1)
            for key, value in cummulative_prob.items():
                if value < spin:
                    return key
            return 1

        if state == "MD":
            md_odds = {

                3: 3,
                4: 15,
                5: 40,
                10: 250
            }
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

    def check_for_super_bonus(self, state: str) -> int:
        """
        Rule confusing...I think this is determined as a function of drawying and/or user selections
        :rtype: int
        """
        if state in ("DC", "WV", "OH"):
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
            if random.randint(0, int(value * 10)) < 10:
                return key
        # guaranteed some sort of mutliplier
        return 2

    def calculate_payoff_n_drawings(self, ticket: "Ticket", strategy: "Strategy") -> float:
        """
        A multi-game ticket, just like in MD.
        :type ticket: Ticket
        :return:
        """
        so_far = 0.0
        for i in range(0, ticket.games):
            # each game is a new set of numbers.
            state_drawing = self.state_drawing()
            so_far += self.calculate_payoff_one_drawing(state_drawing, ticket)
            if i > ticket.games:
                raise  TypeError("1 off error")

        # NOW we calculate taxes
        state = ticket.state
        prize = so_far
        if not strategy.evade_taxes:
            if state == "MD":
                if prize >= self.taxes[state]["limit"]:
                    so_far = prize * (1 - self.taxes[state]["rate"])

        return so_far

    def calculate_payoff_one_drawing(self,
                                     state_drawing: List[int],
                                     ticket: "Ticket") -> float:
        """
        One drawing, a ticket can conver many drawings
        :type state_drawing: list[int]|set[int]
        :type ticket: Ticket
        :rtype: int
        """

        # print(state_drawing, ticket.numbers)
        if not ticket.numbers:
            raise TypeError("uninitialized ticket numbers")
        if len(ticket.numbers) != ticket.spots:
            raise TypeError("wrongly initialized ticket numbers - expected len(n) to match spots")
        matches = self.check_single_winning(ticket.numbers, state_drawing)
        try:
            winnings = float(self.pay_off_chart(ticket)[ticket.spots][len(matches)])
        except KeyError:
            return 0.0

        if ticket.bonus:
            factor = self.check_for_bonus(ticket.state)
            return float(winnings * ticket.bet * factor)

        if ticket.super_bonus:
            factor = self.check_for_super_bonus(ticket.state)
            return float(winnings * ticket.bet * factor)

        return float(winnings * ticket.bet)
