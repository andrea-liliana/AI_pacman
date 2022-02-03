from typing import Tuple
from pacman_module.pacman import GameState
from pacman_module.util import manhattanDistance
import math
from enum import Enum, auto
from pacman_module.game import Actions
from players import Players
from collections.abc import Callable

########################################################################
#                         Type declaration                             #
########################################################################
Pos = Tuple[int, int]
Distance_func = Callable[[Pos, Pos], float]


def get_closest_food_distance(state: GameState,
                              distance_func: Distance_func = manhattanDistance
                              ) -> float:
    """Get the position of the closest food from Pacman.

    Arguments:
    ----------
    - `state`: The state studied in this function.
    - `distance_func`: The distance function that will be used by this
                       function.

    Returns:
    --------
    A float representing the distance between Pacman and the closest
    food.
    """
    pacman_pos = state.getPacmanPosition()
    food_positions = state.getFood().asList()
    best_distance = None

    if food_positions:
        for food_pos in food_positions:
            distance = distance_func(pacman_pos, food_pos)

            if (best_distance is None) or (distance < best_distance):
                best_distance = distance
    else:
        best_distance = 0

    return best_distance


def euclidian_distance(pos1: Pos, pos2: Pos) -> float:
    """Calculate the euclidian distance between the two given positions.

    Arguments:
    ----------
    - `pos1`: The first position.
    - `pos2`: The second position.

    Returns:
    --------
    The euclidian distance between the two given position.
    """
    pos1_x, pos1_y = pos1
    pos2_x, pos2_y = pos2
    return math.sqrt((pos1_x - pos2_x)**2 + (pos1_y - pos2_y)**2)


class Safety(Enum):
    """An enumeration used to indicate the safety of a position."""

    """The position is realy dangerous."""
    DANGEROUS = auto()
    """The position is rather safe."""
    SAFE = auto()
    """The position is safe."""
    EXTRA_SAFE = auto()


def get_safety_of_position(current_state: GameState) -> Safety:
    """Get the safety of Pacman position.

    Arguments:
    ----------
    - `current_state`: The state studied by this function.

    Returns:
    --------
    The Safety of the position of Pacman.
    """
    pacman_pos = current_state.getPacmanPosition()
    ghost_pos = current_state.getGhostPosition(int(Players.GHOST))
    g_pos_x, g_pos_y = ghost_pos

    safety = manhattanDistance(pacman_pos, ghost_pos)

    if safety == 1:
        ghost_dir = current_state.getGhostDirection(int(Players.GHOST))
        g_dir_x, g_dir_y = Actions._directions[ghost_dir]
        pos_behind_ghost = (g_pos_x-g_dir_x, g_pos_y-g_dir_y)
        pacman_is_behind = pos_behind_ghost == pacman_pos

        if pacman_is_behind:
            safety += 1

    if safety == 1:
        return Safety.DANGEROUS
    elif 2 <= safety and safety < 4:
        return Safety.SAFE
    else:
        return Safety.EXTRA_SAFE


def sort_pair(elt1: float, elt2: float) -> Tuple[float, float]:
    """Reorder the given elements.

    Arguments:
    ----------
    - `elt1`: The first element.
    - `elt2`: The second element.

    Returns:
    --------
    A tuple containing the given element with the smallest element
    first and the greater then.
    """
    if elt1 <= elt2:
        return (elt1, elt2)
    else:
        return (elt2, elt1)


