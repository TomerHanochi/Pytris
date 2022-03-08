import os
from datetime import datetime
from multiprocessing import Pool
from typing import Callable

from tqdm import tqdm

from pytris.ai.network import Network
from pytris.ai.population import PopulationGenerator


class Trainer:
    @staticmethod
    def run(generations: int, population_size: int, network_size: int, mutation_power: float, mutation_chance: float,
            offspring_percentage: float, parent_candidates_percentage: float, evaluation_function: Callable[[Network], float],
            log_folder: str = None, concurrency: int = None) -> None:
        """
        Finds the best network in a population across multiple generations according to the specified evaluation_function.
        :param generations: number of populations
        :param population_size: size of each population
        :param network_size: size of the networks inside the population
        :param mutation_power: range to mutate each network by, mutation ∈ [-mutation_power, mutation_power]
        :param mutation_chance: chance for each individual network to mutate
        :param offspring_percentage: percentage of offspring out of population_size
        :param parent_candidates_percentage: percentage of parent candidates out of population_size
        :param evaluation_function: function that receives a network and outputs its fitness
        :param log_folder: folder to upload log file to
        :param concurrency: number of concurrent processes to run
        """
        if log_folder is None:
            log_folder = os.path.curdir

        filename = f'{datetime.now().strftime("%d-%m-%y_%H:%M:%S")}.txt'
        with open(os.path.join(log_folder, filename), 'w') as f:
            with Pool(concurrency) as pool:
                population_generator = PopulationGenerator(generations, population_size, network_size, mutation_power,
                                                           mutation_chance, offspring_percentage, parent_candidates_percentage)
                for population in population_generator:
                    fitnesses = {network: pool.apply_async(evaluation_function, args=(network,))
                                 for network in population}

                    epoch = f'Epoch {population_generator.generation}/{population_generator.generations}'
                    for network, fitness in tqdm(fitnesses.items(), desc=epoch):
                        population[network] = fitness.get()

                    network, fitness = max(population.items(), key=lambda pair: pair[1])
                    f.write(f'epoch {population_generator.generation}:\n'
                            f'   top fitness: {fitness}\n'
                            f'   top weights: {network.weights}\n')
