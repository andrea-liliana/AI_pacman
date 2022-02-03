from pacman_module.game import Agent
import numpy as np
from pacman_module.util import manhattanDistance
from scipy.stats import binom
import math


def get_probable_position_ghost(belief_ghost):
    """
        Get the most probable position of the ghost according to the
        belief.

        Arguments:
        ----------
        - `belief_ghost`: the belief state of pacman regarding the
                          ghost.

        Return:
        -------
        The most likely position of the ghost.
        """
    width, height = belief_ghost.shape
    mat_kernel = np.ones((3, 3))
    mat_kernel[1, 1] = 3
    max_proba = 0
    pos = (0, 0)

    for x in range(1, width-1):
        for y in range(1, height-1):
            proba = np.sum(
                mat_kernel * belief_ghost[x-1:x+2, y-1:y+2]
            )
            if proba > max_proba:
                max_proba = proba
                pos = (x, y)

    return pos


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        """
            Variables to use in 'update_belief_state' method.
            Initialization occurs in 'get_action' method.
            XXX: DO NOT MODIFY THE DEFINITION OF THESE VARIABLES
            # Doing so will result in a 0 grade.
        """

        # Current list of belief states over ghost positions
        self.beliefGhostStates = None

        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None

        # Hyper-parameters
        self.ghost_type = self.args.ghostagent
        self.sensor_variance = self.args.sensorvariance

        self.p = 0.5
        self.n = int(self.sensor_variance/(self.p*(1-self.p)))

        # XXX: Your code here
        # NB: Adding code here is not necessarily useful, but you may.
        self._shape = None
        self.uncertainties = None
        self.qualities = None
        self.nb_records = 250
        self.metrics_file = "metrics.csv"
        # XXX: End of your code

    @property
    def shape(self):
        """
        Initialize the shape if necessary.

        Returns:
        --------
        The shape of the maze.
        """
        if self._shape is None and self.walls is not None:
            self._shape = (self.walls.width, self.walls.height)

        return self._shape

    def _get_sensor_model(self, pacman_position, evidence):
        """
        Arguments:
        ----------
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        Return:
        -------
        The sensor model represented as a 2D numpy array of
        size [width, height].
        The element at position (w, h) is the probability
        P(E_t=evidence | X_t=(w, h))
        """
        width, height = self.shape
        s = np.zeros((width, height))
        binomial = binom(self.n, 0.5)

        for x in range(width):
            for y in range(height):
                md = manhattanDistance(pacman_position, (x, y))
                shift = evidence - md

                s[x, y] = binomial.pmf(self.n/2 + shift)

        return s

    def is_in_grid(self, pos):
        """
        Check if the given position is in the maze.

        Arguments:
        ----------
        - `pos`: The position to test.

        Returns:
        --------
        A boolean indicating if the given position is in the maze or
        not.
        """
        width, height = self.shape
        in_width = not (pos[0] < 0 or pos[0] >= width)
        in_height = not (pos[1] < 0 or pos[1] >= height)
        return in_width and in_height

    def _get_transition_model(self, pacman_position):
        """
        Arguments:
        ----------
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        Return:
        -------
        The transition model represented as a 4D numpy array of
        size [width, height, width, height].
        The element at position (w1, h1, w2, h2) is the probability
        P(X_t+1=(w1, h1) | X_t=(w2, h2))
        """
        pm_x, pm_y = pacman_position
        width, height = self.shape
        trans_m = np.full((width, height, width, height), 0.)

        g = 0
        if self.ghost_type == "confused":
            g = 1  # = 2**0
        elif self.ghost_type == "afraid":
            g = 2  # = 2**1
        elif self.ghost_type == "scared":
            g = 8  # = 2**3

        for x_dep in range(width):
            for y_dep in range(height):
                adj_cases = [
                    (x_dep-1, y_dep), (x_dep+1, y_dep),
                    (x_dep, y_dep-1), (x_dep, y_dep+1)
                ]

                dep_dist = manhattanDistance((x_dep, y_dep), pacman_position)

                for x_dst, y_dst in adj_cases:
                    if (not self.is_in_grid((x_dst, y_dst)) or
                            self.walls[x_dst][y_dst] or
                            self.walls[x_dep][y_dep]):
                        continue

                    new_dist = manhattanDistance(
                                (x_dst, y_dst), pacman_position)
                    new_val = g if (new_dist >= dep_dist) else 1

                    trans_m[x_dst, y_dst, x_dep, y_dep] = new_val

                normal_coef = np.sum(trans_m[:, :, x_dep, y_dep])
                if normal_coef != 0:
                    trans_m[:, :, x_dep, y_dep] = \
                        trans_m[:, :, x_dep, y_dep] / normal_coef

        return trans_m

    def _get_updated_belief(self, belief, evidences, pacman_position,
                            ghosts_eaten):
        """
        Given a list of (noised) distances from pacman to ghosts,
        and the previous belief states before receiving the evidences,
        returns the updated list of belief states about ghosts
        positions.

        Arguments:
        ----------
        - `belief`: A list of Z belief states at state x_{t-1}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        - `ghosts_eaten`: list of booleans indicating
          whether ghosts have been eaten or not
        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.
        N.B. : [0,0] is the bottom left corner of the maze.
               Matrices filled with zeros must be returned for eaten ghosts.
        """

        # XXX: Your code here
        nb_ghosts, width, height = np.shape(belief)
        # initialize all the boxes with the same probability
        if not self.shape:
            self.shape = (width, height)

        new_belief = np.array([
            np.zeros((width, height)) for _ in range(nb_ghosts)
        ])
        trans_model = self._get_transition_model(pacman_position)

        for k in range(nb_ghosts):
            if ghosts_eaten[k]:
                new_belief[k][:, :] = 0
                continue

            belif_gk = belief[k]
            sensor_model = \
                self._get_sensor_model(pacman_position, evidences[k])
            for i in range(width):
                for j in range(height):
                    new_belief[k, i, j] = \
                        np.sum(trans_model[i, j, :, :] * belif_gk)
                    new_belief[k, i, j] *= sensor_model[i, j]

            normal_coef = np.sum(new_belief[k])
            if normal_coef != 0:
                new_belief[k] = new_belief[k] / normal_coef

        belief = new_belief

        # XXX: End of your code

        return belief

    def update_belief_state(self, evidences, pacman_position, ghosts_eaten):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions
        Arguments:
        ----------
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        - `ghosts_eaten`: list of booleans indicating
          whether ghosts have been eaten or not
        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.
        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        belief = self._get_updated_belief(self.beliefGhostStates, evidences,
                                          pacman_position, ghosts_eaten)
        self.beliefGhostStates = belief
        return belief

    def _get_evidence(self, state):
        """
        Computes noisy distances between pacman and ghosts.
        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.
        Return:
        -------
        - A list of Z noised distances in real numbers
          where Z is the number of ghosts.
        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for pos in positions:
            true_distance = manhattanDistance(pos, pacman_position)
            noise = binom.rvs(self.n, self.p) - self.n*self.p
            noisy_distances.append(true_distance + noise)

        return noisy_distances

    def init_record(self, nb_ghosts):
        """
        Initialize the variable used for the records.

        Parameters:
        -----------
        - `nb_ghosts`: The number of ghosts in the game.
        """
        self.uncertainties = [[] for _ in range(nb_ghosts)]
        self.qualities = [[] for _ in range(nb_ghosts)]

    def _get_uncertainty(self, belief):
        """
        Compute the uncertainty of a belief.

        Parameters:
        -----------
        - `belief`: The belief on which the uncertainty will be
                    computed.

        Returns:
        --------
        A number between 0 and 100 corresponding to the uncertainty of
        the given belief.
        """
        return 100 * (np.count_nonzero(belief) / belief.size)

    def _get_quality(self, ghost, belief, state):
        """
        Compute the quality of a given belief regarding a specific
        ghost and the given state.

        Parameters:
        -----------
        - `ghost`: The number associated to the ghost position in the
                   list of matrix corresponding to the beliefs.
        - `belief`: The belief associated to the ghost, on which the
                    the quality will be computed.
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Returns:
        --------
        The quality of the given belief.
        """
        # +1 because 0 is Pacman
        gh_x, gh_y = state.getGhostPosition(ghost+1)
        estim_x, estim_y = get_probable_position_ghost(belief)

        return math.sqrt((estim_x - gh_x)**2 + (estim_y - gh_y)**2)

    def update_metrics(self, nb_ghosts, beliefs, state):
        """
        Update the metrics by recording new values.

        Parameters:
        -----------
        - `nb_ghosts`: The number of ghosts in the game.
        - `beliefs`: A list of Z
                     N*M numpy matrices of probabilities
                     where N and M are respectively width and height
                     of the maze layout and Z is the number of ghosts.
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        """
        for ghost in range(nb_ghosts):
            self.uncertainties[ghost].append(
                self._get_uncertainty(beliefs[ghost])
            )
            self.qualities[ghost].append(
                self._get_quality(ghost, beliefs[ghost], state)
            )

    def _record_metrics(self, belief_states, state):
        """
        Use this function to record your metrics
        related to true and belief states.
        Won't be part of specification grading.
        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.
        - `belief_states`: A list of Z
           N*M numpy matrices of probabilities
           where N and M are respectively width and height
           of the maze layout and Z is the number of ghosts.
        N.B. : [0,0] is the bottom left corner of the maze
        """
        nb_ghosts = belief_states.shape[0]
        if self.uncertainties is None or self.qualities is None:
            self.init_record(nb_ghosts)

        self.update_metrics(nb_ghosts, belief_states, state)

        nb_record = len(self.qualities[0])
        if nb_record == self.nb_records:

            with open(self.metrics_file, "w") as fm:
                for nb_meas in range(len(self.uncertainties[0])):
                    fm.write(f"{self.uncertainties[0][nb_meas]};" +
                             f"{self.qualities[0][nb_meas]}")
                    for i in range(1, nb_ghosts):
                        fm.write(f";{self.uncertainties[i][nb_meas]};" +
                                 f"{self.qualities[i][nb_meas]}")
                    fm.write("\n")

            exit()  # Stop the execution of the program

    def get_action(self, state):
        """
        Given a pacman game state, returns a belief state.
        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.
        Return:
        -------
        - A belief state.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()

        evidence = self._get_evidence(state)
        newBeliefStates = self.update_belief_state(evidence,
                                                   state.getPacmanPosition(),
                                                   state.data._eaten[1:])
        self._record_metrics(self.beliefGhostStates, state)

        return newBeliefStates, evidence
