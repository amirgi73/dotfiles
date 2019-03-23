# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
from json import loads as json_loads
from libqtile import hook
import subprocess
import os


@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([script])


try:
    from typing import List  # noqa: F401
except ImportError:
    pass

try:
    wal_colors_file = os.path.expanduser("~/.cache/wal/colors.json")
    with open(wal_colors_file, 'r') as f:
        wal_colors = json_loads(f.read())
except FileNotFoundError:
    bg_color = "000000"
    fg_color = "ffffff"
    cursor_color = "ffffff"
    bold_color = "ffffff"
else:
    bg_color = wal_colors.get("special").get("background")[1:]
    fg_color = wal_colors.get("special").get("foreground")[1:]
    cursor_color = wal_colors.get("special").get("cursor")[1:]
    bold_color = wal_colors.get("colors").get("color6")[1:]


mod = "mod4"

keys = [
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -c 0 -q set Master toggle")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86MonBrightnessUp", lazy.spwan("xbacklight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),
    Key([mod], 'f', lazy.window.toggle_fullscreen()),
    #Key(['mod1', 'shift'], "Farsi_1", lazy.spawn("terminator")),
    # Switch between windows in current stack pane
    # Key([mod], "k", lazy.layout.down()),
    # Key([mod], "j", lazy.layout.up()),
    # Key(["mod1", "shift"], '1', lazy.spawn("setxbmap us")),
    # Key(["mod1", "shift"], '2', lazy.spawn("setxkbmap de")),
    # Key(["mod1", "shift"], "3", lazy.spawn("setxbmap ir")),
    # Key([mod], 'space', widget.KeyboardLayout(configured_keyboards=['us', 'ir']).next_keyboard()),

    # Move windows up or down in current stack
    # Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    # Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    # Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    # Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    # Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("terminator")),
    Key([mod], "c", lazy.spawn("terminator -x source ~/.bashrc && ranger")),
    Key(["mod1"], "space", lazy.spawn("rofi -show drun")),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "space", lazy.spawn(f"python {os.path.expanduser('~/.config/qtile/KbLayout.py')}")),
]

groups = [Group(i) for i in "12345678"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    #layout.Max(),
    #layout.Stack(num_stacks=2)
    layout.Bsp(margin=4),
    # layout.Zoomy()
]

def get_ip_location(data):
    return f"{data.get('query', '')} -> {data.get('country', '')}"


widget_defaults = dict(
    font='Iosevka Nerd Font Complete',
    fontsize=14,
    padding=10,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(padding=3,
                                this_current_screen_border=bold_color,
                                foreground=fg_color),
                widget.Prompt(foreground=fg_color),
                widget.Spacer(),
                widget.Mpris2(objname="org.mpris.MediaPlayer2.spotify",
                              name="spotify",
                              foreground=fg_color),
                # widget.Notify(default_timeout=10, foreground=fg_color),
                widget.Sep(),
                widget.CheckUpdates(display_format="{updates} Pkg Updates",
                                    colour_no_updates=fg_color,
                                    colour_have_updates=bold_color,
                                    distro='Arch',
                                    execute=lazy.spawn("tkpacman"),
                                    foreground=fg_color),
                widget.Sep(),
                widget.ThermalSensor(tag_sensor="Core 0",
                                     foreground=fg_color),
                widget.Sep(),
                widget.GenPollUrl(url="http://ip-api.com/json/",
                                  parse=get_ip_location,
                                  foreground=fg_color),
                # widget.KeyboardKbdd(configured_keyboards=['us', 'ir']),
                widget.Sep(),
                # widget.Wlan(interface="wlp3s0", format="{essid} {percent:2.0%}", foreground=fg_color),
                # widget.NetGraph(interface="wlp3s0", foreground=fg_color),
                widget.TextBox(text="/dev/sda:",
                               foreground=fg_color),
                widget.HDDBusyGraph(fill_color=cursor_color,
                                    graph_color=bold_color,
                                    border_color=bg_color,
                                    foreground=fg_color),
                widget.Sep(),
                widget.KeyboardLayout(configured_keyboards=['us', 'ir'],
                                      foreground=fg_color),
                widget.Sep(),
                widget.Backlight(backlight_name="intel_backlight",
                                 format="☼ {percent: 2.0%}",
                                 foreground=fg_color),
                widget.Volume(emoji=True,
                              foreground=fg_color),
                # widget.Battery(foreground=fg_color, charge_char=u'▲', discharge_char=u'▼', low_foreground=bold_color),
                # widget.BatteryIcon(),
                widget.Sep(),
                widget.Systray(icon_size=22,
                               padding=7,
                               foreground=fg_color),
                widget.Sep(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p',
                             foreground=fg_color),
            ],
            24,
            background=bg_color,
            opacity=20,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wname': 'tkPacman'},
])
auto_fullscreen = False
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
