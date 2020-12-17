"""Testing ecs_data module with mock_ecs."""
from moto import mock_ec2
from moto import mock_ecs
from tests.infrastructure import initialize_ecs_cluster
from tests.infrastructure import initialize_ecs_infrastructure

from ecs_tasks_ops import ecs_data


@mock_ecs
@mock_ec2
def test_get_clusters():
    """Test get a list of clusters."""
    clusters = ecs_data.get_clusters()
    assert len(clusters) == 0


@mock_ecs
@mock_ec2
def test_get_clusters_1():
    """Test get a list of clusters with one cluster."""
    initialize_ecs_cluster("test-cluster")
    clusters = ecs_data.get_clusters()
    assert len(clusters) == 1


@mock_ecs
@mock_ec2
def test_get_services_def():
    """Test get a list of services."""
    initialize_ecs_cluster("test-cluster")
    services = ecs_data.get_services("default")
    assert len(services) == 0


@mock_ecs
@mock_ec2
def test_get_services_2():
    """Test get a list of 2 services."""
    cluster_name = "test-cluster"
    cluster = initialize_ecs_cluster(cluster_name)
    initialize_ecs_infrastructure(cluster, num_services=2)
    services = ecs_data.get_services(cluster_name)
    assert len(services) == 2


@mock_ecs
@mock_ec2
def test_get_services_100():
    """Test get a list of 100 clusters."""
    cluster_name = "test-cluster"
    cluster = initialize_ecs_cluster(cluster_name)
    initialize_ecs_infrastructure(cluster, num_services=100)
    services = ecs_data.get_services(cluster_name)
    assert len(services) == 100


@mock_ecs
@mock_ec2
def test_get_container_instances_100():
    """Test get a list of 100 instances."""
    cluster_name = "test-cluster"
    cluster = initialize_ecs_cluster(cluster_name)
    initialize_ecs_infrastructure(cluster, num_instances=100)
    isnstances = ecs_data.get_containers_instances(cluster_name)
    assert len(isnstances) == 100


@mock_ecs
@mock_ec2
def test_get_tasks_n():
    """Test get a list of tasks percluster and instance."""
    cluster_name = "test-cluster"
    cluster = initialize_ecs_cluster(cluster_name)
    num_services = 5
    num_instances = 10
    num_tasks = 3
    infraestructure = initialize_ecs_infrastructure(
        cluster,
        num_services=num_services,
        num_instances=num_instances,
        num_tasks=num_tasks,
    )

    services = ecs_data.get_services(cluster_name)
    assert len(services) == num_services
    instances = ecs_data.get_containers_instances(cluster_name)
    assert len(instances) == num_instances
    tasks_cluster = ecs_data.get_tasks_cluster(cluster_name)
    assert len(tasks_cluster) == num_tasks * num_instances
    for instance in infraestructure["instances"]:
        tasks_ins = ecs_data.get_tasks_container_instance(
            cluster_name, instance["containerInstanceArn"]
        )
        assert len(tasks_ins) == num_tasks
