"""Command-line interface."""
import click
from . import ecs_facade
from . import pretty_table


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
    clusters = ecs_facade.get_cluster_list()
    if ctx.obj['OUT_JSON']:
        click.echo(clusters)
    else:
        click.echo(pretty_table.tabulate_list_json(clusters, fields_to=7))


@main.command('services')
@click.option('-c', '--cluster', default='default', help='Cluster name')
@click.pass_context
def main_services(ctx, cluster_name):
    """Services defined in a cluster."""
    click.secho(f"Getting list of Services for '{cluster_name}'", fg="green")
    try:
        services_info = ecs_facade.get_services(cluster_name)
        click.echo(pretty_table.tabulate_list_json_keys(
            services_info, ['serviceArn', 'serviceName', 'status', 'runningCount', 'desiredCount']))
    except ecs_facade.ecs_client.exceptions.ClusterNotFoundException:
        click.secho(f"Cluster {cluster_name} not found", fg="red")
        return []


if __name__ == "__main__":
    main(prog_name="ecs-tasks-ops")  # pragma: no cover
