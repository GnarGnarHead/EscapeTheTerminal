from importlib import metadata

from .game import Game

try:
    __version__ = metadata.version("escape-the-terminal")
except metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"
__all__ = ["Game", "__version__"]
