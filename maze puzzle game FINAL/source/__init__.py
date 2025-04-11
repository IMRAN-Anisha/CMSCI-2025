# format to look like Mr Sullivan's 
from .constants import HEIGHT, WIDTH
from .main import run_game
from .UI import Button, MainMenu, GameSelectionMenu
from .path_levels import EasyMaze, MediumMaze, HardMaze

__all__ = [
    "HEIGHT",
    "WIDTH",
    "run_game",
    "Button",
    "MainMenu",
    "GameSelectionMenu",
    "EasyMaze",
    "MediumMaze",
    "HardMaze"
]