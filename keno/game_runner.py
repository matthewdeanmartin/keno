# coding=utf-8
"""
Poorly named, this is the main code.
"""
import copy
import sys
from collections import OrderedDict

from keno.game import Keno
from keno.player import Player
from keno.ticket import Ticket

KENO = Keno()
class GameRunner(object):
    """
    Represents top level config for similation
    """
    def __init__(self, max_ticket_price,
                 max_ticket_types, max_plays_with_ticket_type,
                 max_loss, sufficient_winnings, max_generations):
        """

        :type max_ticket_price: int
        :type max_ticket_types: int
        """
        # vacuously, the more you bet, the more likley you are to win something
        # This simulator isn't instrested in demonstrating that if you bet a lot
        # you maximize your odds of wining something.
        self.max_ticket_price = max_ticket_price
        # If a ticket takes 100 years to pay off, then who cares?
        self.max_plays_with_ticket_type = max_plays_with_ticket_type
        # How much is a player willing to lose (i.e. when is gambler's ruin?)
        self.max_loss = max_loss
        # How much do you want to win (i.e. a ticket that regularly wins $2 isn't exciting)
        self.suffient_winnings = sufficient_winnings

        # respresents strategies/ticket choices
        self.max_ticket_types = max_ticket_types
        self.tickets = []

        self.max_generations = max_generations

        # Stores each generation
        self.winners = None

        # TODO: Maybe implement Keno of other states.
        global  KENO
        self.keno = KENO

    def generate_tickets(self):
        """
        possibly inefficient way of generating all possible tickets.
        I'm not sure how big the total space is.
        """

        print("Generating tickets...")
        sys.stdout.flush()
        for i in range(0, self.max_ticket_types):
            ticket = Ticket()
            ticket.randomize_ticket()
            if ticket in self.tickets:
                continue
            # TODO: check minimum winning on 1 ticket!!

            if ticket.price() > self.max_ticket_price:
                continue

            self.tickets.append(ticket)

        while len(self.tickets) < self.max_ticket_types:
            print("Not enough tickets with unique individuals, puffing up with dupes")
            self.tickets.extend(self.tickets)

        print("Have {0} tickets. Now ready to play".format(len(self.tickets)))
        sys.stdout.flush()

    def run(self):
        """
        Execute main simulator
        :return:
        """
        self.generate_tickets()

        self.winners = {
            0: self.tickets,
        }
        """:type: dict[int,list[Ticket]]"""


        for generation in range(0, self.max_generations):
            print("Generation {0}".format(generation))
            # round 2+, iterate winners, not orig tickets

            # track all generations
            current_tickets = self.winners[generation]
            self.winners[generation + 1] = []

            i = 0
            print("Now playing {0} tickets ".format(len(current_tickets)))

            # if House net is strongly negative after lots of plays, this is a BUG!
            house_net = 0
            drawing_count = 0
            for ticket in current_tickets:
                i += 1
                jackpot = 2500
                if not self.keno.can_i_win_this_much(ticket, jackpot):
                    # loser ticket.
                    continue
                if ticket.price() > self.max_ticket_price:
                    # costs too much now... loser
                    continue

                player = Player(self.max_loss, self.suffient_winnings, self.max_plays_with_ticket_type)
                # override ticket
                player.ticket = ticket

                house, played = player.go()
                house_net += house
                drawing_count += played
                if drawing_count > 15000 and house_net < 0:
                    pass
                    # raise TypeError("WTF, the house is losing money!")
                if player.good_game():
                    self.winners[generation + 1].append(ticket)
                    self.report_good_games(i, player, ticket)

                    # print(ticket)
                    # print("Ticket Price: {0}".format(ticket.price()))
                    # print(player)
                    # print("-----")
                    # print(md_keno.possible_pay_off_for_ticket_per_game(ticket))

            remaining = len(self.winners[generation + 1])
            print("Remaining winners: {0}".format(remaining))
            if remaining == 0:
                print("All tickets suck")
                break


            upcoming_generation = self.winners[generation + 1]

            while len(self.winners[generation + 1]) < self.max_ticket_types:
                print("Puffing up population of tickets")
                self.winners[generation + 1].extend(self.winners[generation + 1])

            if len(upcoming_generation) >= 3:
                self.cross_and_mutate(upcoming_generation)
            else:
                print("Not enough tickets left for genetic activity")
                break
            sys.stdout.flush()

        self.print_results()

    def cross_and_mutate(self, upcoming_generation):
        print("Crossing Tickets")
        for index in range(0, len(upcoming_generation) - 1, 2):
            upcoming_generation[index].geneticly_merge_ticket(upcoming_generation[index + 1], self.max_ticket_price)
        print("Mutating Tickets")
        if len(upcoming_generation) > 1000:
            # don't mutate all, mutation is very deadly.
            for ticket in upcoming_generation[0:500]:
                ticket.mutate_ticket(.1)
        # children, otherwise pop shrinks too fast
        if len(upcoming_generation) < len(self.tickets) + 500:
            children = []
            for ticket in upcoming_generation:
                children.append(copy.deepcopy(ticket))

            upcoming_generation.extend(children)

    def report_good_games(self, i, player, ticket):
        if i < 6:
            print("------Good Game------ paid-{0}, won(net) {1}".format(
                str(ticket.price() * player.tickets_played),
                player.net_winnings))
            print(player.history)
        else:
            print('.', end='')

    def print_results(self):
        """
        Show best tickets. Ignore worst
        :return:
        """
        histo = {}
        for winner in self.winners[max(self.winners.keys())]:
            if winner in histo.keys():
                histo[winner] += 1
            else:
                histo[winner] = 1

        d_descending = OrderedDict(sorted(histo.items(),
                                          key=lambda x: x[1], reverse=False))

        i = 0
        for winner, occurance in d_descending.items():
            i += 1
            if i < len(d_descending) - 5:
                continue
            print("------{0}------".format(occurance))
            print(winner)
            print("Ticket Price: {0}".format(winner.price()))
            print("Payoff range " + str(self.keno.possible_pay_off_for_ticket_per_game(winner)))
            print("-----")


if __name__ == "__main__":
    def run():
        runner = GameRunner(max_ticket_price=50,
                            max_ticket_types=5000,
                            max_plays_with_ticket_type=200,
                            max_loss=5000,
                            sufficient_winnings=10000,
                            max_generations=4)
        runner.run()


    run()
