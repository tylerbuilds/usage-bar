UsageBar v0.0.2 - Static Linux Binary

This binary has NO Swift runtime dependencies and works on any Linux distro.

Installation:
1. Copy the 'usagebar' binary to your PATH:
   sudo cp usagebar /usr/local/bin/usagebar

2. Install Python dependencies:
   sudo apt install python3-gi gir1.2-appindicator3-0.1 libsqlite3-0

3. Install the tray application files:
   mkdir -p ~/.local/share/usagebar
   cp -r <path-to-tray-files> ~/.local/share/usagebar/

4. Run:
   usagebar --version

Copyright Tyler Casey 2026
MIT License
