
import os
import subprocess
import datetime

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, EzKey
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from uptime import uptime


mod = "mod4"
mybrowser = "min"
altbrowser = "google-chrome"
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

@lazy.function
def increase_vol(qtile):
    widget_volume.cmd_increase_vol()

@lazy.function
def decrease_vol(qtile):
    widget_volume.cmd_decrease_vol()

@lazy.function
def mute_vol(qtile):
    widget_volume.cmd_mute()

# qtile actually has an emacs style `EzKey` helper that makes specifying
# key bindings a lot nicer than the default.
#
# Keys follow some "logic"
# meta - movement, change layout and app spawn
# meta + shift - move windows and alt versions of meta keys
# meta + alt - group movement
# meta + ctrl - change window size
# meta + ctrl + alt - qtile extremes so no accidents
#
keys = [EzKey(k[0], *k[1:]) for k in [
    # Navigation
    # Swtich focus between panes
    ("M-<Left>", lazy.layout.left()),
    ("M-<Down>", lazy.layout.down()),
    ("M-<Up>", lazy.layout.up()),
    ("M-<Right>", lazy.layout.right()),

    ("M-h", lazy.layout.left()),
    ("M-j", lazy.layout.down()),
    ("M-k", lazy.layout.up()),
    ("M-l", lazy.layout.right()),

    # Swap panes: target relative to active.
    ("M-S-<Left>", lazy.layout.shuffle_left(), lazy.layout.swap_left()),
    ("M-S-<Down>", lazy.layout.shuffle_down(), lazy.layout.section_down()),
    ("M-S-<Up>", lazy.layout.shuffle_up(), lazy.layout.section_up()),
    ("M-S-<Right>", lazy.layout.shuffle_right(), lazy.layout.swap_right()),

    ("M-S-h", lazy.layout.shuffle_left(), lazy.layout.swap_left()),
    ("M-S-j", lazy.layout.shuffle_down(), lazy.layout.section_down()),
    ("M-S-k", lazy.layout.shuffle_up(), lazy.layout.section_up()),
    ("M-S-l", lazy.layout.shuffle_right(), lazy.layout.swap_right()),

    # Grow/shrink the main the focused window
    ("M-C-<Left>", lazy.layout.grow_left(), lazy.layout.shrink()),
    ("M-C-<Down>", lazy.layout.grow_down()),
    ("M-C-<Up>", lazy.layout.grow_up()),
    ("M-C-<Right>", lazy.layout.grow_right(), lazy.layout.grow()),

    ("M-C-h", lazy.layout.grow_left(), lazy.layout.shrink()),
    ("M-C-j", lazy.layout.grow_down()),
    ("M-C-k", lazy.layout.grow_up()),
    ("M-C-l", lazy.layout.grow_right(), lazy.layout.grow()),

    ("M-<bracketleft>", lazy.layout.decrease_nmaster()),
    ("M-<bracketright>", lazy.layout.increase_nmaster()),

    # TODO meta alt
    ##Switch focus between two screens
    ("M-A-h", lazy.screen.prev_group()),
    ("M-A-l", lazy.screen.next_group()),
    ("M-A-<Left>", lazy.screen.prev_group()),
    ("M-A-<Right>", lazy.screen.next_group()),
    #("M-A-<Left>", lazy.to_screen(1)),
    ("M-A-<Down>", lazy.prev_screen()),
    ("M-A-<Up>", lazy.next_screen()),
    ("M-A-j", lazy.prev_screen()),
    ("M-A-k", lazy.next_screen()),
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
    ("M-S-w", lazy.spawn(altbrowser)),
    ("<Print>", lazy.spawn("spectacle")),

    # Windows
    ("M-f", lazy.window.toggle_floating()),
    ("M-q", lazy.window.kill()),
    ("M-A-r", lazy.reload_config()),
    ("M-A-C-r", lazy.restart()),
    ("M-A-C-q", lazy.shutdown()),
    ("M-<Page_Down>", lazy.spawn("Qminimize -m")),
    ("M-S-<Page_Down>", lazy.spawn("Qminimize -u")),
    ("M-<Page_Up>", lazy.window.toggle_fullscreen()),
    ("M-S-<Page_Up>", lazy.layout.maximize()),
    # Shut down qtile.
    ("M-n", lazy.layout.normalize()),
    ("M-s", lazy.spawn("qutebrowser ~/.dotfiles/.shortcuts.html")),

    # Change the volume if your keyboard has special volume keys.
    ("<XF86AudioRaiseVolume>", increase_vol),
    ("<XF86AudioLowerVolume>", decrease_vol),
    ("<XF86AudioMute>", mute_vol),
]]

icons = {
    "group_www": "󰖟", # mdi-web
    "group_sys": "󰞷", # mdi-console-line
    "group_dev": "󰗀", # mdi-xml
    "group_doc": "󰧮", # mdi-file-document-outline
    "group_vbx": "󰍹", # mdi-monitor
    "group_cht": "󰍪", # mdi-message-text-outline
    "group_mus": "󰲸", # mdi-playlist-music
    "group_vid": "󰯜", # mdi-video-outline
    "group_gfx": "󰌨", # mdi-layers

    "update": "󰑓", # mdi-reload
    "disk": "󰉉", # mdi-floppy
    "ram": "󰓡", # mdi-swap-horizontal
    "cpu": "󰍛", # mdi-memory
    "volume": "󰕾", # mdi-volume-high
    "uptime": "󱕌", # mdi-sort-clock-descending-outline
    "doomsday": "󰯈", # mdi-skull-outline
    "calendar": "󰸗", # mdi-calendar-month
    "clock": "󱑏", # mdi-clock-time-five-outline

    "screen_focus": "󰍹", # mdi-monitor
    "screen_nofocus": "󰶐", # mdi-monitor-off
    }

