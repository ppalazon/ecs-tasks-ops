"""Intialization of ECS Tasks Operations qt5 UI"""
import click

from ecs_tasks_ops_urwid import urwid_gui


@click.version_option()
def main() -> None:
    """Open Urwid User Interface."""
    urwid_gui.main_gui()


if __name__ == "__main__":
    pass
