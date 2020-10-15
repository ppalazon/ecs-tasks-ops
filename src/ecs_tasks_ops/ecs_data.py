"""Clean and improve ecs data json"""


from . import ecs_facade
from itertools import chain


ecs_data = {}


def _get_tasks_service_improve(cluster_name, service_name):
    tasks = ecs_facade.get_all_tasks(cluster_name, service_name)
    containers_instances = get_containers_instances(cluster_name)
    for task in tasks:
        for inst in containers_instances:
            if inst['containerInstanceArn'] == task['containerInstanceArn']:
                task['ec2InstanceId'] = inst['ec2InstanceId']
    return tasks


def _get_container_instance_info(task):
    containers = task.get('containers', [])
    for container in containers:
        container['ec2InstanceId'] = task.get('ec2InstanceId', '')
    return containers


def _get_containers_service_improve(cluster_name, service_name):
    tasks = _get_tasks_service_improve(cluster_name, service_name)
    containers = list(chain.from_iterable([_get_container_instance_info(task) for task in tasks]))
    return containers


def get_clusters():
    return ecs_data.setdefault("clusters", ecs_facade.get_cluster_list())


def get_services(cluster_name):
    return ecs_data.setdefault(cluster_name+".services", ecs_facade.get_all_services(cluster_name))


def get_containers_instances(cluster_name):
    return ecs_data.setdefault(cluster_name+".container-instances", ecs_facade.get_all_container_instances(cluster_name))


def get_tasks_service(cluster_name, service_name):
    return ecs_data.setdefault(cluster_name+"."+service_name+".tasks", _get_tasks_service_improve(cluster_name, service_name))


def get_containers_service(cluster_name, service_name):
    return ecs_data.setdefault(cluster_name+"."+service_name+".containers", _get_containers_service_improve(cluster_name, service_name))