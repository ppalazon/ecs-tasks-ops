"""Urwind GUI for ECS tasks ops."""

import urwid

txt = urwid.Text(u"Hello World")

def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    txt.set_text(repr(key))

def main_gui():
    fill = urwid.Filler(txt, 'top')
    loop = urwid.MainLoop(fill, unhandled_input=show_or_exit)
    loop.run()
