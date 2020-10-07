"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Ecs Tasks Ops."""


if __name__ == "__main__":
    main(prog_name="ecs-tasks-ops")  # pragma: no cover
