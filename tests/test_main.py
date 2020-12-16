"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner
from moto import mock_ec2
from moto import mock_ecs

from ecs_tasks_ops import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@mock_ecs
@mock_ec2
def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_cluster_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, args="clusters")
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_services_def(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main, args="services")
    assert result.exit_code == 0
    assert result.output == "Getting list of Services for 'default'\nNo data to show\n"


@mock_ecs
@mock_ec2
def test_main_services_cluster(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    cluster_name = "no-exist-cluster"
    result = runner.invoke(__main__.main, ["services", "-c", cluster_name])
    assert result.exit_code == 0
    print(result.output)
    assert (
        result.output
        == f"Getting list of Services for '{cluster_name}'\nNo data to show\n"
    )
