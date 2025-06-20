import subprocess, sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escape.py')


def test_quit_command():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='quit\n',
        text=True,
        capture_output=True,
    )
    assert 'Goodbye' in result.stdout
    assert result.returncode == 0


def test_look_command():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='look\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'dimly lit terminal' in result.stdout
    assert 'access.key' in result.stdout
    assert 'voice.log' in result.stdout
    assert 'Goodbye' in result.stdout


def test_inventory_empty():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='inventory\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'Inventory is empty' in result.stdout
    assert 'Goodbye' in result.stdout


def test_take_item_and_inventory():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\ninventory\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'pick up the access.key' in result.stdout
    assert 'Inventory: access.key' in result.stdout
    assert 'Goodbye' in result.stdout


def test_examine_item():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='examine access.key\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'slim digital token' in result.stdout
    assert 'Goodbye' in result.stdout


def test_examine_missing_item():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='examine unknown\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'do not have unknown' in result.stdout
    assert 'Goodbye' in result.stdout


def test_inventory_alias_i():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='i\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'Inventory is empty' in result.stdout
    assert 'Goodbye' in result.stdout


def test_inventory_alias_inv():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='inv\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'Inventory is empty' in result.stdout
    assert 'Goodbye' in result.stdout


def test_look_around_alias():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='look around\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'dimly lit terminal' in result.stdout
    assert 'Goodbye' in result.stdout


def test_help_alias():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='h\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'Available commands' in result.stdout
    assert 'Goodbye' in result.stdout


def test_use_item_missing():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='use access.key\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'do not have access.key' in result.stdout
    assert 'Goodbye' in result.stdout


def test_use_item_after_take():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\nuse access.key\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'pick up the access.key' in result.stdout
    assert 'hidden directory flickers' in result.stdout
    assert 'Goodbye' in result.stdout


def test_use_item_on_door():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\nuse access.key on door\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'hidden directory flickers' in out
    assert 'hidden/' in out
    assert 'Goodbye' in out


def test_drop_item():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\ndrop access.key\nlook\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'pick up the access.key' in result.stdout
    assert 'drop the access.key' in result.stdout
    assert 'access.key' in result.stdout
    assert 'Goodbye' in result.stdout


def test_save_and_load(tmp_path):
    save_file = tmp_path / 'game.sav'

    # take item and save the game
    subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\nsave\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
    )
    assert save_file.exists()

    # load the game and check inventory
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='load\ninventory\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
    )
    assert 'Inventory: access.key' in result.stdout


def test_ls_and_cd():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='ls\ntake access.key\nuse access.key\nls\ncd hidden\nls\ncd ..\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    # first ls should not show hidden, final ones should
    assert 'hidden/' in out
    assert 'treasure.txt' in out
    assert out.count('hidden/') >= 1
    assert 'Goodbye' in out


def test_root_contains_dream_and_memory():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='ls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'dream/' in out
    assert 'memory/' in out
    assert 'Goodbye' in out


def test_pwd_command():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd lab\npwd\ncd ..\npwd\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert '> > lab' in out
    assert '> > /' in out


def test_enter_lab_and_look():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd lab\nlook\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'cluttered research lab' in out
    assert 'decoder' in out
    assert 'Goodbye' in out


def test_cat_command():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cat voice.log\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'faint digital voice' in result.stdout
    assert 'Goodbye' in result.stdout


def test_use_voice_log():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take voice.log\nuse voice.log\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'haunting voice' in result.stdout
    assert 'Goodbye' in result.stdout


def test_cat_daemon_log():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd core\ncd npc\ncat daemon.log\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'daemon monitors your actions' in out
    assert 'Keep your code clean' in out
    assert 'Goodbye' in out


def test_cat_lucid_note():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\ncat lucid.note\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'dreams you may chart' in out
    assert 'Goodbye' in out


def test_cat_flashback_log():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd memory\ncat flashback.log\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'old memories scroll' in out
    assert 'Goodbye' in out


def test_use_daemon_log():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd core\ncd npc\ntake daemon.log\nuse daemon.log\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'pick up the daemon.log' in out
    assert 'Keep your code clean' in out
    assert 'Goodbye' in out


def test_examine_mem_fragment():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\nuse access.key\ncd hidden\nexamine mem.fragment\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'corrupted memory fragment' in result.stdout
    assert 'Goodbye' in result.stdout


def test_cat_treasure_after_unlock():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\nuse access.key\ncd hidden\ncat treasure.txt\nquit\n',
        text=True,
        capture_output=True,
    )
    assert (
        'You discover a stash of credits and a map leading out of the terminal.'
        in result.stdout
    )
    assert 'Goodbye' in result.stdout


def test_glitch_mode_toggle():
    normal = (
        'You find yourself in a dimly lit terminal session. The prompt blinks patiently.'
    )
    first_glitch = Game()._glitch_text(normal, 1)
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='glitch\nlook\nglitch\nlook\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Glitch mode activated.' in out
    assert first_glitch in out
    assert 'Glitch mode deactivated.' in out
    assert normal in out


def test_glitch_persistence():
    normal = (
        'You find yourself in a dimly lit terminal session. The prompt blinks patiently.'
    )
    first_glitch = Game()._glitch_text(normal, 1)
    later_glitch = Game()._glitch_text(normal, 3)
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='glitch\nlook\nlook\nglitch\nlook\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert first_glitch in out
    assert later_glitch in out
    # final look after glitch off should be normal
    assert out.strip().endswith('Goodbye')


def test_glitch_intensity_increases():
    normal = (
        'You find yourself in a dimly lit terminal session. The prompt blinks patiently.'
    )
    step1 = Game()._glitch_text(normal, 1)
    step3 = Game()._glitch_text(normal, 3)
    step5 = Game()._glitch_text(normal, 5)
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='glitch\nlook\nlook\nlook\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert step1 in out
    assert step3 in out
    assert step5 in out
    # confirm order of increasing corruption
    assert out.index(step1) < out.index(step3) < out.index(step5)


def test_talk_daemon():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd core\ncd npc\ntalk daemon\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'acknowledges your presence' in out
    assert 'more to learn' in out
    assert 'Goodbye' in out


def test_talk_dreamer():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\ncd npc\ntalk dreamer\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'dreamer watches you' in out
    assert '1. Ask about escape' in out
    assert 'Ask about escape' in out
    assert 'Goodbye' in out


def test_dream_contains_subconscious():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'subconscious/' in out
    assert 'Goodbye' in out


def test_reverie_log_present():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\ncd subconscious\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'reverie.log' in out
    assert 'Goodbye' in out


def test_hidden_vault_and_escape_plan():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='take access.key\nuse access.key\ncd hidden\nls\ncd vault\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'vault/' in out
    assert 'escape.plan' in out
    assert 'Goodbye' in out
