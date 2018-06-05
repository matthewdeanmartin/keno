# coding=utf-8
"""
Poorly named, this is the main code.
"""
import sys
from collections import OrderedDict, namedtuple

from keno.game import Keno
from keno.player import Player
from keno.ticket import Ticket

KENO = Keno()

Life = namedtuple('Life', ['ticket', 'fitness'], verbose=False)


class Strategy(object):
    """
    Represents the player's risk tollerances.
    (Not the simulated player's risk tollerances!)
    """

    def __init__(self, max_ticket_price,
                 max_plays_with_ticket_type,
                 max_loss, sufficient_winnings):
        """
        Initialize self
        :type max_ticket_price: int
        :type max_plays_with_ticket_type: int
        :type max_loss: int
        :type sufficient_winnings: int
        """
        if max_loss < max_ticket_price:
            raise TypeError("Max loss > max ticket price, you know tickets often end in 0 winnings?")

        # has a relationship to max_loss
        # games also put limits on price of single ticket
        self.max_ticket_price = max_ticket_price

        # If a ticket takes 100 years to pay off, then who cares?
        self.max_plays_with_ticket_type = max_plays_with_ticket_type

        # How much is a player willing to lose (i.e. when is gambler's ruin?)
        self.max_loss = max_loss

        # How much do you want to win (i.e. a ticket that regularly wins $2 isn't exciting)
        self.sufficient_winnings = sufficient_winnings


class EvolutionParameters(object):
    """
    How will the game of evolution work
    """

    def __init__(self, max_ticket_types, max_generations, mutation_percent, fitness_bonus):
        """
        Initialize self
        :type max_ticket_types: int
        :type max_generations: int
        :type mutation_percent: float
        :type fitness_bonus: int
        """
        # respresents strategies/ticket choices, initial population variety
        self.max_ticket_types = max_ticket_types

        # how many rounds of playing/culling/crossing/mutating
        self.max_generations = max_generations

        # mutate too much and you get a loser
        self.mutation_percent = mutation_percent

        # Evolution moves faster if best get a bigger bonus
        self.fitness_bonus = fitness_bonus


