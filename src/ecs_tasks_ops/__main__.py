"""Command-line interface."""
import json
import click
import curses
from curses import wrapper
from . import ecs_data
from . import ecs_facade
from . import pretty_table
#from . import urwid_gui
from .pretty_json import get_pretty_json_str


@click.group()
@click.option('-x', '--debug/--no-debug', default=False)
@click.option('-j', '--output-json', "output_json", is_flag=True, default=False)
@click.version_option()
@click.pass_context
def main(ctx, debug, output_json) -> None:
    """Ecs Tasks Ops."""
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ## TODO: Format output with json
    ctx.obj['OUT_JSON'] = output_json


@main.command('clusters')
@click.pass_context
def main_clusters(ctx):
    """Clusters information."""
    if not ctx.obj['OUT_JSON']:
        click.secho("Getting list of ECS cluster", fg="green")
    clusters = ecs_data.get_clusters()
    if ctx.obj['OUT_JSON']:
        click.echo(get_pretty_json_str(clusters))
    else:
        click.echo(pretty_table.tabulate_list_json(clusters, fields_to=7))


@main.command('services')
@click.option('-c', '--cluster-name', default='default', help='Cluster name')
@click.pass_context
def main_services(ctx, cluster_name):
    """Services defined in a cluster."""
    click.secho(f"Getting list of Services for '{cluster_name}'", fg="green")
    try:
        services_info = ecs_data.get_services(cluster_name)
        if ctx.obj['OUT_JSON']:
            click.echo(get_pretty_json_str(services_info))
        else:
            click.echo(pretty_table.tabulate_list_json_keys(
                services_info, ['serviceArn', 'serviceName', 'status', 'runningCount', 'desiredCount']))
        
    except ecs_facade.ecs_client.exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []


@main.command('container-instances')
@click.option('-c', '--cluster-name', default='default', help='Cluster name')
@click.pass_context
def main_container_instances(ctx, cluster_name):
    """Container instances defined in a cluster."""
    click.secho(f"Getting list of Container instances for '{cluster_name}'", fg="green")
    try:
        container_instances_info = ecs_data.get_containers_instances(cluster_name)
        if ctx.obj['OUT_JSON']:
            click.echo(get_pretty_json_str(container_instances_info))
        else:
            click.echo(pretty_table.tabulate_list_json_keys(
                container_instances_info, ['ec2InstanceId', 'versionInfo']))
        
    except ecs_facade.ecs_client.exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []


@main.command('tasks')
@click.option('-c', '--cluster-name', default='default', help='Cluster name')
@click.option('-s', '--service-name', default='', help='Service name')
@click.pass_context
def main_tasks(ctx, cluster_name, service_name):
    """Set tasks defined in a cluster."""
    click.secho(f"Getting list of Tasks on '{cluster_name}' for '{service_name}'", fg="green")
    try:
        tasks_info = ecs_data.get_tasks_service(cluster_name, service_name)
        
        if ctx.obj['OUT_JSON']:
            click.echo(get_pretty_json_str(tasks_info))
        else:
            click.echo(pretty_table.tabulate_list_json_keys(
                tasks_info, ['taskArn', 'ec2InstanceId', 'availabilityZone', 'memory', 'cpu', 'desiredStatus', 'healthStatus', 'lastStatus']))
        
    except ecs_facade.ecs_client.exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []


@main.command('containers')
@click.option('-c', '--cluster-name', default='default', help='Cluster name')
@click.option('-s', '--service-name', default='', help='Service name')
@click.option('-d', '--docker-name', help='Docker container name')
@click.pass_context
def main_containers(ctx, cluster_name, service_name, docker_name):
    """Get docker containers defined in a cluster."""
    click.secho(f"Getting docker containers on '{cluster_name}' for '{service_name}'", fg="green")
    try:
        containers_info = ecs_data.get_containers_service(cluster_name, service_name)

        if docker_name:
            containers_info = [c for c in containers_info if c['name'] == docker_name]

        if ctx.obj['OUT_JSON']:
            click.echo(get_pretty_json_str(containers_info))
        else:
            click.echo(pretty_table.tabulate_list_json_keys(
                containers_info, ['image', 'ec2InstanceId', 'name', 'memory', 'cpu', 'runtimeId', 'healthStatus', 'lastStatus']))
        
    except ecs_facade.ecs_client.exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []


# @main.command('gui')
# @click.pass_context
# def main_urwid(ctx):
#     """Testing urwid gui."""
#     urwid_gui.main_gui()


if __name__ == "__main__":
    # main(prog_name="ecs-tasks-ops")  # pragma: no cover
    pass
