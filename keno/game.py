# coding=utf-8
"""

This represents the game's rules. Mostly payoff charts and rules objects
for indidcating if a state supports this or that variation of the game.

Do not include references to Ticket or Strategy or you'll get circular
dependencies!

"""
import random
from collections import OrderedDict
from typing import Dict, Union, List, Set

from keno.number_machine import NumbersMachine


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
            10: {10: 100_000.0, 9: 5_000.0, 8: 500.0, 7: 46.0, 6: 10.0, 5: 2.0, 0: 5.0},
            9: {9: 20_000.0, 8: 2_000.0, 7: 100.0, 6: 15.0, 5: 5.0, 4: 1.0, 0: 2.0},
            8: {8: 10_000.0, 7: 500.0, 6: 50.0, 5: 7.0, 4: 1.0, 0: 2.0},
            7: {7: 1_500.0, 6: 150.0, 5: 20.0, 4: 2.0, 0: 1.0},
            6: {6: 1_500.0, 5: 53.0, 4: 5.0, 3: 1.0},
            5: {5: 400.0, 4: 10.0, 3: 3.0},
            4: {4: 65.0, 3: 5.0, 2: 1.0},
            3: {3: 23.0, 2: 2.0},
            2: {2: 10.0},
            1: {1: 2.50},
        }
        self.md_to_go_pay_off_chart = {
            10: {
                10: 25_000.0,
                9: 1_000.0,
                8: 100.0,
                7: 12.50,
                6: 2.50,
                5: 0.50,
                0: 1.0,
            },
            9: {9: 6_250.0, 8: 625.0, 7: 25.0, 6: 5.0, 5: 1.25, 0: .50},
            8: {8: 2_500.0, 7: 125.0, 6: 12.50, 5: 3.75, 4: .50},
            7: {7: 625.0, 6: 25.0, 5: 3.75, 4: .75, 3: .25},
            6: {6: 250.0, 5: 12.50, 4: 3.75, 3: .25},
            5: {5: 75.0, 4: 3.75, 3: .50},
            4: {4: 12.50, 3: 1.25, 2: .25},
            3: {3: 6.25, 2: .50},
            2: {2: 2.50},
            1: {1: .50},
        }
        self.md_pay_off_chart = {
            # lose 40% in 1 million plays
            10: {10: 100000.0, 9: 4000.0, 8: 400.0, 7: 50.0, 6: 10.0, 5: 2.0, 0: 4.0},
            9: {9: 25000.0, 8: 2500.0, 7: 100.0, 6: 20.0, 5: 5.0, 0: 2.0},
            8: {8: 10000.0, 7: 500.0, 6: 50.0, 5: 10.0, 4: 2.0},
            7: {7: 2500.0, 6: 100.0, 5: 15.0, 4: 3.0, 3: 1.0},
            6: {6: 1000.0, 5: 50.0, 4: 5.0, 3: 1.0},
            5: {5: 300.0, 4: 15.0, 3: 2.0},
            4: {4: 50.0, 3: 5.0, 2: 1.0},
            3: {3: 25.0, 2: 2.0},
            2: {2: 10.0},
            1: {1: 2.0},
        }
        # 25.0% federal tax
        # 8.75% state tax for Maryland residents
        # 7.5% state tax for non-Maryland residents
        self.taxes = {"MD": {"limit": 5000, "rate": .25 + .087}}
        self.wv_pay_off_chart = {
            10: {10: 100000.0, 9: 4000.0, 8: 400.0, 7: 50.0, 6: 10.0, 5: 2.0, 0: 4.0},
            9: {9: 25000.0, 8: 2500.0, 7: 200.0, 6: 25.0, 5: 4.0, 0: 2.0},
            8: {8: 10000.0, 7: 500.0, 6: 50.0, 5: 10.0, 4: 2.0},
            7: {7: 2500.0, 6: 125.0, 5: 15.0, 4: 2.0, 3: 1.0},
            6: {6: 1500.0, 5: 50.0, 4: 5.0, 3: 1.0},
            5: {5: 400.0, 4: 15.0, 3: 2.0},
            4: {4: 50.0, 3: 5.0, 2: 1.0},
            3: {3: 25.0, 2: 2.0},
            2: {2: 10.0},
            1: {1: 2.0},
        }
        self.oh_pay_off_chart = {
            10: {10: 100_000.0, 9: 5_000.0, 8: 500.0, 7: 50.0, 6: 10.0, 5: 2.0, 0: 5.0},
            9: {9: 25_000.0, 8: 2_000.0, 7: 100.0, 6: 20.0, 5: 5.0, 0: 2.0},
            8: {8: 10_000.0, 7: 300.0, 6: 50.0, 5: 15.0, 4: 2.0},
            7: {7: 2000.0, 6: 100.0, 5: 11.0, 4: 5.0, 3: 1.0},
            6: {6: 1100.0, 5: 57.0, 4: 7.0, 3: 1.0},
            5: {5: 410.0, 4: 18.0, 3: 2.0},
            4: {4: 72.0, 3: 5.0, 2: 1.0},
            3: {3: 27.0, 2: 2.0},
            2: {2: 11.0},
            1: {1: 2.0},
        }

    def state_drawing(self) -> List[int]:
        """
        The numbers drawn by state, the winning numbers
        :type:
        """
        return self.machine.draw()
