# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions, GameState
import numpy as np
from a_star import a_star
from pacman_module.util import manhattanDistance
from bayesfilter import get_probable_position_ghost
import random


class PacmanAgent(Agent):
    def __init__(self, args) -> None:
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.target = None
        self.path = None
        self.ghost_pos = []
        self.dest = None

    def _is_target_eaten(self, belief) -> bool:
        """
        Check if the ghost linked to the given belief has already been
        eaten.

        Arguments:
        ----------
        - `belief`: The belief of Pacman regarding a ghost.

        Returns:
        --------
        A boolean indicating if the ghost linked to the given belief
        has been eaten.
        """
        return np.sum(belief) == 0

    def _select_target(self, beliefs, state: GameState) -> bool:
        """
        Select a ghost to chase.

        A compromise has been made to chose between the closest ghost
        and the current chased ghost (to avoid changing of target too
        often).

        Arguments:
        ----------
        - `beliefs`: A list of matrix. Each matrix represent the belief
                     of pacan regarding a ghost.
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Returns:
        --------
        A boolean indicating if the targeted ghost has changed.
        """
        pm_pos = state.getPacmanPosition()

        if self.target is not None and \
                not self._is_target_eaten(beliefs[self.target]):
            target_pos = get_probable_position_ghost(beliefs[self.target])
            target_dist = manhattanDistance(pm_pos, target_pos)
            min_dist = target_dist
        else:
            min_dist = target_dist = None
            self.target = None

        self.ghost_pos = []
        change = False

        for ghost in range(beliefs.shape[0]):
            ghost_pos = get_probable_position_ghost(beliefs[ghost])
            self.ghost_pos.append(ghost_pos)

            dist_pm_gh = manhattanDistance(pm_pos, ghost_pos)

            if min_dist is None or (dist_pm_gh < min_dist and
                                    dist_pm_gh < (0.8*target_dist)):
                if self.target != ghost:
                    change = True
                self.target = ghost
                target_dist = min_dist = dist_pm_gh
                self.dest = ghost_pos

        return change

    def path_to_recompute(self) -> bool:
        """
        Check if the path must be re-computed. If the current
        destination is close to the actual beliefed position of the
        ghost, the path will not be recomputed. This is made to avoid
        too much move repetition.

        Returns:
        --------
        A boolean indicating if the path must be recomputed.
        """
        t_x, t_y = self.dest
        b_x, b_y = self.ghost_pos[self.target]
        return abs(b_x - t_x) > 1 or abs(b_y - t_y) > 1

    def _get_move(self, beliefs, state: GameState) -> Directions:
        """
        Get a move that will make Pacman move toward the adjacent
        position with the highest probability of containing a ghost.

        Arguments:
        ----------
        - `beliefs`: A list of matrix. Each matrix represent the belief
                     of pacan regarding a ghost.
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Returns:
        --------
        A direction indicating where Pacman should go.
        """
        pm_x, pm_y = state.getPacmanPosition()
        adj_cells = {
            (pm_x-1, pm_y): Directions.LEFT,
            (pm_x+1, pm_y): Directions.RIGHT,
            (pm_x, pm_y-1): Directions.SOUTH,
            (pm_x, pm_y+1): Directions.NORTH
        }
        max_proba = 0
        dst = None
        for adj_cell in adj_cells.keys():
            proba_cell = beliefs[self.target, adj_cell[0], adj_cell[1]]
            if proba_cell > max_proba:
                max_proba = proba_cell
                dst = adj_cell

        if not dst:
            return random.choice(state.getLegalPacmanActions())

        return adj_cells[dst]

    def get_action(self, state: GameState, belief_state):
        """
        Given a pacman game state and a belief state,
                returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - `belief_state`: a list of probability matrices.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        # XXX: Your code here to obtain bonus
        changed_target = self._select_target(belief_state, state)

        if changed_target or self.path_to_recompute() or not self.path:
            self.path = a_star(state, self.ghost_pos[self.target])

        if not self.path:
            self.path.append(self._get_move(belief_state, state))

        # XXX: End of your code here to obtain bonus

        return self.path.pop(0)
