# Pacman programming project

<p align="center">
<img src="pacman_game.png" width="50%" />
</p>

The goal of this programming project is to implement intelligent agents for the game of Pacman. The project is divided into three parts:
- [**Project 0**](./project0): Implementation of a Search agent for eating all the food dots as quickly as possible.
- [**Project I**](./project1): Implementation of a Minimax agent for eating all the food dots as quickly as possible, while avoiding the ghost enemies that are chasing you.
- [**Project II**](./project2): Implementation of a Bayes filter for tracking all the non-visible ghosts' positions.

## Table of contents

- [Usage](#usage)
- [FAQ](#faq)
    * [Game score](#game-score)
    * [API](#api)
    * [Illegal moves](#illegal-moves)
- [Credits](#credits)

---


### Usage

Start the game with a Pacman agent controlled by the keyboard (keys `j`, `l`, `i`, `k` or arrow keys):
```bash
python run.py
```

**Options**:

`--agentfile`: Start the game with a Pacman agent following a user-defined control policy:
```bash
python run.py  --agentfile randomagent.py
```

`--ghostagent`: Start the game with a ghost agent (either `dumbyd`, `greedy` or `smarty`):
```bash
python run.py  --ghostagent=greedy
```

`--silentdisplay`: Disable the graphical user interface:
```bash
python run.py --silentdisplay
```

`--layout`: Start the game with a user-specifed layout for the maze (see the `/pacman_module/layouts/` folder):
```bash
python run.py --layout medium
```

`--ghostagent`: Start the game with a user-specifed ghost agent (see [**project I**](./project2)):
```bash
python run.py --ghostagent greedy
```

`-h`: For further details, check the command-line help section:
```bash
python run.py -h
```

---

## FAQ

### Game score

The score function of the game is computed as follows:

`score = -#time steps + 10*#number of eaten food dots - 5*#number of eaten capsules + 200*#number of eaten ghost + (-500 if #losing end) + (500 if #winning end)`.

We have implemented agents that win the game while maximizing their score.

### API

Useful methods of the state are specified below:

 - ```s.generatePacmanSuccessors()``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the pacman agent.
    * This method **must** be called for any node expansion for pacman agent.
 - ```s.generateGhostSuccessors(agentIndex)``` : Returns a list of pairs of successor states and moves given the current state ```s``` for the ghost agent indexed by ```agentIndex>0```.
    * This method **must** be called for any node expansion for ghost agent.
 - ```s.getLegalActions(agentIndex)``` : Returns a list of legal moves given the state ```s``` and the agent indexed by ```agentIndex```. 0 is always the Pacman agent.
 - ```s.getPacmanPosition()``` : Returns the Pacman position in a ```(x,y)``` pair.
 - ```s.getScore()``` : Returns the total score of a state (as defined above).
 - ```s.getFood()``` : Returns a boolean matrix which gives the position of all food dots.
 - ```s.getNumFood()``` : Returns a scalar which gives the number of food dots remaining.
 - ```s.getWalls()``` : Returns a boolean matrix which gives the position of all walls.
 - ```s.getGhostPosition(agentIndex)``` : Returns the position of the ghost agent indexed by ```agentIndex>0```.
 - ```s.getGhostDirection(agentIndex)``` : Returns the direction of the ghost agent indexed by ```agentIndex>0```.
 - ```s.getCapsules()``` : Returns a list of positions of the remaining capsules in the maze.
 - ```s.isWin()``` : Returns True if the state is in a *winning end*.
 - ```s.isLose()``` : Returns True if the state is in a *losing end*.

Implementation examples are provided in `humanagent.py` and `randomagent.py`.

### Illegal moves

The agent always returns a legal move. If it is not the case, the previous move is repeated if it is still legal. Otherwise, it remains in the same location.

---

## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).

---

# Authors 

- Andrea Gómez Herrera - [andrea-liliana](https://github.com/andrea-liliana/)
- Thomas Rives -  [ThomasRives](https://github.com/ThomasRives/)
