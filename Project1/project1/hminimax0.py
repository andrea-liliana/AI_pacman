# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import GameState
from hminimax import HMinimax
from pacman_module.util import manhattanDistance


class PacmanAgent(Agent):
    def evaluation_func(self, state: GameState) -> float:
        """Evaluate the utility of a state.

        For this evaluation function, we consider the distance between
        Pacman and the food (we consider all the food) and the number
        of pills he ate.

        The further the food is, the worth the evaluation function is.

        Arguments:
        ----------
        - `state`: The state studied.

        Returns:
        --------
        An integer corresponding to the utility of th studied state.
        """
        pacman_pos = state.getPacmanPosition()
        evaluation = 0
        for food_pos in state.getFood().asList():
            evaluation -= manhattanDistance(pacman_pos, food_pos)

        eaten_pills = self.nb_pills - state.getNumFood()

        evaluation += 20*eaten_pills

        return evaluation

    def cutoff_func(self, state: GameState, depth: int) -> bool:
        """The cutoff function that will prevent the algorithm to
        explore non promising node.

        For this cutoff test we will not explore node beyond a depth
        of 7

        Arguments:
        ----------
        - `state`: The state studied.
        - `depth`: The depth at which the node is beeing explored.

        Returns:
        --------
        A boolean that indicates if the algorithm should continue to
        explore children node.
        """
        return depth > 7

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
        self.nb_pills = initial_state.getNumFood()

        action = self.hminimax.select_best_option(initial_state)
        return action
