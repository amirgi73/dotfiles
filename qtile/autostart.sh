#!/bin/bash
wal -R
nm-applet &
xfce4-power-manager
compton -b
#setxkbmap -layout us,ir -option grp:alt_shift_toggle
