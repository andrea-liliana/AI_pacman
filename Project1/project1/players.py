from enum import IntEnum


class Players(IntEnum):
    PACMAN = 0
    """According to documentation Pacman is identified as the
    agent 0."""
    GHOST = 1
    """As we have only one ghost, we will use 1 as identifier."""
