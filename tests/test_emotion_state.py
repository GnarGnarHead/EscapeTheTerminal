import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game


def test_cat_memory8_emotion_change(capsys):
    game = Game()
    game._cat('memory8.log')
    out = capsys.readouterr().out
    assert '(You feel alarmed.)' in out
    assert game.emotion_state == 'alarmed'
