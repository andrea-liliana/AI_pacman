# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import GameState
from hminimax import HMinimax
from util import Safety, get_safety_of_position,\
                 get_best_food, ghost_in_path


class PacmanAgent(Agent):
    def evaluation_func(self, state: GameState) -> float:
        """Evaluate the utility of a state.

        For this evaluation function, we consider the distance between
        Pacman and the closest food (we consider the walls), the
        number of pills he ate and the dangerosity of its position.

        If there is a wall or a ghost in the path to the food, the
        evaluation is worse.

        Arguments:
        ----------
        - `state`: The state studied.

        Returns:
        --------
        An integer corresponding to the utility of th studied state.
        """
        evaluation = 0
        food_pos, dist_pm_food, wall = get_best_food(state)

        if wall:
            evaluation -= 50

        eaten_pills = self.nb_pills - state.getNumFood()

        evaluation += 50*eaten_pills - dist_pm_food

        if (not wall) and ghost_in_path(state, food_pos):
            evaluation -= 100

        safety = get_safety_of_position(state)
        if safety == Safety.DANGEROUS:
            evaluation -= 100

        return evaluation

    def cutoff_func(self, state: GameState, depth) -> bool:
        """The cutoff function that will prevent the algorithm to
        explore non promising node.

        For this cutoff test we will not explore node beyond a depth
        of 7. We will also stop searching further if Pacman is in an
        safe position (the distance between him and the ghost is
        higher than 2) and that the depth is higher than 2.

        Arguments:
        ----------
        - `state`: The state studied.
        - `depth`: The depth at which the node is beeing explored.

        Returns:
        --------
        A boolean that indicates if the algorithm should continue to
        explore children node.
        """
        safety = get_safety_of_position(state)
        pos_is_safe = (safety == Safety.SAFE or
                       safety == Safety.EXTRA_SAFE)
        return ((pos_is_safe and depth >= 2) or
                depth > 7)

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.hminimax = HMinimax(self.evaluation_func, self.cutoff_func, True)

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
