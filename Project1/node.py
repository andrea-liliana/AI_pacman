from pacman_module.pacman import GameState
from players import Players
import sys
from copy import copy
from pacman_module.game import Directions


def key(state: GameState) -> int:
    """Get a unique key from a state.

    The key calculation depends on the food present at this state,
    Pacman position, the position of the ghost, the direction of the
    ghost.

    Arguments:
    ----------
    - `state`: The state of the game.

    Returns:
    --------
    An integer that represent the game of the state. A different state
    implies a different key.
    """
    return hash((state.getFood(),
                state.getPacmanPosition(),
                state.getGhostPosition(int(Players.GHOST)),
                state.getGhostDirection(int(Players.GHOST))))


class Node:
    """This class represent a `Gamestate` with additional feature.

    We use a class since it allow us to perform more actions than a
    tuple. When we used tuples, we add method linked to the tupple.
    We thought that a class was a better choice for readability and
    debugging.

    Attributes:
    -----------
    - `state`: The state represented by the node.
    - `_action`: An action, corresponding to the action to (to
                 maximize / minimize) do when the state is reached.
    - `ancestors`: The ancestors of the state. It is used to detect
                   loops in the process.
    - `_utility`: The utility of the state.
    """
    def __init__(self, state: GameState) -> None:
        """The constructor of the class.

        Arguments:
        ----------
        - `state`: The state represented by the node.

        Returns:
        --------
        An `Node` representing the given State.
        """
        self.state = state
        self._action = None
        self.ancestors = set()
        self._utility = None

    @property
    def action(self):
        """Getter for `_action`."""
        return self._action

    @action.setter
    def action(self, new_action):
        """Setter for `_action`."""
        if self._action is not None:
            sys.exit("2 actions in the same node")
        self._action = new_action

    def add_ancestor(self, new_ancestor: GameState) -> None:
        """Add an ancestor to the node.

        Arguments:
        ----------
        - `new_ancestor`: the ancestor to add to the node.
        """
        if not self.in_ancestor(new_ancestor):
            self.ancestors.add(key(new_ancestor))

    def in_ancestor(self, state: GameState) -> bool:
        """Indicates if a states is in the ancestors of the node.

        Arguments:
        ----------
        - `state`: The state we want to know if it is in the ancestors.

        Returns:
        --------
        A boolean that indicates if the state is in the ancestors.
        """
        return key(state) in self.ancestors

    @property
    def utility(self) -> float:
        """Getter for `_utility`."""
        return self._utility

    @utility.setter
    def utility(self, new_utility: float) -> None:
        """Setter for `_utility`."""
        if self._utility is not None:
            sys.exit("The utility of a node has been set twice")
        self._utility = new_utility

    def create_successor(self, state: GameState,
                         action: Directions) -> 'Node':
        """Create a successor to the node.

        Arguments:
        ----------
        - `state`: The state that is the successor.

        Returns:
        --------
        A `Node` representing the successor.
        """
        new_node = Node(state)
        if self.ancestors:
            new_node.ancestors = copy(self.ancestors)
        if action != Directions.STOP:
            # Ancestor already stored
            new_node.add_ancestor(self.state)

        return new_node
