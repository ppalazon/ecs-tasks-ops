"""Testing generate ssh commands."""
from moto import mock_ec2
from moto import mock_ecs
from tests.infrastructure import initialize_ecs_cluster
from tests.infrastructure import initialize_ecs_infrastructure

from ecs_tasks_ops import ecs_ssh

# from ecs_tasks_ops import ecs_data


@mock_ecs
@mock_ec2
def test_ssh_container_instance() -> None:
    """It exits with a status code of zero."""
    cluster = initialize_ecs_cluster("test-cluster")
    infrastructure = initialize_ecs_infrastructure(
        cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
    )

    for instance in infrastructure["instances"]:
        ssh_cmd = ecs_ssh.ssh_cmd_container_instance(instance)
        assert ssh_cmd.find("ssh") >= 0
        assert ssh_cmd.find(instance["ec2InstanceId"]) >= 0


# @mock_ecs
# @mock_ec2
# def test_ssh_task_log() -> None:
#     """It exits with a status code of zero."""

#     cluster = initialize_ecs_cluster("test-cluster")
#     infrastructure = initialize_ecs_infrastructure(
#         cluster, num_task_def=10, num_services=2, num_instances=3, num_tasks=3
#     )

#     instance_ids = [instance['ec2InstanceId'] for instance in infrastructure['instances']]

#     tasks = ecs_data.get_tasks_cluster("test-cluster")

#     for task in tasks:
#         ssh_cmd = ecs_ssh.ssh_cmd_task_log(task)
#         assert ssh_cmd.find("ssh") >= 0
#         assert any(id in ssh_cmd for id in instance_ids)
