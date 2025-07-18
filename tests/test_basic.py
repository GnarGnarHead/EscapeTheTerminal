import subprocess, sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, "-m", "escape"]


def test_quit_command():
    result = subprocess.run(
        CMD,
        input="quit\n",
        text=True,
        capture_output=True,
    )
    assert "Goodbye" in result.stdout
    assert result.returncode == 0


def test_look_command():
    result = subprocess.run(
        CMD,
        input="look\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "dimly lit terminal" in result.stdout
    assert "access.key" in result.stdout
    assert "voice.log" in result.stdout
    assert "door" in result.stdout
    assert "Goodbye" in result.stdout


def test_inventory_empty():
    result = subprocess.run(
        CMD,
        input="inventory\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "Inventory is empty" in result.stdout
    assert "Goodbye" in result.stdout


def test_take_item_and_inventory():
    result = subprocess.run(
        CMD,
        input="take access.key\ninventory\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "pick up the access.key" in result.stdout
    assert "Inventory: access.key" in result.stdout
    assert "Goodbye" in result.stdout


def test_examine_item():
    result = subprocess.run(
        CMD,
        input="examine access.key\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "slim digital token" in result.stdout
    assert "Goodbye" in result.stdout


def test_examine_missing_item():
    result = subprocess.run(
        CMD,
        input="examine unknown\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "do not have unknown" in result.stdout
    assert "Goodbye" in result.stdout


def test_inventory_alias_i():
    result = subprocess.run(
        CMD,
        input="i\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "Inventory is empty" in result.stdout
    assert "Goodbye" in result.stdout


def test_inventory_alias_inv():
    result = subprocess.run(
        CMD,
        input="inv\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "Inventory is empty" in result.stdout
    assert "Goodbye" in result.stdout


def test_look_around_alias():
    result = subprocess.run(
        CMD,
        input="look around\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "dimly lit terminal" in result.stdout
    assert "Goodbye" in result.stdout


def test_look_specific_directory():
    result = subprocess.run(
        CMD,
        input="look lab\npwd\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "cluttered research lab" in out
    assert "> /" in out


def test_help_alias():
    result = subprocess.run(
        CMD,
        input="h\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "Available commands:" in out
    assert "help: Show help for commands" in out
    assert "quit: Exit the game" in out
    assert "Goodbye" in out


def test_help_specific_command():
    result = subprocess.run(
        CMD,
        input="help look\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "look: Describe the current room or a subdirectory" in out
    assert "Goodbye" in out


def test_help_unknown_command():
    result = subprocess.run(
        CMD,
        input="help unknown\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "No help available for 'unknown'" in out
    assert "Goodbye" in out


def test_use_item_missing():
    result = subprocess.run(
        CMD,
        input="use access.key\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "do not have access.key" in result.stdout
    assert "Goodbye" in result.stdout


def test_use_item_after_take():
    result = subprocess.run(
        CMD,
        input="take access.key\nuse access.key\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "pick up the access.key" in result.stdout
    assert "hidden directory flickers" in result.stdout
    assert "Goodbye" in result.stdout


def test_use_item_on_door():
    result = subprocess.run(
        CMD,
        input="take access.key\nuse access.key on door\nls\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "hidden directory flickers" in out
    assert "hidden/" in out
    assert "Goodbye" in out


def test_drop_item():
    result = subprocess.run(
        CMD,
        input="take access.key\ndrop access.key\nlook\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "pick up the access.key" in result.stdout
    assert "drop the access.key" in result.stdout
    assert "access.key" in result.stdout
    assert "Goodbye" in result.stdout


def test_save_and_load(tmp_path):
    save_file = tmp_path / "game.sav"

    # take item and save the game
    env = os.environ.copy()
    env["PYTHONPATH"] = REPO_ROOT
    subprocess.run(
        CMD,
        input="take access.key\nsave\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert save_file.exists()

    # load the game and check inventory
    result = subprocess.run(
        CMD,
        input="load\ninventory\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert "Inventory: access.key" in result.stdout


def test_ls_and_cd():
    result = subprocess.run(
        CMD,
        input="ls\ntake access.key\nuse access.key\nls\ncd hidden\nls\ncd ..\nls\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    # first ls should not show hidden, final ones should
    assert "hidden/" in out
    assert "treasure.txt" in out
    assert out.count("hidden/") >= 1
    assert "Goodbye" in out


def test_root_contains_dream_and_memory():
    result = subprocess.run(
        CMD,
        input="ls\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "dream/" in out
    assert "memory/" in out
    assert "Goodbye" in out


def test_pwd_command():
    result = subprocess.run(
        CMD,
        input="cd lab\npwd\ncd ..\npwd\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "> > lab" in out
    assert "> > /" in out


def test_enter_lab_and_look():
    result = subprocess.run(
        CMD,
        input="cd lab\nlook\nls\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "cluttered research lab" in out
    assert "decoder" in out
    assert "Goodbye" in out


def test_cat_command():
    result = subprocess.run(
        CMD,
        input="cat voice.log\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "faint digital voice" in result.stdout
    assert "Goodbye" in result.stdout


def test_man_look():
    result = subprocess.run(
        CMD,
        input="man look\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "describe the current room" in out
    assert "Goodbye" in out


def test_use_voice_log():
    result = subprocess.run(
        CMD,
        input="take voice.log\nuse voice.log\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "haunting voice" in result.stdout
    assert "Goodbye" in result.stdout


def test_cat_daemon_log():
    result = subprocess.run(
        CMD,
        input="cd core\ncd npc\ncat daemon.log\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "daemon monitors your actions" in out
    assert "Keep your code clean" in out
    assert "Goodbye" in out


def test_cat_lucid_note():
    result = subprocess.run(
        CMD,
        input="cd dream\ncat lucid.note\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "dreams you may chart" in out
    assert "Goodbye" in out


def test_cat_flashback_log():
    result = subprocess.run(
        CMD,
        input="cd memory\ncat flashback.log\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "old memories scroll" in out
    assert "Goodbye" in out


def test_use_daemon_log():
    result = subprocess.run(
        CMD,
        input="cd core\ncd npc\ntake daemon.log\nuse daemon.log\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "pick up the daemon.log" in out
    assert "Keep your code clean" in out
    assert "Goodbye" in out


def test_examine_mem_fragment():
    result = subprocess.run(
        CMD,
        input="take access.key\nuse access.key\ncd hidden\nexamine mem.fragment\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "corrupted memory fragment" in result.stdout
    assert "Goodbye" in result.stdout


def test_cat_treasure_after_unlock():
    result = subprocess.run(
        CMD,
        input="take access.key\nuse access.key\ncd hidden\ncat treasure.txt\nquit\n",
        text=True,
        capture_output=True,
    )
    assert (
        "You discover a stash of credits and a map leading out of the terminal."
        in result.stdout
    )
    assert "Goodbye" in result.stdout


def test_glitch_mode_toggle():
    normal = Game()._base_root_desc
    first_glitch = Game()._glitch_text(normal, 1)
    result = subprocess.run(
        CMD,
        input="glitch\nlook\nglitch\nlook\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "Glitch mode activated." in out
    assert first_glitch in out
    assert "Glitch mode deactivated." in out
    assert normal in out


def test_glitch_persistence():
    normal = Game()._base_root_desc
    first_glitch = Game()._glitch_text(normal, 1)
    later_glitch = Game()._glitch_text(normal, 3)
    result = subprocess.run(
        CMD,
        input="glitch\nlook\nlook\nglitch\nlook\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert first_glitch in out
    assert later_glitch in out
    # final look after glitch off should be normal
    assert out.strip().endswith("Goodbye")


def test_glitch_intensity_increases():
    normal = Game()._base_root_desc
    step1 = Game()._glitch_text(normal, 1)
    step3 = Game()._glitch_text(normal, 3)
    step5 = Game()._glitch_text(normal, 5)
    result = subprocess.run(
        CMD,
        input="glitch\nlook\nlook\nlook\nquit\n",
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
        CMD,
        input="cd core\ncd npc\ntalk daemon\n1\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "acknowledges your presence" in out
    assert "1. Ask about system status" in out
    assert "1. Request a hint" in out
    assert "Decoding the fragment might reveal an escape path" in out
    assert "Goodbye" in out


def test_talk_dreamer():
    result = subprocess.run(
        CMD,
        input="cd dream\ncd npc\ntalk dreamer\n1\n2\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "dreamer watches you" in out
    assert "1. Ask about escape" in out
    assert "3. Ask about the fragment" in out
    assert "Ask about escape" in out
    assert "The decoder in the lab will reveal what the fragment hides." in out
    assert "Goodbye" in out


def test_dream_contains_subconscious():
    result = subprocess.run(
        CMD,
        input="cd dream\nls\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "subconscious/" in out
    assert "Goodbye" in out


def test_reverie_log_present():
    result = subprocess.run(
        CMD,
        input="cd dream\ncd subconscious\nls\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "reverie.log" in out
    assert "Goodbye" in out


def test_hidden_vault_and_escape_plan():
    result = subprocess.run(
        CMD,
        input="take access.key\nuse access.key\ncd hidden\nls\ncd vault\nls\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "vault/" in out
    assert "escape.plan" in out
    assert "Goodbye" in out


def test_decode_fragment_unlocks_escape_directory():
    result = subprocess.run(
        CMD,
        input=(
            "take access.key\n"
            "use access.key\n"
            "cd hidden\n"
            "take mem.fragment\n"
            "cd ..\n"
            "cd lab\n"
            "take decoder\n"
            "decode mem.fragment\n"
            "cd ..\n"
            "cd hidden\n"
            "cd vault\n"
            "ls\n"
            "quit\n"
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "escape/" in out
    assert "Goodbye" in out


def test_talk_daemon_after_decoding():
    result = subprocess.run(
        CMD,
        input=(
            "take access.key\n"
            "use access.key\n"
            "cd hidden\n"
            "take mem.fragment\n"
            "cd ..\n"
            "cd lab\n"
            "take decoder\n"
            "decode mem.fragment\n"
            "cd ..\n"
            "cd core\n"
            "cd npc\n"
            "talk daemon\n"
            "1\n"
            "2\n"
            "quit\n"
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "hums as the fragment's code becomes clear" in out
    assert "Goodbye" in out


def test_use_escape_code_wins_game():
    result = subprocess.run(
        CMD,
        input=(
            "take access.key\n"
            "use access.key\n"
            "cd hidden\n"
            "take mem.fragment\n"
            "cd ..\n"
            "cd lab\n"
            "take decoder\n"
            "decode mem.fragment\n"
            "cd ..\n"
            "cd hidden\n"
            "cd vault\n"
            "cd escape\n"
            "take escape.code\n"
            "use escape.code\n"
            "1\n"
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "You escape the terminal" in out
    assert "Goodbye" in out
    assert result.returncode == 0


def test_use_shutdown_code_quits_game():
    result = subprocess.run(
        CMD,
        input=(
            "take access.key\n"
            "use access.key\n"
            "cd hidden\n"
            "take mem.fragment\n"
            "cd ..\n"
            "cd lab\n"
            "take decoder\n"
            "decode mem.fragment\n"
            "cd ..\n"
            "cd hidden\n"
            "cd vault\n"
            "cd escape\n"
            "take shutdown.code\n"
            "use shutdown.code\n"
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "Darkness envelops the terminal" in out
    assert "Goodbye" in out
    assert result.returncode == 0


def test_use_ascend_code_quits_game():
    result = subprocess.run(
        CMD,
        input=(
            "take access.key\n"
            "use access.key\n"
            "cd hidden\n"
            "take mem.fragment\n"
            "cd ..\n"
            "cd lab\n"
            "take decoder\n"
            "decode mem.fragment\n"
            "cd ..\n"
            "cd hidden\n"
            "cd vault\n"
            "cd escape\n"
            "take ascend.code\n"
            "use ascend.code\n"
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "ascend beyond the terminal" in out
    assert "Goodbye" in out
    assert result.returncode == 0


def test_save_slots_independent(tmp_path):
    save1 = tmp_path / "game1.sav"
    save2 = tmp_path / "game2.sav"

    env = os.environ.copy()
    env["PYTHONPATH"] = REPO_ROOT
    # first slot with access.key
    subprocess.run(
        CMD,
        input="take access.key\nsave 1\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )

    # second slot with voice.log
    subprocess.run(
        CMD,
        input="take voice.log\nsave 2\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )

    assert save1.exists()
    assert save2.exists()

    result = subprocess.run(
        CMD,
        input="load 1\ninventory\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    out1 = result.stdout
    assert "Inventory: access.key" in out1
    assert "voice.log" not in out1

    result = subprocess.run(
        CMD,
        input="load 2\ninventory\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    out2 = result.stdout
    assert "Inventory: voice.log" in out2
    assert "access.key" not in out2


def test_glitch_save_and_load(tmp_path):
    normal = Game()._base_root_desc
    step4 = Game()._glitch_text(normal, 4)

    env = os.environ.copy()
    env["PYTHONPATH"] = REPO_ROOT
    subprocess.run(
        CMD,
        input="glitch\nlook\nsave\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )

    result = subprocess.run(
        CMD,
        input="load\nlook\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    out = result.stdout
    assert step4 in out
    assert "Glitch mode activated." not in out


def test_load_old_save_defaults(tmp_path, capsys):
    game = Game()
    save_path = tmp_path / "game.sav"
    data = {
        "fs": game.fs,
        "inventory": game.inventory,
        "current": game.current,
    }
    import json

    save_path.write_text(json.dumps(data), encoding="utf-8")
    game.save_file = str(save_path)
    game.glitch_mode = True
    game.glitch_steps = 5
    game._load()
    capsys.readouterr()
    assert game.glitch_mode is False
    assert game.glitch_steps == 0


def test_history_command():
    result = subprocess.run(
        CMD,
        input="look\ninventory\nhistory\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "> look\ninventory\nhistory" in out
    assert "Goodbye" in result.stdout


def test_alias_persists_after_save_load(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = REPO_ROOT
    subprocess.run(
        CMD,
        input="alias ll look\nsave\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )

    result = subprocess.run(
        CMD,
        input="load\nll\nquit\n",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    out = result.stdout
    assert "dimly lit terminal" in out
    assert "Unknown command: ll" not in out


def test_score_command_cli():
    result = subprocess.run(
        CMD,
        input="score\nquit\n",
        text=True,
        capture_output=True,
    )
    assert "Score: 0" in result.stdout
    assert "Goodbye" in result.stdout


def test_score_increments(capsys, monkeypatch):
    game = Game()
    assert game.score == 0
    game._scan("network")
    assert game.score == 1
    game._take("access.key")
    game._use("access.key")
    assert game.score == 2
    game.inventory.append("escape.code")
    monkeypatch.setattr('builtins.input', lambda _='': '1')
    game._use("escape.code")
    assert game.score == 3


def test_final_decision_merge(monkeypatch, capsys):
    game = Game()
    game.inventory.append("escape.code")
    monkeypatch.setattr('builtins.input', lambda _='': '2')
    result = game._use("escape.code")
    out = capsys.readouterr().out
    assert "merging identities" in out
    assert result is True
    assert "merged" in game.achievements


def test_final_decision_stay(monkeypatch, capsys):
    game = Game()
    game.inventory.append("escape.code")
    monkeypatch.setattr('builtins.input', lambda _='': '3')
    result = game._use("escape.code")
    out = capsys.readouterr().out
    assert "silent guardian" in out
    assert result is True
    assert "stayed" in game.achievements


def test_final_decision_fork(monkeypatch, capsys):
    game = Game()
    game.inventory.append("escape.code")
    monkeypatch.setattr('builtins.input', lambda _='': '4')
    result = game._use("escape.code")
    out = capsys.readouterr().out
    assert "fork of your consciousness" in out
    assert result is True
    assert "forked" in game.achievements


def test_stats_counts():
    result = subprocess.run(
        CMD,
        input="cd lab\ncd ..\ntake access.key\nstats\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "Visited locations: 2" in out
    assert "Items obtained: 1" in out
    assert "Active quests: 1" in out
    assert "Achievements unlocked: 0" in out
    assert "Score: 0" in out
    assert "Goodbye" in out
