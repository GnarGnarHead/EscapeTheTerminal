import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game


def test_cat_memory_multi_line(capsys):
    game = Game()
    game._cd("memory")
    game._cat("memory2.log")
    out = capsys.readouterr().out
    lines = out.strip().splitlines()
    assert len(lines) > 1
    assert "tinkered with terminal prompts for fun" in out
