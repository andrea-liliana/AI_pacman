from pacman_module.pacman import GameState
from node import Node, key
from players import Players
from pacman_module.game import Directions
import sys
from collections.abc import Callable
from typing import Optional
from a_star import a_star


def get_next_player(current_player: Players) -> Players:
    """Get the player that is going to play next.

    As we only consider a 2 player game, it symply returns the other
    player.
    This function can exit the program if the given player does not
    exists.

    Arguments:
    ----------
    - `current_player`: the player of this turn.

    Returns:
    --------
    A Player, representing the player that will play the next turn.
    """
    if current_player == Players.PACMAN:
        return Players.GHOST
    elif current_player == Players.GHOST:
        return Players.PACMAN
    else:
        sys.exit("Given player does not exist")


class HMinimax:
    """A class to factorize the code of hminimax.

    A class is used to store all information related to hminimax.
    As only the cutoff test and the evaluation function change,
    we can give these functions to the constructor to appply
    minimax with them.

    To speed up the process, alpha-beta prunning is used. It
    does not replace the cutoff test. It is just to speed up the
    process.

    Some changes to the original algorithm have been made.
    First of all, as the depth can be used as a cutoff, we will
    count the depth. We could give the maximum authorized depth
    to the minimax function, but then, this test would not be in
    the cutoff function, and it can be confusing.
    We prefered an increasing depth that stoped when it goes too deep
    to a maximum depth that decrease until it reachs 0.

    The methods `min_player_step` and `min_player_step` can easily be
    factorized but we wanted to keep those steps apparts to ease the
    comprehension.

    Attributes:
    ----------
    - `eval_func`: The evaluation function that will be used to
                   estimate the utility of a state.
    - `cutoff_func`: The cutoof test that will be used to determine
                     if it is worth to explore the following nodes.
    - `explored_nodes`: A list of ids of explored states.

    Methods:
    --------
    - `select_best_option`
    - `hminimax`
    - `hminimax_step`
    - `max_player_step`
    - `min_player_step`
    - `suicide`
    - `path_to_ghost`
    """

    def __init__(self,
                 eval_func: Callable[[GameState], float],
                 cutoff_func: Callable[[GameState, int], bool],
                 consider_stop: bool = False) -> None:
        """The constructor of the class.

        Arguments:
        ----------
        - `eval_func`: The evaluation function that will be used to
                   estimate the utility of a state.
        - `cutoff_func`: The cutoof test that will be used to determine
                     if it is worth to explore the following nodes.

        Returns:
        --------
        An `HMinimax` instance.
        """
        self.eval_func = eval_func
        self.cutoff_func = cutoff_func
        self.explored_nodes = dict()
        self.consider_stop = consider_stop
        self.suicide = False
        self.path_to_ghost = []

    def select_best_option(self,
                           state: GameState) -> Optional[Directions]:
        """Select the best action to do to maximize the score.

        To select this action, this function uses minimax with
        alpha-beta prunning, an evaluation function, and a cutoff-test.

        Pacman is the max player and the ghost is the min player.

        Arguments:
        ----------
        - `state`: The current state of the game.

        Returns:
        --------
        A `Directions`, corresponding to the next direction where
        pacman should go.
        """
        current_node = Node(state)

        if self.explored_nodes.keys():
            current_node.ancestors = set(self.explored_nodes.keys())

        next_node = self.hminimax(current_node, Players.PACMAN, 0)

        if next_node is None:
            # A loop is detected
            # We decided to make Pacman die
            action = Directions.STOP
            if not self.suicide:
                self.suicide = True
                self.path_to_ghost = a_star(current_node.state)

            if self.path_to_ghost:
                action = self.path_to_ghost.pop(0)

            return action
        else:
            self.suicide = False
            if next_node.action != Directions.STOP:
                self.explored_nodes[key(next_node.state)] = next_node
            return next_node.action

    def hminimax(self, current_node: Node,
                 current_player: Players,
                 depth: int,
                 alpha: float = -float('inf'),
                 beta: float = float('inf')) -> Optional[Node]:
        """The hminimax function that determine the best node to go.

        It implements the alpha-beta prunning to avoid the exploration
        of nodes that would lead to worse or equivalent solution.

        Arguments:
        ----------
        - `current_node`: The node currently studied.
        - `current_player`: The player of the studied turn.
        - `depth`: The depth of the studied node.
        - `alpha`: The alpha value, used to speed up the process.
        - `beta`: The beta value, used to speed up the process.

        Returns:
        --------
        A `Node` corresponding to the studied node, containing the
        action that Pacman should do to maximize its score.
        If the studied node as already been explored or lead to explored
        nodes only, None is returned.
        """
        current_state = current_node.state

        if current_state.isWin() or current_state.isLose():
            current_node.utility = current_state.getScore()
            return current_node

        elif current_node.in_ancestor(current_state):
            # A loop is detected, we indicate the path as already
            # been explored
            return None

        elif depth != 0 and self.cutoff_func(current_state, depth):
            current_node.utility = self.eval_func(current_state)
            return current_node

        else:
            return self.hminimax_step(current_node, depth,
                                      current_player, alpha, beta)

    def hminimax_step(self, current_node: Node,
                      depth: int, current_player: Players,
                      alpha: float, beta: float) -> Optional[Node]:
        """Execute a step of hminimax.

        This function call the correct function depending on the
        player (max player or min player).

        Arguments:
        ----------
        - `current_node`: The node currently studied.
        - `current_player`: The player of the studied turn.
        - `depth`: The depth of the studied node.
        - `alpha`: The alpha value, used to speed up the process.
        - `beta`: The beta value, used to speed up the process.

        Returns:
        --------
        A `Node` corresponding to the studied node, containing the
        action that the playing agent should do to maximize / minimize
        the score.
        If the studied node as already been explored or lead to explored
        nodes only, None is returned.
        """
        if current_player == Players.PACMAN:
            return self.max_player_step(current_node, depth,
                                        current_player, alpha, beta)

        elif current_player == Players.GHOST:
            return self.min_player_step(current_node, depth,
                                        current_player, alpha, beta)

    def max_player_step(self, current_node: Node,
                        depth: int, current_player: Players,
                        alpha: float, beta: float) -> Optional[Node]:
        """Estimate the optimal move when it is Pacman's turn.

        The function will update alpha and beta will determining the
        best move to do.

        Arguments:
        ----------
        - `current_node`: The node currently studied.
        - `current_player`: The player of the studied turn.
        - `depth`: The depth of the studied node.
        - `alpha`: The alpha value, used to speed up the process.
        - `beta`: The beta value, used to speed up the process.

        Returns:
        --------
        A `Node` corresponding to the studied node, containing the
        action that Pacman should do to maximize the score.
        If the studied node as already been explored or lead to explored
        nodes only, None is returned.
        """
        current_state = current_node.state
        possible_successors = current_state.generatePacmanSuccessors()
        if self.consider_stop:
            possible_successors.append((
                current_state.generatePacmanSuccessor(Directions.STOP),
                Directions.STOP
            ))
        best_successor = None
        best_predicted_score = None
        best_action = None

        for state, action in possible_successors:
            successor = current_node.create_successor(state, action)

            next_node = self.hminimax(successor,
                                      get_next_player(current_player),
                                      depth+1,
                                      alpha, beta)
            if not next_node:
                # The next node has already been explored
                continue

            successor_score = next_node.utility

            if ((best_predicted_score is None) or
                    (successor_score > best_predicted_score)):
                best_predicted_score = successor_score
                best_successor = next_node
                best_action = action

                alpha = max(alpha, best_predicted_score)
                if alpha >= beta:
                    break

        if best_predicted_score is None:
            return None

        current_node.utility = best_successor.utility
        current_node.action = best_action
        return current_node

    def min_player_step(self, current_node: Node, depth: int,
                        current_player: Players,
                        alpha: float, beta: float) -> Optional[Node]:
        """Estimate the optimal move when it is the ghost's turn.

        The function will update alpha and beta will determining the
        best move to do.

        Arguments:
        ----------
        - `current_node`: The node currently studied.
        - `current_player`: The player of the studied turn.
        - `depth`: The depth of the studied node.
        - `alpha`: The alpha value, used to speed up the process.
        - `beta`: The beta value, used to speed up the process.

        Returns:
        --------
        A `Node` corresponding to the studied node, containing the
        action that Pacman should do to maximize the score.
        If the studied node as already been explored or lead to explored
        nodes only, None is returned.
        """
        current_state = current_node.state
        possible_successors = current_state.generateGhostSuccessors(
                                                        current_player)
        best_successor = None
        best_predicted_score = None
        best_action = None

        for state, action in possible_successors:
            successor = current_node.create_successor(state, action)

            next_node = self.hminimax(successor,
                                      get_next_player(current_player),
                                      depth+1,
                                      alpha, beta)
            if not next_node:
                # loop detected
                continue

            successor_score = next_node.utility

            if ((best_predicted_score is None) or
                    (successor_score < best_predicted_score)):
                best_predicted_score = successor_score
                best_successor = next_node
                best_action = action

                beta = min(beta, best_predicted_score)
                if alpha >= beta:
                    break

        if best_predicted_score is None:
            return None

        current_node.utility = best_successor.utility
        current_node.action = best_action
        return current_node
