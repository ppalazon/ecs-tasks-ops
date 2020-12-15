"""Cache ecs data on a dictionary."""
from . import ecs_data

cache = {}


def get_clusters():
    """Get s cached list of clusters."""
    return cache.setdefault("clusters", ecs_data.get_clusters())


def get_services(cluster_name):
    """Get a cached list of services."""
    return cache.setdefault(
        cluster_name + ".services", ecs_data.get_services(cluster_name)
    )


def get_containers_instances(cluster_name):
    """Get a cached list of container instances by cluster name."""
    return cache.setdefault(
        cluster_name + ".container-instances",
        ecs_data.get_containers_instances(cluster_name),
    )


def get_tasks_cluster(cluster_name):
    """Get a cached list of tasks by cluster name."""
    return cache.setdefault(
        cluster_name + ".tasks", ecs_data.get_tasks_cluster(cluster_name)
    )


def get_tasks_service(cluster_name, service_name):
    """Get a cached list of services by cluster and service name."""
    return cache.setdefault(
        cluster_name + "." + service_name + ".tasks",
        ecs_data.get_tasks_service(cluster_name, service_name),
    )


def get_tasks_container_instance(cluster_name, containers_instance_arn):
    """Get a cache list of task by cluster and container instance."""
    return cache.setdefault(
        cluster_name + "." + containers_instance_arn + ".tasks",
        ecs_data.get_tasks_container_instance(cluster_name, containers_instance_arn),
    )


def get_containers_service(cluster_name, service_name):
    """Get a cached list of container instances by cluster and service name."""
    return cache.setdefault(
        cluster_name + "." + service_name + ".containers",
        ecs_data.get_containers_service(cluster_name, service_name),
    )


def get_containers_tasks(cluster_name, task_arn):
    """Get a cached list of docker instances by cluster and task id."""
    return cache.setdefault(
        cluster_name + "." + task_arn + ".containers",
        ecs_data.get_containers_tasks(cluster_name, task_arn),
    )