class GameRunner(object):
    """
    Represents top level config for similation
    """

    def __init__(self, strategy, evolution_parameters):
        """
        Initialize values
        :type strategy: Strategy
        :type evolution_parameters: EvolutionParameters
        """
        # vacuously, the more you bet, the more likley you are to win something
        # This simulator isn't instrested in demonstrating that if you bet a lot
        # you maximize your odds of wining something.
        self.strategy = strategy
        self.evolution_parameters = evolution_parameters

        self.tickets = []

        # Stores each generation
        self.winners = None

        # TODO: Maybe implement Keno of other states.
        global  KENO
        self.keno = KENO

    def generate_initial_population(self):
        """
        possibly inefficient way of generating all possible tickets.
        I'm not sure how big the total space is.
        """

        print("Generating tickets...")
        sys.stdout.flush()
        for _ in range(0, self.evolution_parameters.max_ticket_types):
            ticket = Ticket()
            ticket.randomize_ticket()
            if ticket in self.tickets:
                continue
            # TODO: check minimum winning on 1 ticket!!

            # don't waste time on these tickets
            if ticket.price() > self.strategy.max_ticket_price:
                continue

            self.tickets.append(ticket)

        while len(self.tickets) < self.evolution_parameters.max_ticket_types:
            print("Not enough tickets with unique individuals, puffing up with dupes")
            self.tickets.extend(self.tickets)

        print("Have {0} tickets. Now ready to play".format(len(self.tickets)))
        sys.stdout.flush()

    def run(self):
        """
        Execute main simulator
        :return:
        """
        self.generate_initial_population()

        lives = [Life(t, 0) for t in self.tickets]
        self.winners = {
            0: lives,
        }
        """:type: dict[int,list[Life]]"""

        for generation in range(0, self.evolution_parameters.max_generations):
            print("Generation {0}".format(generation))
            # round 2+, iterate winners, not orig tickets

            # track all generations
            current_lives = self.winners[generation]
            self.winners[generation + 1] = []

            i = 0
            print("Now playing {0} tickets ".format(len(current_lives)))

            # if House net is strongly negative after lots of plays, this is a BUG!
            house_net = 0
            drawing_count = 0
            for ticket, fitness in current_lives:
                i += 1
                jackpot = 2500
                if not self.keno.can_i_win_this_much(ticket, jackpot):
                    # loser ticket.
                    continue
                if ticket.price() > self.strategy.max_ticket_price:
                    # costs too much now... loser
                    continue

                player = Player(self.strategy)
                # override ticket
                player.ticket = ticket

                # this is the fitness function, currently binary (good/not good)
                house, played = player.go()
                house_net += house
                drawing_count += played
                if drawing_count > 15000 and house_net < 0:
                    pass
                    # raise TypeError("WTF, the house is losing money!")
                if player.good_game():
                    self.winners[generation + 1].append(Life(ticket, player.evolutionary_fitness()))
                    self.report_good_games(i, player, ticket)

            remaining = len(self.winners[generation + 1])
            print("Remaining winners: {0}".format(remaining))
            if remaining == 0:
                print("All tickets suck")
                break

            if generation == self.evolution_parameters.max_generations:
                # don't add mutants, etc to final generation!
                break

            upcoming_generation = self.winners[generation + 1]

            # TODO: reward better with more slots in next generation
            while len(self.winners[generation + 1]) < self.evolution_parameters.max_ticket_types:
                print("Puffing up population of tickets")

                split_on = int(len(self.winners[generation + 1]) / 2)
                top = sorted(self.winners[generation + 1], key=lambda x: x.fitness)[0:split_on]
                bottom = sorted(self.winners[generation + 1], key=lambda x: x.fitness)[split_on:]
                to_add = []
                for life in top:
                    # range(0,2) == [0,1]
                    for _ in range(0,self.evolution_parameters.fitness_bonus):
                        to_add.append(life)

                for life in bottom:
                    to_add.append(life)

                self.winners[generation + 1].extend(to_add)

            if len(upcoming_generation) >= 3:
                self.cross_and_mutate(upcoming_generation)
            else:
                print("Not enough tickets left for genetic activity")
                break
            sys.stdout.flush()

        self.print_results()

    def cross_and_mutate(self, upcoming_generation):
        """
        Simulate biology
        :type upcoming_generation: list[Life]
        :return:
        """
        print("Crossing Tickets")
        # merge pairs
        for index in range(0, len(upcoming_generation) - 1, 2):
            # cross tickets & immediately remove overpriced
            upcoming_generation[index].ticket.geneticly_merge_ticket(upcoming_generation[index + 1].ticket,
                                                                     self.strategy.max_ticket_price)

        print("Mutating Tickets")
        if len(upcoming_generation) > 1000:
            # don't mutate all, mutation is very deadly.
            for ticket, fitness in upcoming_generation[0:500]:
                ticket.mutate_ticket(self.evolution_parameters.mutation_percent)

        # children, otherwise pop shrinks too fast
        if len(upcoming_generation) < len(self.tickets) + 500:
            children = []
            for ticket, fitness in upcoming_generation:
                children.append(Life(ticket.copy(), fitness))

            upcoming_generation.extend(children)

    def report_good_games(self, i, player, ticket):
        """
        Diagnostics
        :type i: int
        :type player: Player
        :type ticket: Ticket
        :return:
        """
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
            print(winner.ticket)
            print("Ticket Price: {0}".format(winner.ticket.price()))
            print("Fitness (net winnigs): {0}".format(winner.fitness))
            print("Payoff range " + str(self.keno.possible_pay_off_for_ticket_per_game(winner.ticket)))
            print("-----")


if __name__ == "__main__":
    def run():
        """
        Exercise code
        :return:
        """
        runner = GameRunner(Strategy(max_ticket_price=50,

                                     max_plays_with_ticket_type=200,
                                     max_loss=5000,
                                     sufficient_winnings=10000),
                            EvolutionParameters(
                                max_ticket_types=5000,
                                max_generations=4,
                                mutation_percent=.2,
                                fitness_bonus=2))
        runner.run()


    run()
