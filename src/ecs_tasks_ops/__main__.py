"""Command-line interface."""
import click
from . import ecs_facade
from . import pretty_table


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.version_option()
def main(debug) -> None:
    """Ecs Tasks Ops."""
    pass


@main.command()
def cluster():
    """Clusters information."""
    click.secho("Getting list of ECS cluster", fg="green")
    clusters = ecs_facade.get_cluster_list()
    click.echo(pretty_table.tabulate_list_json(clusters, fields_to=7))


@main.command()
@click.option('-c', '--cluster', default='default')
def services(cluster):
    """Services defined in a cluster."""
    click.secho(f"Getting list of Services for '{cluster}'", fg="green")
    services = ecs_facade.get_services(cluster)
    click.echo(pretty_table.tabulate_list_json_keys(services, ['serviceArn', 'serviceName', 'status', 'runningCount',
                                                               'desiredCount']))


if __name__ == "__main__":
    main(prog_name="ecs-tasks-ops")  # pragma: no cover
