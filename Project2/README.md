
# Project II

## Table of contents

- [Description](#description)
- [Credits](#credits)

---
## Description

In this third part of the project, Pacman got tired of ghosts wandering around him. So he decided to buy a laser gun and kill them. But while he shot them, he figured out that the gun has instead turned them into invisible but edible ghosts! Fortunately, as it was part of a box that he bought from a flea market, he also got his hands on a rusty sensor, which still works but is subject to measurement errors which are described in the user manual.

A lot of confusion arose since Pacman shot the ghosts: he has no idea where they currently are in the maze! However, he knows that the ghosts are confused and should be willing to escape from him. More precisely, he knows that `scared` is more fearful than `afraid` who is more fearful than `confused`.

We have designed an intelligent agent based on the Bayes filter algorithm for locating all the ghosts in the maze.

You may use the following command line to start a game where the sole eadible `scared` ghost wanders around the maze while Pacman, controlled by the `humanagent`, tries to locate him with a (very) rusty sensor:

```bash
python run.py --agentfile humanagent.py --bsagentfile beliefstateagent.py --ghostagent scared --nghosts 1 --seed -1 --layout large_filter
```


The **Bayes filter** algorithm was implemented to compute Pacman's belief state. This was done in the `update_belief_state` function of `bayesfilter.py`. The implementation works with multiple ghosts (all running the same policy), Pacman's belief state eventually converges to an uncertainty area for each ghost and the filter considers the Pacman position, as Pacman may wander freely in the maze.

A Pacman's controller to eat ghosts using only its current position, the set of legal actions and its current belief state was implemented as well in the `pacmanagent.py` file.


---



## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
