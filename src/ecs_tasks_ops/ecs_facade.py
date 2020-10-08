"""ECS Facade for ecs-tasks-ops."""

import boto3

ecs_client = boto3.client('ecs')


def get_cluster_list():
    """Get a complete list with cluster information."""
    list_clusters = ecs_client.list_clusters()
    return ecs_client.describe_clusters(
        clusters=list_clusters.get('clusterArns', [])
    ).get('clusters', [])
