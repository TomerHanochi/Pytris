import time
from functools import cached_property
from typing import Dict

from pytris import Tetris
from pytris.ai.algorithm import generate_best_move
from pytris.ai.network import Network
from pytris.utils.vector import Vector


class TetrisController:
    def __init__(self, width: int, height: int) -> None:
        self.__tetris = Tetris(width, height)
        self.__time_since_move_down = 0
        self.__time_since_cant_move_down = 0
        self.__move_right = False
        self.__time_since_move_right = 0
        self.__move_left = False
        self.__time_since_move_left = 0
        self.__rotate_right = False
        self.__time_since_rotate_right = 0
        self.__rotate_left = False
        self.__time_since_rotate_left = 0
        self.__soft_drop = False
        self.__time_since_soft_drop = 0

        self.__paused = False
        self.__time_since_pause = 0

        self.__use_ai = False

    def ai(self) -> None:
        """ Lets the Algorithm generate the best move and does it. """
        best_move, use_alt_move = generate_best_move(self.__tetris, self.network)

        if use_alt_move:
            self.__tetris.hold()

        for _ in range(best_move.rotation):
            self.__tetris.rotate_right()

        for _ in range(best_move.right):
            self.__tetris.move_right()

        for _ in range(best_move.left):
            self.__tetris.move_left()

        self.__tetris.hard_drop()
        self.__tetris.lock()

    def player(self) -> None:
        """ Controls movement cooldowns for the player. """
        now = time.perf_counter()
        if self.__move_right and now - self.__time_since_move_right > self.move_horizontal_cooldown:
            self.__tetris.move_right()
            self.__time_since_move_right = now

        if self.__move_left and now - self.__time_since_move_left > self.move_horizontal_cooldown:
            self.__tetris.move_left()
            self.__time_since_move_left = now

        if self.__rotate_right and now - self.__time_since_rotate_right > self.rotate_cooldown:
            self.__tetris.rotate_right()
            self.__time_since_rotate_right = now

        if self.__rotate_left and now - self.__time_since_rotate_left > self.rotate_cooldown:
            self.__tetris.rotate_left()
            self.__time_since_rotate_left = now

        if self.__soft_drop and now - self.__time_since_soft_drop > self.soft_drop_cooldown:
            self.__tetris.soft_drop()
            self.__time_since_soft_drop = now

        if now - self.__time_since_move_down > self.move_down_cooldown:
            self.__tetris.move_down()
            self.__time_since_move_down = now

        if not self.__tetris.can_move_down:
            if self.__time_since_cant_move_down == 0:
                self.__time_since_cant_move_down = now
            elif not (self.__tetris.can_move_right or self.__tetris.can_move_left) \
                    or now - self.__time_since_cant_move_down > self.lock_delay:
                self.__tetris.lock()
                self.__time_since_cant_move_down = 0

    def update(self) -> None:
        if self.__tetris.terminal or self.paused:
            return

        if self.use_ai:
            self.ai()
        else:
            self.player()

    def start_move_right(self) -> None:
        self.__move_right = True

    def stop_move_right(self) -> None:
        self.__move_right = False

    def start_move_left(self) -> None:
        self.__move_left = True

    def stop_move_left(self) -> None:
        self.__move_left = False

    def start_soft_drop(self) -> None:
        self.__soft_drop = True

    def stop_soft_drop(self) -> None:
        self.__soft_drop = False

    def start_rotate_right(self) -> None:
        self.__rotate_right = True

    def stop_rotate_right(self) -> None:
        self.__rotate_right = False

    def start_rotate_left(self) -> None:
        self.__rotate_left = True

    def stop_rotate_left(self) -> None:
        self.__rotate_left = False

    def hard_drop(self) -> None:
        self.__tetris.hard_drop()

    def hold(self) -> None:
        self.__tetris.hold()

    def reset(self) -> None:
        self.__tetris.reset()

    def pause_or_resume(self) -> None:
        """ Pauses or resumes the game, updates cooldowns accordingly. """
        if self.paused:
            elapsed_time = time.perf_counter() - self.__time_since_pause
            self.__time_since_move_right += elapsed_time
            self.__time_since_move_left += elapsed_time
            self.__time_since_rotate_right += elapsed_time
            self.__time_since_rotate_left += elapsed_time
            self.__time_since_soft_drop += elapsed_time
            self.__time_since_move_down += elapsed_time
        else:
            self.__time_since_pause = time.perf_counter()
        self.__paused = not self.__paused

    def switch_use_ai(self) -> None:
        self.__use_ai = not self.use_ai

    @property
    def move_down_cooldown(self) -> float:
        return (0.807 - self.__tetris.level * 0.007) ** (self.__tetris.level - 1)

    @property
    def soft_drop_cooldown(self) -> float:
        return 0.05

    @property
    def move_horizontal_cooldown(self) -> float:
        return 0.15 - self.__tetris.level * 0.005

    @property
    def rotate_cooldown(self) -> float:
        return 0.2

    @property
    def lock_delay(self) -> float:
        return self.move_horizontal_cooldown

    @property
    def paused(self) -> bool:
        return self.__paused

    @property
    def use_ai(self) -> bool:
        return self.__use_ai

    @cached_property
    def network(self) -> Network:
        """ The best network found during training. """
        return Network(Vector((-0.7197158631719868, 0.593281303546271, -0.22543477397177927, -0.281434777249245)))

    def to_json(self) -> Dict:
        return self.__tetris.to_json()
