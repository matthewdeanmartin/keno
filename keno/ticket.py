# coding=utf-8
"""
All choice that a player makes when buying a ticket.

Some choices are "sucker's bets" and should not be played.
"""
import random
from collections import OrderedDict
from typing import Dict, Union, List, Set

from keno.game import Keno
from keno.number_machine import StaticNumbersMachine
from keno.strategy import Strategy

KENO = Keno()


class Ticket(object):
    """
    Represents all the choices you make on a real ticket.

    Assumes that the exact numbers are not a real choice, that one set of numbers is as good as the next.
    """

    def __init__(self) -> None:
        self.to_go = False
        self.spots = -1
        self.games = -1
        self.bet = -1
        self.bonus = False
        self.super_bonus = False
        self.state = ""

        self._numbers = []  # type: List[int]

        global KENO
        self.rules = KENO
        # actually... you can't buy multiple tickets against same game... hafta buy multiples
        # within same 3 mintues!!
        # self.constant_numbers = False

        self.history = {}  # type: Dict[int, List[str]]
        self.fitness = 0

    def copy(self) -> "Ticket":
        """
        Faster than copy/deepcopy
        :return:
        """
        copy_ticket = Ticket()
        copy_ticket.to_go = self.to_go
        copy_ticket.spots = self.spots
        copy_ticket.games = self.games
        copy_ticket.bet = self.bet
        copy_ticket.bonus = self.bonus
        copy_ticket.super_bonus = self.super_bonus
        copy_ticket.state = self.state

        copy_ticket._numbers = self._numbers
        return copy_ticket

    @property
    def numbers(self) -> List[int]:
        """
        Make sure this doesn't accidentally get mutated.
        :type: dict[str,list[int|bool]]
        """
        if not self._numbers:
            self.pick()
        return self._numbers

    def pick(self) -> None:
        """
        Generate random numbers, but other strategic decisions.
        :return:
        """
        if self.spots < 1 or self.spots > 20:
            raise TypeError("Invalid spot range")
        machine = StaticNumbersMachine(self.spots)
        self._numbers = machine.draw()
        assert len(self.numbers) == self.spots

    def price(self) -> float:
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

    def randomize_ticket(self) -> None:
        """
        Randomize self
        :return:
        """

        validator = TicketValidator()

        i = 0
        while i == 0 or not validator.is_good_ticket(self):
            i += 1
            self.to_go = [True, False][random.randint(0, 2 - 1)]
            ranges = self.rules.ticket_ranges(self.to_go)
            for key, value in ranges.items():
                if key == "to_go":
                    continue
                setattr(self, key, ranges[key][random.randint(0, len(value) - 1)])

            if self.bonus and self.super_bonus and self.state == "MD":
                if random.randint(0, 1) == 1:
                    self.bonus = True
                    self.super_bonus = False
                else:
                    self.bonus = False
                    self.super_bonus = True
            if self.state == "DC":
                self.super_bonus = False
                self.to_go = False

            if i > 200:
                raise TypeError("Can't generate a good ticket!")

    def __str__(self) -> str:
        """
        Pretty printer
        :return:
        """
        result = "----- Ticket ------\n"
        md_keno = Keno()

        for key in sorted(md_keno.ticket_ranges(self.to_go)):
            result += "{0}, {1}".format(key, getattr(self, key))
            result += "\n"
        return result

    def make_save_point(self) -> Dict[str, Union[bool, str, int, float]]:
        """
        Faster than copy/deepcopy
        :return:
        """
        return {
            "to_go": self.to_go,
            "spots": self.spots,
            "games": self.games,
            "bet": self.bet,
            "bonus": self.bonus,
            "super_bonus": self.super_bonus,
            # "_numbers":self.numbers
            "state": self.state,
        }

    def geneticly_merge_ticket(self, ticket: "Ticket", strategy: Strategy) -> None:
        """
        Make this ticket 1/2 like the other ticket
        :type ticket: Ticket
        :type strategy: Strategy
        :return:
        """
        if self == ticket:
            # crossing with a clone.
            return
        save_point = self.make_save_point()

        keys = [x for x in self.rules.ticket_ranges(self.to_go).keys()]
        random.shuffle(keys)
        for key in keys:
            if random.randint(0, 1) == 1:
                if ticket.to_go == self.to_go:
                    setattr(self, key, getattr(ticket, key))
                else:
                    if key in ("to_go", "bet", "games"):
                        setattr(self, "to_go", getattr(ticket, "to_go"))
                        setattr(self, "games", getattr(ticket, "games"))
                        setattr(self, "bet", getattr(ticket, "bet"))
                    else:
                        setattr(self, key, getattr(ticket, key))

        try:
            # This mutant valid?
            validator = TicketValidator()
            validator.check_all_prizes_winnable(self)
            validator.check_ticket(self)
            if not validator.ticket_complies_with_strategy(self, strategy):
                raise TypeError("Invalid ticket")
            if self.price() > strategy.max_ticket_price:
                raise TypeError("too big")
            if self.price() < strategy.minimum_ticket_price:
                raise TypeError("too small")

        except:
            # undo
            for key in keys:
                # setattr(self, key, getattr(save_point, key))
                setattr(self, key, save_point[key])

    def mutate_ticket(self, percent: Union[float, int], strategy: Strategy) -> None:
        """
        Make this ticket change to random property for up to n percent
        :type percent:float
        :type strategy: Strategy
        :return:
        """
        # save_point = copy.deepcopy(self)
        save_point = self.make_save_point()

        mutation_ticket = Ticket()
        mutation_ticket.randomize_ticket()

        features = len(self.rules.ticket_ranges(self.to_go))

        tries = 0
        found_one = False
        while tries < 10 and not found_one:
            try:
                i = 0
                keys = [x for x in self.rules.ticket_ranges(self.to_go).keys()]
                random.shuffle(list(keys))
                for key in keys:
                    i += 1
                    setattr(self, key, getattr(mutation_ticket, key))
                    if i / features > percent:
                        break

                # This mutant valid?
                validator = TicketValidator()
                validator.check_all_prizes_winnable(self)
                validator.check_ticket(self)
                if not validator.ticket_complies_with_strategy(self, strategy):
                    raise TypeError("Invalid ticket")
                if self.price() > strategy.max_ticket_price:
                    raise TypeError("too big")
                if self.price() < strategy.minimum_ticket_price:
                    raise TypeError("too small")
                found_one = True
            except:
                tries += 1
                # undo
                for key in keys:
                    setattr(self, key, save_point[key])

    def __hash__(self) -> int:
        """
        Allow this to be in dictionary for histogram calculations
        :return:
        """
        return hash(
            ":".join(
                list(
                    map(
                        str,
                        [
                            self.to_go,
                            self.spots,
                            self.games,
                            self.bet,
                            self.bonus,
                            self.super_bonus,
                            self.state,
                        ],
                    )
                )
            )
        )

    def __eq__(self, other: "Ticket") -> bool:
        """
        Check equality
        :type other:Ticket
        :rtype:bool
        """
        # numbers & rules ignored right now.
        return (
            self.to_go == other.to_go
            and self.spots == other.spots
            and self.games == other.games
            and self.bet == other.bet
            and self.bonus == other.bonus
            and self.super_bonus == other.super_bonus
            and self.state == other.state
        )

    def calculate_payoff_n_drawings(
        self, ticket: "Ticket", strategy: "Strategy"
    ) -> float:
        """
        A multi-game ticket, just like in MD.
        :type ticket: Ticket
        :return:
        """
        so_far = 0.0
        for i in range(0, ticket.games):
            # each game is a new set of numbers.
            state_drawing = self.rules.state_drawing()
            so_far += self.calculate_payoff_one_drawing(state_drawing, ticket)
            if i > ticket.games:
                raise TypeError("1 off error")

        # NOW we calculate taxes
        state = ticket.state
        prize = so_far
        if not strategy.evade_taxes:
            if state == "MD":
                if prize >= self.rules.taxes[state]["limit"]:
                    so_far = prize * (1 - self.rules.taxes[state]["rate"])

        return so_far

    def calculate_payoff_one_drawing(
        self, state_drawing: List[int], ticket: "Ticket"
    ) -> float:
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
            raise TypeError(
                "wrongly initialized ticket numbers - expected len(n) to match spots"
            )
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

    def check_single_winning(
        self,
        picks: Union[List[int], Set[int]],
        state_drawing: Union[List[int], Set[int]],
    ) -> Set[int]:
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
            cummulative_prob = OrderedDict(
                [
                    (1, 0.4008703648066716),
                    (2, 0.8255574067498794),
                    (3, 0.887489871539253),
                    (4, 0.950046886807054),
                    (5, 0.9876309871721337),
                    (10, 0.9999981791531241),
                ]
            )
            spin = random.uniform(0, 1)
            for key, value in cummulative_prob.items():
                if value < spin:
                    return key
            return 1

        if state == "MD":
            md_odds = {3: 3, 4: 15, 5: 40, 10: 250}
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
        odds = {2: 2.4, 3: 7.1, 4: 3.9, 5: 7.4, 6: 28.2, 10: 160, 12: 310.1, 20: 930.2}
        for key, value in odds.items():
            if random.randint(0, int(value * 10)) < 10:
                return key
        # guaranteed some sort of mutliplier
        return 2

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

    def possible_pay_off_for_ticket_per_game(
        self, ticket: "Ticket"
    ) -> Dict[int, Union[int, float, List[float]]]:
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

    def pay_off_chart(self, ticket: "Ticket") -> Dict[int, Dict[int, float]]:
        """

        :type ticket: Ticket
        :type: dict[dict[int,float]]
        """
        state = ticket.state
        to_go = ticket.to_go

        if state == "MD" and not to_go:
            # wrong place to apply taxes...
            return self.rules.md_pay_off_chart

        if state == "MD" and to_go:
            return self.rules.md_to_go_pay_off_chart

        if state == "DC":
            return self.rules.dc_pay_off_chart

        if state == "WV":
            return self.rules.wv_pay_off_chart
        if state == "OH":
            return self.rules.wv_pay_off_chart
        raise TypeError("Don't know that state")


