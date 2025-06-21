from escape import Game


def test_cipher_plugin(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'cipher',
        'cipher You found a secret decoder.',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out_lines = capsys.readouterr().out.splitlines()
    assert any('Decode this:' in line for line in out_lines)
    assert 'Correct! Cipher solved.' in out_lines
