# Project I

## Table of contents

- [Description](#description)
- [Credits](#credits)

---

## Description

In the last project, Pacman could wander peacefully in its maze. In this project, he needs to avoid a walking ghost that would kill it if it reached his position. And Pacman has not idea of (i) what is the objective of the ghost (whether the ghost wants to kill him or not) and (ii) if it is playing optimally for achieving its goal. Pacman only knows that the ghost cannot make a half-turn unless it has no other choice.

The ghost follows one of the following policies, as set through the `--ghostagent` command line option:
 - `dumby`: Rotate on itself in a counterclockwise fashion until it can go on its left.
 - `greedy`: Select the next position that is the closest to Pacman.
 - `smarty`: Select the next position which leads to the shortest path towards Pacman.

But as specified above, Pacman is not aware of the policy that the ghost follows.

An intelligent agent is designed based on adversarial search algorithms for maximizing the score. In this project, we will not consider layouts with capsules. In order to run the code, you can use the following command (replacing `humanagent.py` by `minimax.py / hminimax0.py / hminimax1.py / hminimax2.py`) :

```
python3 run.py --agentfile humanagent.py --ghost dumby --layout small_adv
```

We have implemented the following:

  - A **Minimax** algorithm in `minimax.py` with completeness guaranteed and that provides an optimal strategy in the smaller map against all kinds of ghosts.
  
  - An **H-Minimax** algorithm with cutoff-tests and evaluation functions in `hminimax0.py`, `hminimax1.py` and `hminimax2.py`. Each proposed evaluation function differs from the game score function, the evaluation functions are fast to compute and generalizable.
  

---

## Credits

The programming projects are adapted from [CS188 (UC Berkeley)](http://ai.berkeley.edu/project_overview.html).
