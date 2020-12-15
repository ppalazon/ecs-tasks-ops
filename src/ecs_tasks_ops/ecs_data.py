"""Clean and improve ecs data json."""
from itertools import chain

from ecs_tasks_ops import ecs_facade


def improve_container_instance_info(cluster_name):
    """Extract more information about containers info for a specific cluster."""
    container_instances = ecs_facade.get_all_container_instances(cluster_name)
    for ci in container_instances:
        attrs = ci.get("attributes", [])
        attrs_vals = [a for a in attrs if "value" in a]
        ci["features"] = [a["name"] for a in attrs if "value" not in a]
        for attr in attrs_vals:
            ci[attr["name"]] = attr["value"]
        registered_resources = ci["registeredResources"]
        available_resources = ci["remainingResources"]
        ci["ami_id"] = next(obj for obj in attrs if obj["name"] == "ecs.ami-id")[
            "value"
        ]
        ci["instance_type"] = next(
            obj for obj in attrs if obj["name"] == "ecs.instance-type"
        )["value"]
        ci["availability_zone"] = next(
            obj for obj in attrs if obj["name"] == "ecs.availability-zone"
        )["value"]
        ci["available_memory"] = next(
            obj for obj in available_resources if obj["name"] == "MEMORY"
        )["integerValue"]
        ci["total_memory"] = next(
            obj for obj in registered_resources if obj["name"] == "MEMORY"
        )["integerValue"]
        ci["available_cpu"] = next(
            obj for obj in available_resources if obj["name"] == "CPU"
        )["integerValue"]
        ci["total_cpu"] = next(
            obj for obj in registered_resources if obj["name"] == "CPU"
        )["integerValue"]
        ci["taken_ports"] = ", ".join(
            sorted(
                next(obj for obj in available_resources if obj["name"] == "PORTS")[
                    "stringSetValue"
                ]
            )
        )
    return container_instances


def improve_tasks_info(cluster_name, tasks):
    """Get more information for a list of tasks."""
    containers_instances = get_containers_instances(cluster_name)
    for task in tasks:
        for inst in containers_instances:
            if inst["containerInstanceArn"] == task["containerInstanceArn"]:
                task["ec2InstanceId"] = inst["ec2InstanceId"]
        task["networks"] = [
            extract_network_from_docker_container(c) for c in task["containers"]
        ]
        # task['name'] = task['taskDefinitionArn'].split("/")[1] + " - " + task['taskArn'].split("/")[1]
        task["name"] = task["taskDefinitionArn"].split("/")[1]
    return tasks


def improve_one_tasks_info(cluster_name, task_arn):
    """Get more information from a cluster and task id."""
    tasks = ecs_facade.get_describe_tasks(cluster_name, [task_arn])
    return improve_tasks_info(cluster_name, tasks)


def improve_service_tasks_info(cluster_name, service_name):
    """Get more information for a list of task of a service."""
    tasks = ecs_facade.get_all_tasks_services(cluster_name, service_name)
    return improve_tasks_info(cluster_name, tasks)


def improve_container_instance_tasks_info(cluster_name, container_instance):
    """Get more information for a list of task of a container instance."""
    tasks = ecs_facade.get_all_tasks_container(cluster_name, container_instance)
    return improve_tasks_info(cluster_name, tasks)


def improve_cluster_tasks_info(cluster_name):
    """Get more infomation for a list of tasks of a cluster."""
    tasks = ecs_facade.get_all_tasks_cluster(cluster_name)
    return improve_tasks_info(cluster_name, tasks)


def extract_docker_containers(task):
    """Extract docker container information for a task."""
    containers = task.get("containers", [])
    for container in containers:
        container["ec2InstanceId"] = task.get("ec2InstanceId", "")
        container["networks"] = extract_network_from_docker_container(container)
    return containers


def extract_network_from_docker_container(docker_container):
    """Extract network information for a docker container."""
    network_bindings = docker_container.get("networkBindings")
    bindings = [
        network["bindIP"]
        + " ("
        + str(network["hostPort"])
        + "[host] -> "
        + str(network["containerPort"])
        + "[network])"
        for network in network_bindings
    ]
    if bindings is []:
        bindings = "no network binding"
    else:
        bindings = ", ".join(bindings)
    return docker_container["name"] + " -> " + bindings


def improve_docker_container_info(cluster_name, service_name):
    """Get a list of docker container for a list of task of a service."""
    tasks = improve_service_tasks_info(cluster_name, service_name)
    containers = list(
        chain.from_iterable([extract_docker_containers(task) for task in tasks])
    )
    return containers


def improve_docker_container_task_info(cluster_name, task_arn):
    """Get a list of docker container for a list of task of a task."""
    tasks = improve_one_tasks_info(cluster_name, task_arn)
    containers = list(
        chain.from_iterable([extract_docker_containers(task) for task in tasks])
    )
    return containers


def get_clusters():
    """Get a complete list of clusters."""
    return ecs_facade.get_cluster_list()


def get_services(cluster_name):
    """Get a complete list of services by cluster."""
    return ecs_facade.get_all_services(cluster_name)


def get_containers_instances(cluster_name):
    """Get a complete list of container instances by cluster."""
    return improve_container_instance_info(cluster_name)


def get_tasks_cluster(cluster_name):
    """Get a complete list of task by cluster."""
    return improve_cluster_tasks_info(cluster_name)


def get_tasks_service(cluster_name, service_name):
    """Get a complete list of services by clusters."""
    return improve_service_tasks_info(cluster_name, service_name)


def get_tasks_container_instance(cluster_name, containers_instance_arn):
    """Get a complete info for a container instance in a cluster."""
    return improve_container_instance_tasks_info(cluster_name, containers_instance_arn)


def get_containers_service(cluster_name, service_name):
    """Get a list of docker containers by a service and cluster."""
    return improve_docker_container_info(cluster_name, service_name)


def get_containers_tasks(cluster_name, task_arn):
    """Get a list of docker containers by task."""
    return improve_docker_container_task_info(cluster_name, task_arn)
