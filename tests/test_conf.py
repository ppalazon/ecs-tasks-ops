"""Test configuration file."""
from unittest.mock import mock_open
from unittest.mock import patch

from ecs_tasks_ops import ecs_conf


@patch("builtins.open", new_callable=mock_open, read_data="{}")
def test_get_conf(mock_file):
    """Get basic configuration."""
    ecs_conf.load_config()
    assert ecs_conf.cfg == {}


@patch("builtins.open", new_callable=mock_open, read_data='{"commands": ["/bin/bash"]}')
def test_get_conf_commands(mock_file):
    """Get basic configuration."""
    ecs_conf.load_config()
    assert ecs_conf.cfg["commands"] == ["/bin/bash"]
