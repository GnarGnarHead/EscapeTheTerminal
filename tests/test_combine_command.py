import os
import sys
from escape import Game


def test_combine_valid_items(capsys):
    game = Game()
    game._cd('memory')
    game._take('flashback.log')
    game._cd('..')
    game._cd('dream')
    game._cd('subconscious')
    game._take('reverie.log')
    game._cd('..')
    game._cd('..')
    game._combine('flashback.log reverie.log')
    out = capsys.readouterr().out
    assert 'You combine flashback.log and reverie.log into dream.index.' in out
    assert 'dream.index' in game.inventory
    assert 'flashback.log' not in game.inventory
    assert 'reverie.log' not in game.inventory


def test_combine_invalid_recipe(capsys):
    game = Game()
    game._take('access.key')
    game._cd('lab')
    game._take('decoder')
    game._cd('..')
    game._combine('access.key decoder')
    out = capsys.readouterr().out
    assert 'Nothing happens.' in out
    assert 'access.key' in game.inventory
    assert 'decoder' in game.inventory