def direct_path(current_state: GameState, pos: Pos) -> bool:
    """Indicates if there is wall in the path between Pacman and the
    position.

    For a faster treatment, we only consider path constitued of 2
    straight lines (considering all the position was inefficient since
    it did not indicates if a path was possible). Searching for a real
    path is too slow to be used in an evaluation function. This is why
    we simplified the problem.

    Arguments:
    ----------
    - `current_state`: The state that will be studied.
    - `pos`: The position that Pacman want to reach.

    Returns:
    --------
    A boolean that indicates if there is an obvious path to go to the
    given position.
    """
    pos_x, pos_y = pos
    pm_pos_x, pm_pos_y = current_state.getPacmanPosition()

    start_x, end_x = sort_pair(pm_pos_x, pos_x)
    start_y, end_y = sort_pair(pm_pos_y, pos_y)

    walls_pos = current_state.getWalls()
    wall_on_road_x1, wall_on_road_x2 = False, False
    wall_on_road_y1, wall_on_road_y2 = False, False

    for x in range(start_x, end_x+1):
        if walls_pos[x][pm_pos_y]:
            wall_on_road_x1 = True
            break

    if not wall_on_road_x1:
        for y in range(start_y, end_y+1):
            if walls_pos[pos_x][y]:
                wall_on_road_y1 = True
                break

    if (not wall_on_road_x1) and (not wall_on_road_y1):
        return True

    if pos_y != pm_pos_y:
        for x in range(start_x, end_x+1):
            if walls_pos[x][pos_y]:
                wall_on_road_x2 = True
                break
    else:
        wall_on_road_x2 = wall_on_road_x1

    if pos_x != pm_pos_x:
        if not wall_on_road_x2:
            for y in range(start_y, end_y+1):
                if walls_pos[pm_pos_x][y]:
                    wall_on_road_y2 = True
                    break
    else:
        wall_on_road_y2 = wall_on_road_y1

    return (not wall_on_road_x2) and (not wall_on_road_y2)


def get_best_food(state: GameState,
                  dist_func: Distance_func = manhattanDistance
                  ) -> Tuple[Pos, float, bool]:
    """Get the distance between Pacman and the best food to get.

    The best food is determine considering the distance and if there is
    a wall in the path.

    Arguments:
    ----------
    - `state`: The state to study.
    - `dist_func`: The distance function to us in this function.

    Returns:
    --------
    A tuple containing the position of the best food, the distance
    between pacman and the best food, and a boolean indicating
    if there is a wall between pacman and the food.
    """
    pacman_pos = state.getPacmanPosition()

    best_dist = None
    best_food = None
    best_has_wall = False
    eval = 0
    best_eval = None

    for food_pos in state.getFood().asList():
        distance = dist_func(pacman_pos, food_pos)
        eval = distance
        reachable_directly = direct_path(state, food_pos)

        if not reachable_directly:
            eval += 50
            wall = True
        else:
            wall = False

        if (best_eval is None) or (eval < best_eval):
            best_eval = eval
            best_dist = distance
            best_food = food_pos
            best_has_wall = wall

    if best_dist is None:
        best_dist = 0

    return best_food, best_dist, best_has_wall


def ghost_in_path(state: GameState, destination: Pos) -> bool:
    """Check if a ghost is in an obvious path to the destination.

    An obvious path is build with 2 straight lines joining Pacman
    and the destination.

    Arguments:
    ----------
    - `state`: the state studied in this function.
    - `destination`: Pacman destination.

    Returns:
    --------
    A boolean that indicates if there is a ghost on an obvious path.
    """
    pos_x, pos_y = destination
    pm_x, pm_y = state.getPacmanPosition()
    gh_x, gh_y = state.getGhostPosition(int(Players.GHOST))

    start_x, end_x = sort_pair(pm_x, pos_x)
    start_y, end_y = sort_pair(pm_y, pos_y)

    ghost_on_road_x1, ghost_on_road_x2 = False, False
    ghost_on_road_y1, ghost_on_road_y2 = False, False

    for x in range(start_x, end_x):
        if (gh_x == x) and (gh_y == pm_y):
            ghost_on_road_x1 = True
            break

    if not ghost_on_road_x1:
        for y in range(start_y, end_y):
            if (gh_x == pos_x) and (gh_y == y):
                ghost_on_road_y1 = True
                break

    if (not ghost_on_road_x1) and (not ghost_on_road_y1):
        return False

    if pos_y != pm_y:
        for x in range(start_x, end_x):
            if (gh_x == x) and (gh_y == pos_y):
                ghost_on_road_x2 = True
                break
    else:
        ghost_on_road_x2 = ghost_on_road_x1

    if pos_x != pm_x:
        if not ghost_on_road_x2:
            for y in range(start_y, end_y):
                if (gh_y == y) and (gh_x == pm_x):
                    ghost_on_road_y2 = True
                    break
    else:
        ghost_on_road_y2 = ghost_on_road_y1

    return ghost_on_road_x2 or ghost_on_road_y2
