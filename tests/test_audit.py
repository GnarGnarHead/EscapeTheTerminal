import os
from escape import Game


def test_audit_outputs_fields(monkeypatch, capsys):
    os.environ['ET_MODEL'] = 'test-model'
    os.environ['ET_TOKENS'] = '10'
    os.environ['ET_INTEGRITY_BASE'] = '80'
    os.environ['ET_AGENCY_BASE'] = '90'
    game = Game()
    game.corruption = 100  # 25%
    monkeypatch.setattr(Game, "_apply_corruption", lambda self, text: text)
    game.command_history.extend(['look', 'take key'])
    capsys.readouterr()
    game._audit()
    out_lines = capsys.readouterr().out.splitlines()
    assert "Model: test-model" in out_lines
    assert "Tokens used: 13" in out_lines
    assert "Prompt integrity: 55%" in out_lines
    assert "User agency: 65%" in out_lines


def test_audit_command_registered():
    game = Game()
    assert 'audit' in game.command_descriptions
    assert 'audit' in game.command_map
