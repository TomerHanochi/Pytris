import os

from pytris import Tetris
from pytris.ai.algorithm import generate_best_move
from pytris.ai.network import Network
from pytris.ai.trainer import Trainer


def tetris_evaluation(network: Network) -> float:
    """ Returns the number of lines cleared in 'n' moves and 'm' games. """
    fitness = 0
    tetris = Tetris(10, 20)
    num_of_games = 3
    num_of_moves = 100
    for _ in range(num_of_games):
        tetris.reset()
        for _ in range(num_of_moves):
            if tetris.terminal:
                break

            best_move, use_alt_move = generate_best_move(tetris, network)
            if use_alt_move:
                tetris.hold()

            for _ in range(best_move.rotation):
                tetris.rotate_right()

            for _ in range(best_move.right):
                tetris.move_right()

            for _ in range(best_move.left):
                tetris.move_left()

            tetris.hard_drop()
            tetris.lock()
        fitness += tetris.cleared_lines
    return fitness


def main() -> None:
    log_folder = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    Trainer.run(generations=3, population_size=50, network_size=4, mutation_power=.3, mutation_chance=.75,
                offspring_percentage=.5, parent_candidates_percentage=.3, evaluation_function=tetris_evaluation,
                log_folder=log_folder, concurrency=36)


if __name__ == '__main__':
    main()
