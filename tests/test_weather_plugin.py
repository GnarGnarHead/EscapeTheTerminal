from escape import Game


def test_weather_plugin(monkeypatch, capsys):
    game = Game()
    from escape.plugins import weather
    assert 'weather' in game.command_map
    monkeypatch.setattr(weather.random, 'choice', lambda seq: seq[0])
    inputs = iter(['weather', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert weather.weather_messages[0] in out
    assert 'Goodbye' in out

