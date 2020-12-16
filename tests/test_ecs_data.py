"""Testing ecs_data module with mock_ecs."""
import secrets

import boto3
from moto import mock_ec2
from moto import mock_ecs

from ecs_tasks_ops import ecs_data
from ecs_tasks_ops import ecs_facade
from ecs_tasks_ops import pretty_json

random = secrets.SystemRandom()


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


def initialize_ecs_cluster(cluster_name="default"):
    """Initialize a cluster."""
    ecs_client = ecs_facade.ecs_client()
    return ecs_client.create_cluster(clusterName=cluster_name)["cluster"]


def initialize_ecs_infrastructure(
    cluster, num_task_def=10, num_services=0, num_instances=0, num_tasks=0
):
    """Initialize a list a infraestructure for a cluser."""
    ecs_client = ecs_facade.ecs_client()
    ec2_client = boto3.client("ec2")

    cluster_name = cluster["clusterName"]

    infrastructure = {
        "cluster": cluster,
        "task_defintions": [],
        "services": [],
        "instances": [],
    }

    for t in range(num_task_def):
        cd = [{"name": f"task-def-{t}", "image": "image-test", "cpu": 10, "memory": 10}]
        task_def = ecs_client.register_task_definition(
            family=f"family-{t}-task-def", containerDefinitions=cd
        )
        infrastructure["task_defintions"].append(task_def["taskDefinition"])

    images = ec2_client.describe_images()["Images"]

    if num_instances > 0:
        image_id = images[random.randrange(0, len(images))]["ImageId"]
        instances = ec2_client.run_instances(
            MaxCount=num_instances, MinCount=num_instances, ImageId=image_id
        )
        for instance in instances["Instances"]:
            iid = {
                "accountId": "12345678910",
                "architecture": "x86_64",
                "availabilityZone": "eu-west-1b",
                "imageId": image_id,
                "instanceId": instance["InstanceId"],
                "instanceType": instance["InstanceType"],
                "pendingTime": "2020-11-18T22:00:02Z",
                "privateIp": instance["PrivateIpAddress"],
                "region": instance["Placement"]["AvailabilityZone"],
                "version": "2017-09-30",
            }
            container_instance = ecs_client.register_container_instance(
                cluster=cluster_name,
                instanceIdentityDocument=pretty_json.dumps(iid, indent=0),
            )["containerInstance"]
            infrastructure["instances"].append(container_instance)
            for nr in range(num_tasks):
                task_definition_arn = infrastructure["task_defintions"][
                    random.randrange(0, num_task_def)
                ]["taskDefinitionArn"]
                print(f"Creating {nr} tasks for {task_definition_arn}")
                container_arns = [container_instance["containerInstanceArn"]]
                ecs_client.start_task(
                    cluster=cluster_name,
                    containerInstances=container_arns,
                    taskDefinition=task_definition_arn,
                )

    for i in range(num_services):
        task_definition_arn = infrastructure["task_defintions"][
            random.randrange(0, num_task_def)
        ]["taskDefinitionArn"]
        ecs_client.create_service(
            cluster=cluster_name,
            serviceName=f"service-{i}",
            deploymentController={"type": "ECS"},
            taskDefinition=task_definition_arn,
            desiredCount=1,
        )

    return infrastructure
