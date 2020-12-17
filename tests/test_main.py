"""Test cases for the __main__ module."""
import json

import pytest
from click.testing import CliRunner
from moto import mock_ec2
from moto import mock_ecs
from tests.infrastructure import initialize_ecs_cluster
from tests.infrastructure import initialize_ecs_infrastructure

from ecs_tasks_ops import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@mock_ecs
@mock_ec2
def test_main_succeeds(runner: CliRunner) -> None:
    """Show help."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_no_infra_cluster_succeeds(runner: CliRunner) -> None:
    """Show clusters, but there aren't any."""
    result = runner.invoke(__main__.main, args="clusters")
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_no_infra_services_succeeds(runner: CliRunner) -> None:
    """Show services, but there aren't any."""
    result = runner.invoke(__main__.main, args="services")
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_no_infra_tasks_succeeds(runner: CliRunner) -> None:
    """Show tasks, but there aren't any."""
    result = runner.invoke(__main__.main, args="tasks")
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_no_infra_containers_error(runner: CliRunner) -> None:
    """Show containers, but fails without service name."""
    result = runner.invoke(__main__.main, args="containers")
    assert result.exit_code != 0


@mock_ecs
@mock_ec2
def test_main_no_infra_containers_succeeds(runner: CliRunner) -> None:
    """Show containers, but there aren't any."""
    result = runner.invoke(__main__.main, args=["containers", "-s", "invented"])
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_no_infra_containers_instances_succeeds(runner: CliRunner) -> None:
    """Show containers instances, but there aren't any."""
    result = runner.invoke(__main__.main, args="container-instances")
    assert result.exit_code == 0


@mock_ecs
@mock_ec2
def test_main_infra_cluster_succeeds(runner: CliRunner) -> None:
    """Show a cluster."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(__main__.main, args=["clusters"])
    assert result.exit_code == 0
    assert result.output.find("test-cluster") >= 0


@mock_ecs
@mock_ec2
def test_main_infra_services_succeeds(runner: CliRunner) -> None:
    """Show 2 services."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(__main__.main, args=["services", "-c", "test-cluster"])
    assert result.exit_code == 0
    assert result.output.find("service-0") >= 0
    assert result.output.find("service-1") >= 0
    assert len(result.output.split("\n")) == 5


@mock_ecs
@mock_ec2
def test_main_infra_containers_instances_succeeds(runner: CliRunner) -> None:
    """Show 3 instances."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(
        __main__.main, args=["container-instances", "-c", "test-cluster"]
    )
    assert result.exit_code == 0
    assert result.output.find("ec2InstanceId") >= 0
    assert len(result.output.split("\n")) == 6


@mock_ecs
@mock_ec2
def test_main_infra_tasks_succeeds(runner: CliRunner) -> None:
    """Show cluster tasks."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(__main__.main, args=["tasks", "-c", "test-cluster"])
    assert result.exit_code == 0
    assert result.output.find("taskArn") >= 0
    assert len(result.output.split("\n")) == 12


@mock_ecs
@mock_ec2
def test_main_infra_tasks_service_succeeds(runner: CliRunner) -> None:
    """Show services tasks, there's a problem with the mock."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(
        __main__.main, args=["tasks", "-c", "test-cluster", "-s", "service-1"]
    )
    assert result.exit_code == 0
    assert result.output.find("taskArn") >= 0
    assert len(result.output.split("\n")) == 12


@mock_ecs
@mock_ec2
def test_main_infra_tasks_containers_succeeds(runner: CliRunner) -> None:
    """Show tasks in a container instance."""
    cluster = initialize_ecs_cluster("test-cluster")
    infrastructure = initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    instance_ids = [
        instance["containerInstanceArn"] for instance in infrastructure["instances"]
    ]

    for instance_id in instance_ids:
        result = runner.invoke(
            __main__.main, args=["tasks", "-c", "test-cluster", "-i", instance_id]
        )
        assert result.exit_code == 0
        assert result.output.find("taskArn") >= 0
        assert len(result.output.split("\n")) == 6


@mock_ecs
@mock_ec2
def test_main_infra_containers_succeeds(runner: CliRunner) -> None:
    """It fails showing containers without service name."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(__main__.main, args=["containers", "-c", "test-cluster"])
    assert result.exit_code != 1


