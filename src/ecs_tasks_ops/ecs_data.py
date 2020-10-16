"""Clean and improve ecs data json"""


from . import ecs_facade
from itertools import chain


ecs_data = {}

def improve_container_instance_info(cluster_name):
    containers = ecs_facade.get_all_container_instances(cluster_name)
    for c in containers:
        attrs = c.get('attributes', [])
        attrs_vals = [a for a in attrs if 'value' in a]
        c['features'] = [a['name'] for a in attrs if 'value' not in a]
        for attr in attrs_vals:
            c[attr['name']] = attr['value']
        c['attributes'] = None
    return containers


def improve_tasks_info(cluster_name, tasks):
    containers_instances = get_containers_instances(cluster_name)
    for task in tasks:
        for inst in containers_instances:
            if inst['containerInstanceArn'] == task['containerInstanceArn']:
                task['ec2InstanceId'] = inst['ec2InstanceId']
        task['networks'] = [extract_network_from_docker_container(c) for c in task['containers']]
        task['name'] = task['taskDefinitionArn'].split("/")[1] + " - " + task['taskArn'].split("/")[1]
    return tasks


def improve_service_tasks_info(cluster_name, service_name):
    tasks = ecs_facade.get_all_tasks_services(cluster_name, service_name)
    return improve_tasks_info(cluster_name, tasks)


def improve_container_instance_tasks_info(cluster_name, container_instance):
    tasks = ecs_facade.get_all_tasks_container(cluster_name, container_instance)
    return improve_tasks_info(cluster_name, tasks)


def improve_cluster_tasks_info(cluster_name):
    tasks = ecs_facade.get_all_tasks_cluster(cluster_name)
    return improve_tasks_info(cluster_name, tasks)


def extract_docker_containers(task):
    containers = task.get('containers', [])
    for container in containers:
        container['ec2InstanceId'] = task.get('ec2InstanceId', '')
    return containers


def extract_network_from_docker_container(docker_container):
    network_bindings = docker_container['networkBindings']
    bindings = [network['bindIP'] + " (" + str(network['hostPort']) + "[host] -> " + str(
        network['containerPort']) + "[network])" for network in network_bindings]
    if bindings is []:
        bindings = "no network binding"
    else:
        bindings = ', '.join(bindings)
    return docker_container['name'] + " -> " + bindings


def improve_docker_container_info(cluster_name, service_name):
    tasks = get_tasks_service(cluster_name, service_name)
    containers = list(chain.from_iterable([extract_docker_containers(task) for task in tasks]))
    return containers


def get_clusters():
    return ecs_data.setdefault("clusters", ecs_facade.get_cluster_list())


def get_services(cluster_name):
    return ecs_data.setdefault(cluster_name+".services", ecs_facade.get_all_services(cluster_name))


def get_containers_instances(cluster_name):
    return ecs_data.setdefault(cluster_name+".container-instances", improve_container_instance_info(cluster_name))


def get_tasks_cluster(cluster_name):
    return ecs_data.setdefault(cluster_name+".tasks", improve_cluster_tasks_info(cluster_name))


def get_tasks_service(cluster_name, service_name):
    return ecs_data.setdefault(cluster_name+"."+service_name+".tasks", improve_service_tasks_info(cluster_name, service_name))


def get_tasks_container_instance(cluster_name, containers_instance_arn):
    return ecs_data.setdefault(cluster_name+"."+containers_instance_arn+".tasks", improve_container_instance_tasks_info(cluster_name, containers_instance_arn))


def get_containers_service(cluster_name, service_name):
    return ecs_data.setdefault(cluster_name+"."+service_name+".containers", improve_docker_container_info(cluster_name, service_name))