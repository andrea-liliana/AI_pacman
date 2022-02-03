# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import GameState
import sys
from hminimax import HMinimax


class PacmanAgent(Agent):
    def evaluation_func(self, state: GameState) -> float:
        """Minimax does not use evaluation function."""
        sys.exit("Minimax does not use heuristic.",
                 "This function should never be used.")

    def cutoff_func(self, state: GameState, max_depth: int) -> bool:
        """Minimax does not use cutoff."""
        return False

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self._hminimax = HMinimax(self.evaluation_func, self.cutoff_func)

    def get_action(self, initial_state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `initial_state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        action = self._hminimax.select_best_option(initial_state)

        return action
