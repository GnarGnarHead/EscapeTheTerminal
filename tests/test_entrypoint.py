import subprocess
import sys
import importlib.metadata


def test_console_script_invocation():
    # Ensure the console entry point is registered
    eps = importlib.metadata.entry_points()
    names = [ep.name for ep in eps.select(group='console_scripts')]
    assert 'escape-terminal' in names

    result = subprocess.run(
        [sys.executable, '-m', 'escape'],
        input='quit\n',
        text=True,
        capture_output=True,
    )
    assert 'Goodbye' in result.stdout
    assert result.returncode == 0


def test_world_option(tmp_path):
    import json
    import os

    world = tmp_path / 'world.json'
    world.write_text(
        json.dumps(
            {
                'fs': {'desc': 'Custom root', 'items': [], 'dirs': {}},
                'hidden_dir': {'desc': '', 'items': [], 'dirs': {}},
                'network_node': {'desc': '', 'items': [], 'dirs': {}, 'locked': False},
                'deep_network_node': {'desc': '', 'items': [], 'dirs': {}, 'locked': False},
                'npc_locations': {},
                'item_descriptions': {},
            }
        )
    )

    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.dirname(__file__))
    result = subprocess.run(
        [sys.executable, '-m', 'escape', '--world', str(world)],
        input='look\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    out = result.stdout
    assert 'Custom root' in out
    assert 'Goodbye' in out
