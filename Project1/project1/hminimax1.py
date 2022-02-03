# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import GameState
from hminimax import HMinimax
from util import get_closest_food_distance


class PacmanAgent(Agent):
    def evaluation_func(self, state: GameState) -> float:
        """Evaluate the utility of a state.

        For this evaluation function, we consider the distance between
        Pacman and the closetst food and the number of food that is
        left on the board.

        The further the food is, the worth the evaluation function is.
        The more food there is in the board, the worth the evaluation
        function is.

        Arguments:
        ----------
        - `state`: The state studied.

        Returns:
        --------
        An integer corresponding to the utility of th studied state.
        """
        dist_food = get_closest_food_distance(state)

        evaluation = -50*state.getNumFood() - dist_food

        return evaluation

    def cutoff_func(self, state: GameState, depth: int) -> bool:
        """The cutoff function that will prevent the algorithm to
        explore non promising node.

        For this cutoff test we will not explore node beyond a depth
        of 6.

        Arguments:
        ----------
        - `state`: The state studied.
        - `depth`: The depth at which the node is beeing explored.

        Returns:
        --------
        A boolean that indicates if the algorithm should continue to
        explore children node.
        """
        return depth > 6

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.hminimax = HMinimax(self.evaluation_func,
                                 self.cutoff_func, True)

    def get_action(self, initial_state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `initial_test`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        action = self.hminimax.select_best_option(initial_state)

        return action
