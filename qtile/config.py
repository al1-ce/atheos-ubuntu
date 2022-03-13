
import os
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, EzKey
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
mybrowser = "min"
terminal = guess_terminal()
home = os.path.expanduser('~')
spawnshortcuts = "qutebrowser " + home + "/.dotfiles/.shortcuts.html";

def switch_screens(target_screen):
    '''Send the current group to the other screen.'''
    @lazy.function
    def _inner(qtile):
        current_group = qtile.screens[1 - target_screen].group
        qtile.screens[target_screen].setGroup(current_group)

    return _inner


def focus_or_switch(group_name):
    '''
    Focus the selected group on the current screen or switch to the other
    screen if the group is currently active there
    '''
    @lazy.function
    def _inner(qtile):
        # Check what groups are currently active
        groups = [s.group.name for s in qtile.screens]

        try:
            # Jump to that screen if we are active
            index = groups.index(group_name)
            qtile.toScreen(index)
        except ValueError:
            # We're not active so pull the group to the current screen
            qtile.currentScreen.setGroup(qtile.groupMap[group_name])

    return _inner

# qtile actually has an emacs style `EzKey` helper that makes specifying
# key bindings a lot nicer than the default.
keys = [EzKey(k[0], *k[1:]) for k in [
    # Navigation
    # Swtich focus between panes
    ("M-<Up>", lazy.layout.up()),
    ("M-<Down>", lazy.layout.down()),
    ("M-<Left>", lazy.layout.left()),
    ("M-<Right>", lazy.layout.right()),

    ("M-h", lazy.layout.left()),
    ("M-j", lazy.layout.down()),
    ("M-k", lazy.layout.up()),
    ("M-l", lazy.layout.right()),

    # Swap panes: target relative to active.
    ("M-S-<Up>", lazy.layout.shuffle_up(), lazy.layout.section_up()),
    ("M-S-<Down>", lazy.layout.shuffle_down(), lazy.layout.section_down()),
    ("M-S-<Left>", lazy.layout.shuffle_left(), lazy.layout.swap_left()),
    ("M-S-<Right>", lazy.layout.shuffle_right(), lazy.layout.swap_right()),

    ("M-S-h", lazy.layout.shuffle_left(), lazy.layout.swap_left()),
    ("M-S-j", lazy.layout.shuffle_down(), lazy.layout.section_down()),
    ("M-S-k", lazy.layout.shuffle_up(), lazy.layout.section_up()),
    ("M-S-l", lazy.layout.shuffle_right(), lazy.layout.swap_right()),

    # Grow/shrink the main the focused window
    ("M-C-<Up>", lazy.layout.grow_up()),
    ("M-C-<Down>", lazy.layout.grow_down()),
    ("M-C-<Left>", lazy.layout.grow_left(), lazy.layout.shrink()),
    ("M-C-<Right>", lazy.layout.grow_right(), lazy.layout.grow()),

    ("M-C-h", lazy.layout.grow_up()),
    ("M-C-j", lazy.layout.grow_down()),
    ("M-C-k", lazy.layout.grow_left()),
    ("M-C-l", lazy.layout.grow_right()),

    ("M-<bracketleft>", lazy.layout.decrease_nmaster()),
    ("M-<bracketright>", lazy.layout.increase_nmaster()),

    # TODO meta alt
    ##Switch focus between two screens
    ("M-A-<Left>", lazy.prev_screen()),
    #("M-<Down>", lazy.to_screen(1)),
    ("M-A-<Right>", lazy.next_screen()),
    ##Move the focused group to one of the screens and follow it
    #("M-S-<bracketleft>", switch_screens(0), lazy.to_screen(0)),
    #("M-S-<bracketright>", switch_screens(1), lazy.to_screen(1)),

    # Layouts
    ("M-<backslash>", lazy.next_layout()),
    ("M-S-<backslash>", lazy.prev_layout()),
    ("M-r", lazy.layout.rotate(), lazy.layout.flip(), lazy.layout.spaw_column_left(), lazy.layout.spaw_column_right()),
    #("M-S-r", lazy.layout.flip()),
    ("M-<space>", lazy.layout.toggle_split()),
    #("M-f", lazy.prev_layout()),
    #("M-f", lazy.prev_layout()),
    # Applications
    ("M-<Return>", lazy.spawn(terminal)),
    ("M-<grave>", lazy.spawn("rofi -show drun")),
    ("M-S-<grave>", lazy.spawn("rofi -show run")),
    ("M-<Tab>", lazy.spawn("rofi -show")),
    ("M-e", lazy.spawn("dolphin")),
    ("M-w", lazy.spawn(mybrowser)),
    ("<Print>", lazy.spawn("spectacle")),

    # Windows
    ("M-<Page_Down>", lazy.spawn("Qminimize -m")),
    ("M-S-<Page_Down>", lazy.spawn("Qminimize -u")),
    ("M-S-<Page_Up>", lazy.layout.maximize()),
    ("M-<Page_Up>", lazy.window.toggle_fullscreen()),
    ("M-f", lazy.window.toggle_floating()),
    ("M-q", lazy.window.kill()),
    ("M-A-r", lazy.reload_config()),
    ("M-A-C-r", lazy.restart()),
    # Shut down qtile.
    ("M-A-q", lazy.shutdown()),
    ("M-n", lazy.layout.normalize()),
    ("M-s", lazy.spawn("qutebrowser ~/.dotfiles/.shortcuts.html")),

    # Change the volume if your keyboard has special volume keys.
    ("<XF86AudioRaiseVolume>", lazy.spawn("amixer -c 0 -q set Master 3dB+")),
    ("<XF86AudioLowerVolume>", lazy.spawn("amixer -c 0 -q set Master 3dB-")),
    ("<XF86AudioMute>", lazy.spawn("amixer -c 0 -q set Master toggle")),
]]

