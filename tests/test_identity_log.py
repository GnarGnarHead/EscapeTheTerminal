from escape import Game


def test_mem_part_locations(capsys):
    game = Game()
    game._cd('memory')
    game._ls()
    out = capsys.readouterr().out
    assert 'mem.part1' in out
    game._cd('..')
    game._cd('dream')
    game._cd('subconscious')
    game._ls()
    out = capsys.readouterr().out
    assert 'mem.part2' in out


def test_combine_identity_log(capsys):
    game = Game()
    game._cd('memory')
    game._take('mem.part1')
    game._cd('..')
    game._cd('dream')
    game._cd('subconscious')
    game._take('mem.part2')
    game._cd('..')
    game._cd('..')
    game._combine('mem.part1 mem.part2')
    combine_out = capsys.readouterr().out
    assert 'You combine mem.part1 and mem.part2 into identity.log.' in combine_out
    assert 'identity.log' in game.inventory
    assert 'mem.part1' not in game.inventory
    assert 'mem.part2' not in game.inventory
    game._cat('identity.log')
    log_out = capsys.readouterr().out
    assert 'architect of this terminal world' in log_out


def test_identity_log_triggers_quest_and_achievement(capsys):
    game = Game()
    game._cd('memory')
    game._take('mem.part1')
    game._cd('..')
    game._cd('dream')
    game._cd('subconscious')
    game._take('mem.part2')
    game._cd('..')
    game._cd('..')
    game._combine('mem.part1 mem.part2')
    capsys.readouterr()
    assert 'Confront your past' not in game.quests
    assert 'identity_recovered' not in game.achievements
    game._cat('identity.log')
    capsys.readouterr()
    assert 'Confront your past' in game.quests
    assert 'identity_recovered' in game.achievements
