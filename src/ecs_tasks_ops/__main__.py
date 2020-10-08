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
    """Show information about all cluster defined"""
    click.secho("Getting list of ECS cluster", fg="green")
    clusters = ecs_facade.get_cluster_list()
    click.echo(pretty_table.tabulate_list_json(clusters, fields_to=7))


if __name__ == "__main__":
    main(prog_name="ecs-tasks-ops")  # pragma: no cover
