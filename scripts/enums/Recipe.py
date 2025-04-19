from enum import Enum


class Recipe(Enum):
    """Enum of the build types available to the user, corresponding to LaTeX compilation recipes.
    """
    full = "full"
    lualatex = "lualatex"
    biber = "biber"
