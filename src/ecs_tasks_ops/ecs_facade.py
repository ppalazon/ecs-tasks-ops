"""ECS Facade for ecs-tasks-ops."""

import boto3

ecs_client = boto3.client('ecs')


def get_cluster_list():
    """Get a complete list with cluster information."""
    list_clusters = ecs_client.list_clusters()
    return ecs_client.describe_clusters(
        clusters=list_clusters.get('clusterArns', [])
    ).get('clusters', [])


def get_services(cluster):
    """Get information about all services defined in a cluster."""
    list_services = ecs_client.list_services(cluster=cluster).get('serviceArns', [])
    return ecs_client.describe_services(cluster=cluster, services=list_services).get('services', [])