groups = [
    Group("WWW"),
    Group("DEV"),
    Group("SYS"),
    Group("DOC"),
    Group("VBX"),
    Group("CHT"),
    Group("MUS"),
    Group("VID"),
    Group("GFX")]

# .: Jump between groups and also throw windows to groups :. #
for _ix, group in enumerate(groups[:9]):
    # Index from 1-0 instead of 0-9
    ix = 0 if _ix == 9 else _ix + 1

    keys.extend([EzKey(k[0], *k[1:]) for k in [
        # M-ix = switch to that group
        # ("M-%d" % ix, lazy.group[group.name].toscreen()),
        ("M-%d" % ix, focus_or_switch(group.name)),
        # M-S-ix = switch to & move focused window to that group
        ("M-S-%d" % ix, lazy.window.togroup(group.name)),
    ]])

# .: Use the mouse to drag floating layouts :. #
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

layout_theme = {
    "margin": 5,
    "border_width": 2,
    "border_focus": "#49579f",
    "border_normal": "#2d3542",
    "border_focus_stack": "#63d7b0",
    "border_normal_stack": "#4e8f87"
    }

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Tile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2, **layout_theme),
    # layout.Bsp(),
    #layout.Matrix(**layout_theme),
    # layout.RatioTile(),
    #layout.TreeTab(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Cascadia Mono PL",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

sep_def = {
    "linewidth": 1,
    "padding": 6
    }

def init_widgets():
    return [

        widget.Sep(**sep_def),
        widget.TextBox(
            text="•••",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(spawnshortcuts)}
            ),

        widget.Sep(**sep_def),
        widget.GroupBox(
            disable_drag = True,
            rounded = False,
            highlight_method = "block"
            ),

        widget.Sep(**sep_def),
        widget.WindowName(parse_text = lambda text: text.rsplit("— ", 1)[1]),

        widget.Sep(**sep_def),
        widget.CheckUpdates(
            distro = "Ubuntu",
            update_interval = 1800,
            display_format = "{updates}",
            no_update_string = "  0",
            fmt = "Upd: {}"
            ),

        widget.Sep(**sep_def),
        widget.Memory(
            format="{MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate -e btop')},
            fmt="Mem: {}"
            ),

        widget.Sep(**sep_def),
        widget.CPU(
            format="{load_percent}%",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate -e btop')},
            fmt="CPU: {}"
            ),

        widget.Sep(**sep_def),
        widget.Volume(
            step = 5,
            fmt = "Vol: {}"
            ),

        widget.Sep(**sep_def),
        widget.Clock(format="Time: %H:%M:%S"),

        widget.Sep(**sep_def),
        widget.Systray(),
        #widget.CurrentLayout(),

        widget.Sep(**sep_def),
        ]

def get_widgets_notray():
    wid = init_widgets()
    del wid[16:18]
    return wid

# should be:
# | *** | DEV | Window Name                       Upd:  45 | Mem:  53% | CPU:   3% | Doom | Up | Time | V |
screens = [
    Screen( top=bar.Bar(widgets=get_widgets_notray(), size=20) ),
    Screen( top=bar.Bar(widgets=init_widgets(), size=20) ),
    Screen( top=bar.Bar(widgets=get_widgets_notray(), size=20) ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def start_once():
    subprocess.call([home + '/.config/qtile/autostart.sh'])

