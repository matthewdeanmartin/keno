# coding=utf-8
"""
Poorly named, this is the main code.
"""
import multiprocessing
import sys
from collections import OrderedDict, namedtuple
from functools import partial
from multiprocessing.pool import Pool

from keno.evolutionary_parameters import EvolutionParameters
from keno.game import Keno
from keno.player import Player
from keno.strategy import Strategy
from keno.ticket import Ticket

KENO = Keno()

Life = namedtuple('Life', ['ticket', 'fitness'], verbose=False)


def simulate(ticket, strategy):
    player = Player(strategy)
    # override ticket
    player.ticket = ticket
    house, played = player.go()
    return house, played, player

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
        self.generations = {}  # generation: ticket
        self.true_winners = {}  # generation: list(Ticket)

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

            # This keeps the initial pop too small for a genetic algo!
            # if ticket in self.tickets:
            #     continue

            # TODO: check minimum winning on 1 ticket!!

            # don't waste time on these tickets
            if ticket.price() > self.strategy.max_ticket_price:
                continue
            if ticket.price() < self.strategy.minimum_ticket_price:
                continue
            if ticket.state not in self.strategy.state_range:
                continue

            self.tickets.append(ticket)

        if not self.tickets:
            raise TypeError("No possible valid tickets? Something must be wrong.")

        while len(self.tickets) < self.evolution_parameters.max_ticket_types:
            print("Not enough tickets with unique individuals, puffing up with dupes have {0}. Need {1}".format(
                len(self.tickets), self.evolution_parameters.max_ticket_types))
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
        self.generations = {
            0: lives,
        }
        """:type: dict[int,list[Life]]"""
        self.true_winners = {
            0: lives
        }
        for generation in range(0, self.evolution_parameters.max_generations):
            print("Generation {0}".format(generation))
            # round 2+, iterate winners, not orig tickets

            # track all generations
            current_lives = self.generations[generation]
            self.generations[generation + 1] = []

            i = 0
            print("Now playing {0} tickets ".format(len(current_lives)))

            # if House net is strongly negative after lots of plays, this is a BUG!
            house_net = 0
            drawing_count = 0

            playable = []
            for ticket, _ in current_lives:
                i += 1

                # need to be able to win 1/2 as much as target in single winning.
                if not self.keno.can_i_win_this_much(ticket, self.strategy.sufficient_winnings/2):
                    # loser ticket.
                    continue
                if ticket.price() > self.strategy.max_ticket_price:
                    # costs too much now... loser
                    continue
                playable.append(ticket)


            workers = multiprocessing.cpu_count()
            chunksize = int(len(playable) / workers)

            if not playable:
                print("All tickets suck")
                self.print_results()
                print("Early termination")
                break

            with Pool(processes=workers) as pool:
                results = pool.map(partial(simulate, strategy=self.strategy), playable, chunksize)

            for house, played, player in results:
                # this is the fitness function, currently binary (good/not good)

                house_net += house
                drawing_count += played
                if drawing_count > 15000 and house_net < 0:
                    pass
                    # raise TypeError("WTF, the house is losing money!")
                if player.good_game():
                    self.generations[generation + 1].append(Life(player.ticket, player.evolutionary_fitness()))
                    self.report_good_games(i, player, player.ticket)

            remaining = len(self.generations[generation + 1])
            self.true_winners[generation + 1] = self.generations[generation + 1]
            print("\nRemaining winners: {0}".format(remaining))


            if generation == self.evolution_parameters.max_generations:
                # don't add mutants, etc to final generation!
                break

            upcoming_generation = self.generations[generation + 1]

            if not self.generations[generation + 1]:
                print("Ran out of good tickets")
                break
            # TODO: reward better with more slots in next generation
            while len(self.generations[generation + 1]) < self.evolution_parameters.max_ticket_types:
                print("Puffing up population of tickets-- have {0}, need {1}"
                      .format(len(self.generations[generation + 1]),
                              self.evolution_parameters.max_ticket_types))

                split_on = int(len(self.generations[generation + 1]) / 2)
                top = sorted(self.generations[generation + 1], key=lambda x: x.fitness)[0:split_on]
                bottom = sorted(self.generations[generation + 1], key=lambda x: x.fitness)[split_on:]
                to_add = []
                for life in top:
                    # range(0,2) == [0,1]
                    for _ in range(0, self.evolution_parameters.fitness_bonus):
                        to_add.append(life)

                for life in bottom:
                    to_add.append(life)

                self.generations[generation + 1].extend(to_add)

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
                                                                     self.strategy)

        print("Mutating Tickets")
        if len(upcoming_generation) > 1000:
            # don't mutate all, mutation is very deadly.
            for ticket, fitness in upcoming_generation[0:500]:
                ticket.mutate_ticket(self.evolution_parameters.mutation_percent, self.strategy)

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
        last_generation = max(self.true_winners.keys())
        for life in self.true_winners[last_generation]:
            ticket = life.ticket
            if ticket in histo.keys():
                histo[ticket] += 1
            else:
                histo[ticket] = 1

        # sort by fitness
        d_descending = OrderedDict(sorted(histo.items(),
                                          key=lambda x: x[1], reverse=False))

        i = 0
        for winning_ticket, occurance in d_descending.items():
            i += 1
            if i < len(d_descending) - 5:
                continue
            print("------Occurance in final generation {0}------".format(occurance))
            print(winning_ticket)
            print("Ticket Price: {0}".format(winning_ticket.price()))
            print("Fitness (net winnigs): {0}".format(winning_ticket.fitness))
            print("History: {0}".format(winning_ticket.history))
            print("Payoff range " + str(self.keno.possible_pay_off_for_ticket_per_game(winning_ticket)))
            print("-----")


if __name__ == "__main__":
    def run():
        """
        Exercise code
        :return:
        """
        runner = GameRunner(Strategy(state_range=["MD", "DC", "WV", "OH"],
                                     min_ticket_price=0,
                                     max_ticket_price=50,

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
