from importlib import metadata

from .game import Game

__version__ = metadata.version("escape-the-terminal")
__all__ = ["Game", "__version__"]
