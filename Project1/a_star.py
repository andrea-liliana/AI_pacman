from pacman_module.game import Directions
from pacman_module.pacman import GameState
from pacman_module.util import PriorityQueue, manhattanDistance
from players import Players


def key(state: GameState) -> int:
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    return hash((
        state.getPacmanPosition(),
        state.getFood(),
        state.getGhostPosition(Players.GHOST)))


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


def heuristic(state: GameState) -> float:
    """The heuristic used for the a star algorithm.

    We used the basic manhattan distance between the ghost and Pacman.

    Arguments:
    ----------
    - `state`: The state studied by the heuristic.

    Returns:
    --------
    A float corresponding to the evaluation of the given state for
    a star algorithm.
    """
    pacman_pos = state.getPacmanPosition()
    ghost_pos = state.getGhostPosition(Players.GHOST)

    return manhattanDistance(pacman_pos, ghost_pos)


def a_star(state: GameState) -> list[Directions]:
    """
    Given a pacman game state,
    returns a list of legal moves to go reach the ghost.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
                `pacman.GameState`.

    Return:
    -------
    A list of legal moves as defined in `game.Directions`.
    """
    path = []
    fringe = PriorityQueue()
    fringe.push((state, path, 0.), 0.)
    closed = set()

    while True:
        if fringe.isEmpty():
            return []

        _, (current, path, cost) = fringe.pop()

        if current.isLose():
            return path

        current_key = key(current)

        if current_key not in closed:
            closed.add(current_key)
            for next_state, action in current.generatePacmanSuccessors():
                next_cost = cost + step_cost(current, next_state)
                fringe.push(
                    (next_state, path + [action], next_cost),
                    next_cost + heuristic(next_state)
                )