groups = [
    Group("WWW", label = icons["group_www"]),
    Group("SYS", label = icons["group_sys"]),
    Group("DEV", label = icons["group_dev"]),
    Group("DOC", label = icons["group_doc"]),
    Group("VBX", label = icons["group_vbx"]),
    Group("CHT", label = icons["group_cht"]),
    Group("MUS", label = icons["group_mus"]),
    Group("VID", label = icons["group_vid"]),
    Group("GFX", label = icons["group_gfx"])]

# .: Jump between groups and also throw windows to groups :. #
for _ix, group in enumerate(groups[:9]):
    # Index from 1-0 instead of 0-9
    ix = 0 if _ix == 9 else _ix + 1

    keys.extend([EzKey(k[0], *k[1:]) for k in [
        # M-ix = switch to that group
        ("M-%d" % ix, lazy.group[group.name].toscreen()),
        #("M-%d" % ix, focus_or_switch(group.name)),
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

def get_uptime():
    seconds = uptime()
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{:.0f}:{:.0f}".format(h, m)

def get_doomsday():
    return subprocess.run([home + "/.dotfiles/doomsday-clock", "-c"], capture_output = True, text = True).stdout[:-1]

layout_theme = {
    "margin": 5,
    "border_width": 2,
    "border_focus": "#c58265",
    "border_normal": "#2d3542",
    "border_focus_stack": "#c89265",
    "border_normal_stack": "#7d634c"
    }

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Tile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Floating(**layout_theme),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2, **layout_theme),
    # layout.Bsp(),
    #layout.Matrix(**layout_theme),
    # layout.RatioTile(),
    #layout.TreeTab(),
    # layout.Zoomy(),
]

bar_opacity = "bb";
bar_color = "#202020" + bar_opacity;
icon_font = "Material Design Icons"

colors = {
    "main": "#e27100",
    "accent": "#d8ceb8",
    "off": "#606060",
    }

widget_defaults = {
    "font": "Cascadia Mono PL",
    "fontsize": 13,
    "padding": 3,
    "foreground": colors["accent"]
}

sep_def = {
    "linewidth": 1,
    "padding": 6
    }

spacer_def = {
    "length": 12
    }

fa_def = {
    "foreground": colors["main"],
    "padding": 0,
    "font": icon_font,
    "fontsize": 24,
    }

widget_volume = widget.PulseVolume(
    step = 5,
    fmt = "{}",
    **widget_defaults
    )

def init_widgets():
    return [
        widget.GroupBox(
            disable_drag = True,
            rounded = False,
            highlight_method = "block",
            active = colors["main"],
            inactive = colors["off"],
            this_current_screen_border = "#404040" + bar_opacity,
            other_current_screen_border = "#202020" + "22",
            this_screen_border = "#404040" + bar_opacity,
            other_screen_border = "#202020" + "22",
            **fa_def
            ),

        widget.WindowName(
            **widget_defaults,
            parse_text = lambda text: text.rsplit("— ", 1)[1]
            ),

        widget.TextBox( **fa_def, text = icons["update"] ),
        widget.CheckUpdates(
            **widget_defaults,
            distro = "Ubuntu",
            update_interval = 1800,
            display_format = "{updates}",
            no_update_string = "  0",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate --hold -e apt list --upgradable')},
            colour_have_updates = colors["accent"],
            colour_no_updates = colors["off"],
            ),

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["disk"] ),
        widget.DF(
            **widget_defaults,
            format="{r:2.0f}%",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate -e btop')},
            visible_on_warn = False
            ),

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["ram"] ),
        widget.Memory(
            format="{MemPercent:2.0f}%",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate -e btop')},
            ),

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["cpu"] ),
        widget.CPU(
            **widget_defaults,
            format="{load_percent:2.0f}%",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate -e btop')},
            ),

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["volume"] ),
        widget_volume,

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["uptime"] ),
        widget.GenPollText(
            **widget_defaults,
            func = get_uptime,
            update_interval = 60
            ),

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["doomsday"] ),
        widget.GenPollText(
            **widget_defaults,
            func = get_doomsday,
            update_interval = 60 * 60 * 6
            ),

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["calendar"] ),
        widget.Clock(
            **widget_defaults,
            format="%d/%m",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate --hold -e ncal -yMb')},
            ),

        widget.Spacer(**spacer_def),
        widget.TextBox( **fa_def, text = icons["clock"] ),
        widget.Clock(
            **widget_defaults,
            format="%H:%M:%S",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' --separate --hold -e ncal -yMb')},
            ),

        widget.Spacer(**spacer_def),
        widget.CurrentScreen(
            **fa_def,
            active_text = icons["screen_focus"],
            inactive_text = icons["screen_nofocus"],
            active_color = colors["main"],
            inactive_color = colors["off"],
            ),
        widget.Spacer(**spacer_def),
        ]


# should be:
# | *** | DEV | Window Name                       Upd:  45 | Mem:  53% | CPU:   3% | Doom | Up | Time | V |
screens = [
    Screen( top = bar.Bar(widgets = init_widgets(), size = 24, background = bar_color) ),
    Screen( top = bar.Bar(widgets = init_widgets(), size = 24, background = bar_color) ),
    Screen( top = bar.Bar(widgets = init_widgets(), size = 24, background = bar_color) ),
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

@hook.subscribe.startup
def set_screen_groups():
    # left center right = 2 0 1
    screens[2].set_group(groups[0], warp = False)
    screens[0].set_group(groups[1], warp = False)
    screens[1].set_group(groups[2], warp = False)

@hook.subscribe.startup_once
def start_once():
    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.client_new
def func(c):
    if c.name == "Desktop — Plasma":
        c.cmd_kill()
