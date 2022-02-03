# A class for HMinimax ?

As we used the very same code for all our hminimax, we decided to put it in a class.
Thanks to this, we were sure that there were no mistake in the implementation of hminimax.
We just have to define the **evaluation function** and the **cutoff test** in the different files.

Doing so helped us to find and correct a lot of bugs in our implementation of hminimax (cases we did not expected and did not handled).

# Conventions

When there is some properties to respect regarding a property of an object, we use the `property` decorator.
Then, we add an `_` before the variable name, we define the `get`, and `set` method if there are special rules to apply (in our case, it was rules to check for debugging).

# Type hinting
The type hinting was used to enable more functionalities on IDE. Autocompletion works better with it. This is why we used it for our code. Furthermore, it made the code easier to use since all we need to call a function is directly in its signature.

# Suicide

When Pacman is lost (i.e. there is a loop in the explored nodes), we decided to make him die.
To do so, we use a star algorithm so that he goes to the gost.
If the minimax goes out of the loop, Pacman stop going to the ghost.
The chosen solution is not optimal since Pacman try to go where the ghost were when he decide to kill himself, but it is not a random choice. As greedy and smarty "follow" Pacman, there is a high chance they will kill Pacman while he is going to its destination. For dumby, when Pacman arrived to its destination, he wait for the ghost to kill him.

This solution ensure the terminaison of the algorithm.