class TicketValidator(object):
    """
    Check if ticket is valid for MD Keno game
    """

    def __init__(self) -> None:
        self.md_keno = Keno()

    def ticket_complies_with_strategy(self, ticket: Ticket, strategy: Strategy) -> bool:
        """

        :type ticket: Ticket
        :type strategy: Strategy
        :rtype: bool
        """
        price = ticket.price()
        if price > strategy.max_ticket_price:
            return False
        if price < strategy.minimum_ticket_price:
            return False
        if price > strategy.max_loss:
            return False
        # TODO: check if can win the goal.
        return True

    def is_good_ticket(self, ticket: Ticket) -> bool:
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

    def check_ticket(self, ticket: Ticket) -> None:
        """
        Throws on bad tickets
        :type ticket: Ticket
        :rtype: None
        """
        if not ticket.numbers:
            raise TypeError("numbers not initialized")
        if len(ticket.numbers) != ticket.spots:
            raise TypeError("numbers wrongly initialized")

        for key, value in self.md_keno.ticket_ranges(ticket.to_go).items():
            if (
                getattr(ticket, key)
                not in self.md_keno.ticket_ranges(ticket.to_go)[key]
            ):
                raise TypeError(
                    "Bad ticket {0} can be {1}, but got {2}".format(
                        key, value, getattr(ticket, key)
                    )
                )

        # bonus rules
        if ticket.bonus and ticket.super_bonus:
            raise TypeError("Can't do bonus and super bonus at same time.")

        # max ticket rules
        # $100 is the maximum Keno wager per playslip.
        # $200 is the maximum Keno wager per playslip when the Bonus option is selected.
        # $300 is the maximum Keno wager per playslip when the Super Bonus option is selected.
        if ticket.bet * ticket.games > 100:
            raise TypeError(
                "Too much for this slip! ${0}".format(ticket.bet * ticket.games)
            )
        if ticket.bonus and ticket.bet * 2 * ticket.games > 200:
            raise TypeError(
                "Too much for this slip! ${0}".format(ticket.bet * 2 * ticket.games)
            )
        if ticket.super_bonus and ticket.bet * 3 * ticket.games > 300:
            raise TypeError(
                "Too much for this slip ${0}".format(ticket.bet * 3 * ticket.games)
            )

    def check_all_prizes_winnable(self, ticket: Ticket) -> None:
        """
        Throws on bad tickets
        :type ticket: Ticket
        :rtype: None
        """
        # TODO: DC & MD have different max ticket/max drawing limits
        pass
        # don't bet if max prize is unwinnable (
        # pay_off = self.md_keno.pay_off_chart(ticket.state)[ticket.spots][ticket.spots] * ticket.bet
        # if ticket.bonus and pay_off * 10 > 1000000:
        #     raise TypeError("Why? Max payout is 100K")
        # if ticket.bonus and pay_off * 20 > 1000000:
        #     raise TypeError("Why? Max payout is 100K")