@mock_ecs
@mock_ec2
def test_main_infra_containers_service_succeeds(runner: CliRunner) -> None:
    """Show docker contatiners per service, moto mock doesn't work fine."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(
        __main__.main, args=["containers", "-c", "test-cluster", "-s", "service-1"]
    )
    assert result.exit_code == 0
    assert result.output.find("No data to show") >= 0


@mock_ecs
@mock_ec2
def test_main_infra_cluster_succeeds_json(runner: CliRunner) -> None:
    """Show json with clusters."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(__main__.main, args=["-j", "clusters"])
    assert result.exit_code == 0
    assert result.output.find("test-cluster") >= 0
    json_load = json.loads(result.output)
    assert json_load is not None


@mock_ecs
@mock_ec2
def test_main_infra_services_succeeds_json(runner: CliRunner) -> None:
    """Show json with services."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(__main__.main, args=["-j", "services", "-c", "test-cluster"])
    assert result.exit_code == 0
    assert result.output.find("test-cluster") >= 0
    assert result.output.find("service-0") >= 0
    assert result.output.find("service-1") >= 0
    json_load = json.loads(result.output)
    assert json_load is not None


@mock_ecs
@mock_ec2
def test_main_infra_containers_instances_succeeds_json(runner: CliRunner) -> None:
    """Show json with containers intances."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(
        __main__.main, args=["-j", "container-instances", "-c", "test-cluster"]
    )
    assert result.exit_code == 0
    assert result.output.find("ec2InstanceId") >= 0
    json_load = json.loads(result.output)
    assert json_load is not None


@mock_ecs
@mock_ec2
def test_main_infra_tasks_succeeds_json(runner: CliRunner) -> None:
    """Show json tasks in a cluster."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(__main__.main, args=["-j", "tasks", "-c", "test-cluster"])
    assert result.exit_code == 0
    assert result.output.find("test-cluster") >= 0
    assert result.output.find("taskArn") >= 0
    json_load = json.loads(result.output)
    assert json_load is not None


@mock_ecs
@mock_ec2
def test_main_infra_tasks_service_succeeds_json(runner: CliRunner) -> None:
    """Show json tasks in a service."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(
        __main__.main, args=["-j", "tasks", "-c", "test-cluster", "-s", "service-1"]
    )
    assert result.exit_code == 0
    assert result.output.find("test-cluster") >= 0
    assert result.output.find("taskArn") >= 0
    json_load = json.loads(result.output)
    assert json_load is not None


@mock_ecs
@mock_ec2
def test_main_infra_tasks_containers_succeeds_json(runner: CliRunner) -> None:
    """Show json with task in a container instance."""
    cluster = initialize_ecs_cluster("test-cluster")
    infrastructure = initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    instance_ids = [
        instance["containerInstanceArn"] for instance in infrastructure["instances"]
    ]

    for instance_id in instance_ids:
        result = runner.invoke(
            __main__.main, args=["-j", "tasks", "-c", "test-cluster", "-i", instance_id]
        )
        assert result.exit_code == 0
        assert result.output.find("test-cluster") >= 0
        assert result.output.find("taskArn") >= 0
        json_load = json.loads(result.output)
        assert json_load is not None


@mock_ecs
@mock_ec2
def test_main_infra_containers_succeeds_json(runner: CliRunner) -> None:
    """Fails json with docker containers in a cluster without a service."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(
        __main__.main, args=["-j", "containers", "-c", "test-cluster"]
    )
    assert result.exit_code != 0


@mock_ecs
@mock_ec2
def test_main_infra_containers_service_succeeds_json(runner: CliRunner) -> None:
    """Show json with docker containers in a service."""
    cluster = initialize_ecs_cluster("test-cluster")
    initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    result = runner.invoke(
        __main__.main,
        args=["-j", "containers", "-c", "test-cluster", "-s", "service-1"],
    )
    assert result.exit_code == 0
    json_load = json.loads(result.output)
    assert json_load is not None
