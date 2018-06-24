# coding=utf-8
"""
How to do the genetic algo
"""
from typing import Union


class EvolutionParameters(object):
    """
    How will the game of evolution work
    """

    def __init__(
        self,
        max_ticket_types: int,
        max_generations: int,
        mutation_percent: float,
        fitness_bonus: int,
    ) -> None:
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
        self.percent_of_population_to_mutate = .5

        # Evolution moves faster if best get a bigger bonus
        self.fitness_bonus = fitness_bonus

        # minimum to survive a culling round
        self.minimum_survivors = 10
