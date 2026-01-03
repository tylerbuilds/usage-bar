#!/bin/bash
# Force X11 backend for Wayland compatibility
export GDK_BACKEND=x11
exec /usr/bin/python3 /mnt/data/projects/UsageBar/usagebar-tray.py "$@"
