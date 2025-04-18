from enum import Enum


class BuildMode(Enum):
    full = "full"
    lualatex = "lualatex"
    biber = "biber"
