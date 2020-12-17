"""Utils to create a fictional infrastructure."""
import secrets

import boto3

from ecs_tasks_ops import ecs_facade
from ecs_tasks_ops import pretty_json

random = secrets.SystemRandom()


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
        "tasks": [],
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
                instanceIdentityDocument=pretty_json.dumps(iid, indent=None),
            )["containerInstance"]
            infrastructure["instances"].append(container_instance)
            for nr in range(num_tasks):
                task_definition = infrastructure["task_defintions"][
                    random.randrange(0, num_task_def)
                ]
                task_definition_arn = task_definition["taskDefinitionArn"]
                print(f"Creating {nr} tasks for {task_definition_arn}")
                container_arns = [container_instance["containerInstanceArn"]]
                task = ecs_client.start_task(
                    cluster=cluster_name,
                    containerInstances=container_arns,
                    taskDefinition=task_definition_arn,
                )
                add_docker_container_info(task, task_definition)
                infrastructure["tasks"].append(task)

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


def add_docker_container_info(task, task_definition):
    """Add information about docker containers in a task."""
    task["containers"] = []
    for container_def in task_definition["containerDefinitions"]:
        container_run = {
            "containerArn": "arn:aws:ecs:eu-west-1:12345678910:container/aa32446b-b8a9-4ee8-b06b-9fc26ec2baac",
            "taskArn": task_definition["taskDefinitionArn"],
            "name": container_def["name"],
            "image": container_def["image"],
            "imageDigest": f"sha256:{secrets.token_hex(64)}",
            "runtimeId": secrets.token_hex(64),
            "lastStatus": "RUNNING",
            "networkBindings": [
                {
                    "bindIP": "10.0.0.100",
                    "containerPort": random.randrange(1024, 65535),
                    "hostPort": random.randrange(1024, 65535),
                    "protocol": "tcp",
                }
            ],
            "networkInterfaces": [],
            "healthStatus": "UNKNOWN",
            "cpu": container_def["cpu"],
            "memoryReservation": container_def["memory"],
        }
        task["containers"].append(container_run)
