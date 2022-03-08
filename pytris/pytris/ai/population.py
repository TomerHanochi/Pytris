from heapq import nlargest
from random import choices, random
from typing import Dict, List

from pytris.ai.network import Network


class PopulationGenerator:
    def __init__(self, generations: int, population_size: int, network_size: int, mutation_power: float,
                 mutation_chance: float, offspring_percentage: float, parent_candidates_percentage: float) -> None:
        """
        Generates population using the applied fitnesses evaluated during training.
        :param generations: number of populations
        :param population_size: size of each population
        :param network_size: size of the networks inside the population
        :param mutation_power: range to mutate each network by, mutation ∈ [-mutation_power, mutation_power]
        :param mutation_chance: chance for each individual network to mutate
        :param offspring_percentage: percentage of offspring out of population_size
        :param parent_candidates_percentage: percentage of parent candidates out of population_size
        """
        self.__generation = 0
        self.__generations = generations
        self.__population_size = population_size

        self.__networks = {Network.random(network_size): 0 for _ in range(population_size)}

        self.mutation_power = mutation_power
        self.mutation_chance = mutation_chance
        self.num_of_offspring = int(offspring_percentage * population_size)
        self.num_of_parent_candidates = int(parent_candidates_percentage * population_size)

    def __iter__(self) -> 'PopulationGenerator':
        return self

    def __next__(self) -> Dict[Network, float]:
        """ Returns the next population after applying crossover. """
        if self.generation < self.generations:
            if self.generation != 0:
                self.crossover()

            self.__generation += 1
            return self.__networks

        raise StopIteration()

    def crossover(self) -> None:
        """ Picks the strongest networks in the current population, and replaces the weakest with newborn networks. """
        strongest_networks = nlargest(n=self.population_size - self.num_of_offspring,
                                      iterable=self.networks.keys(),
                                      key=lambda network: self.networks[network])
        self.__networks = {child: 0 for child in self.offspring}
        self.__networks.update({network: 0 for network in strongest_networks})

    @property
    def offspring(self) -> List[Network]:
        """
        For each offspring, we randomly select a number of networks from the population, and pick
        the top two networks from the sample. We combine these two networks using the following formula:
        if w = parent1_weights * parent1_fitness + parent2_weights * parent2_fitness
        then child_weights = w / |w|
        Then, there is a random chance to mutate the child network, altering its values by a certain amount.
        :return: List of newly generated networks
        """
        offspring = list()
        all_candidates = list(self.networks.items())
        for _ in range(self.num_of_offspring):
            (parent1, fitness1), (parent2, fitness2) = nlargest(n=2, key=lambda pair: pair[1],
                                                                iterable=choices(all_candidates,
                                                                                 k=self.num_of_parent_candidates))
            child = Network(parent1.weights * fitness1 + parent2.weights * fitness2)

            if random() < self.mutation_chance:
                child.mutate(self.mutation_power)

            offspring.append(child)
        return offspring

    @property
    def networks(self) -> Dict[Network, float]:
        """ A dict of a network mapped to its fitness. """
        return self.__networks

    @property
    def generation(self) -> int:
        return self.__generation

    @property
    def generations(self) -> int:
        return self.__generations

    @property
    def population_size(self) -> int:
        return self.__population_size
