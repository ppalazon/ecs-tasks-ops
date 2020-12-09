"""Cache ecs data on a dictionary"""
from . import ecs_data

cache = {}


def get_clusters():
    return cache.setdefault("clusters", ecs_data.get_clusters())


def get_services(cluster_name):
    return cache.setdefault(
        cluster_name + ".services", ecs_data.get_services(cluster_name)
    )


def get_containers_instances(cluster_name):
    return cache.setdefault(
        cluster_name + ".container-instances",
        ecs_data.get_containers_instances(cluster_name),
    )


def get_tasks_cluster(cluster_name):
    return cache.setdefault(
        cluster_name + ".tasks", ecs_data.get_tasks_cluster(cluster_name)
    )


def get_tasks_service(cluster_name, service_name):
    return cache.setdefault(
        cluster_name + "." + service_name + ".tasks",
        ecs_data.get_tasks_service(cluster_name, service_name),
    )


def get_tasks_container_instance(cluster_name, containers_instance_arn):
    return cache.setdefault(
        cluster_name + "." + containers_instance_arn + ".tasks",
        ecs_data.get_tasks_container_instance(cluster_name, containers_instance_arn),
    )


def get_containers_service(cluster_name, service_name):
    return cache.setdefault(
        cluster_name + "." + service_name + ".containers",
        ecs_data.get_containers_service(cluster_name, service_name),
    )


def get_containers_tasks(cluster_name, task_arn):
    return cache.setdefault(
        cluster_name + "." + task_arn + ".containers",
        ecs_data.get_containers_tasks(cluster_name, task_arn),
    )
