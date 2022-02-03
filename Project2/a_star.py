from pacman_module.game import Directions
from pacman_module.pacman import GameState
from pacman_module.util import PriorityQueue, manhattanDistance
from typing import Tuple, List


Pos = Tuple[int, int]


def key(state: GameState, target_ghost_pos: Pos) -> int:
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.
    - `target_ghost_pos`: The estimated position of the targeted ghost.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    return hash((
        state.getPacmanPosition(),
        target_ghost_pos
        ))


def step_cost(prev_state: GameState, next_state: GameState) -> int:
    """
    Returns the cost to add to the prev_state cost to go to next_state

    Arguments:
    ----------
    - `prev_state`: the previous game state.
    - `next_state`: the next game state.

    Return:
    -------
    An integer corrsponding to the cost of a step.
    """
    return 1  # Walk


def heuristic(pacman_pos: Pos, target_ghost_pos: Pos) -> float:
    """The heuristic used for the a star algorithm.

    We used the basic manhattan distance between the ghost and Pacman.

    Arguments:
    ----------
    - `pacman_pos`: The position of pacman.
    - `target_ghost_pos`: The estimated position of the targeted ghost.

    Returns:
    --------
    A float corresponding to the evaluation of the given state for
    a star algorithm.
    """
    return manhattanDistance(pacman_pos, target_ghost_pos)


def a_star(state: GameState, target_ghost: Pos) -> List[Directions]:
    """
    Given a pacman game state,
    returns a list of legal moves to go reach the ghost.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
                `pacman.GameState`.
    - `target_ghost_pos`: The estimated position of the targeted ghost.

    Return:
    -------
    A list of legal moves as defined in `game.Directions`.
    """
    path = []
    fringe = PriorityQueue()
    fringe.push((state, path, 0.), 0.)
    closed = set()
    pm_pos = state.getPacmanPosition()

    while True:
        if fringe.isEmpty():
            return []

        _, (current, path, cost) = fringe.pop()

        if current.getPacmanPosition() == target_ghost:
            return path

        current_key = key(current, target_ghost)

        if current_key not in closed:
            closed.add(current_key)
            for next_state, action in current.generatePacmanSuccessors():
                next_cost = cost + step_cost(current, next_state)
                fringe.push(
                    (next_state, path + [action], next_cost),
                    next_cost + heuristic(pm_pos, target_ghost)
                )
