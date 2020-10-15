"""Urwind GUI for ECS tasks ops."""

import urwid
import string
import json
from datetime import datetime
import subprocess
from .urwid_widgets import RefreshableItems
from .urwid_widgets import BodyController


def exit_on_cr(key):
    if isinstance(key, str) and key in 'Q':
        raise urwid.ExitMainLoop()


PALETTE = [('title', 'yellow', 'dark blue'),
           ('reveal focus', 'black', 'white'),
           ('key', 'yellow', 'dark blue', ('standout','underline'))]
FOOTER = urwid.AttrMap(urwid.Text(
    u'Press \'U\' to update, \'<enter>\' to look at sub-resources,\'D\' to look at more detail, \'B\' to go back to '
    u'the previous page and \'Q\' to quit'), 'title')


#BODY_CONTROLLER = BodyController(RefreshableItems(retrieve_clusters, []))


LAYOUT = urwid.Frame(body=urwid.Text("Testing"), footer=FOOTER)


def main_gui():
    main_loop = urwid.MainLoop(LAYOUT, palette=PALETTE, unhandled_input=exit_on_cr)
    main_loop.run()

