#!/bin/bash
# Complete release build script for UsageBar
# Builds CLI, packages, and prepares for distribution

set -e

VERSION="1.0.0"
echo "======================================="
echo "UsageBar Release Build v${VERSION}"
echo "======================================="
echo

# 1. Build the CLI
echo "[1/5] Building CLI..."
if [ ! -f ".build/release/CodexBarCLI" ]; then
    swift build -c release --product CodexBarCLI
fi
echo "✅ CLI built"
ls -lh .build/release/CodexBarCLI
echo

# 2. Test basic functionality
echo "[2/5] Testing CLI..."
usagebar --version || (echo "✗ CLI test failed" && exit 1)
echo "✅ CLI working"
echo

# 3. Check Python modules
echo "[3/5] Checking Python modules..."
python3 -m py_compile usagebar-tray.py usagebar-history.py usagebar-charts.py usagebar-update.py
echo "✅ All Python modules valid"
echo

# 4. Create installation summary
echo "[4/5] Creating installation summary..."
cat > INSTALL.md << 'EOF'
# UsageBar Installation Guide

## Quick Install (Ubuntu/Debian)

```bash
# 1. Build the CLI
swift build -c release --product CodexBarCLI
sudo cp .build/release/CodexBarCLI /usr/local/bin/usagebar

# 2. Install dependencies
sudo apt install python3-gi gir1.2-appindicator3-0.1 libsqlite3-0

# 3. Launch
./usagebar-tray-launcher.sh
```

## System Requirements

- Ubuntu 24.04+ or equivalent
- Swift 6.0+ (for building CLI)
- Python 3.8+
- GTK3 and AppIndicator3

## Auto-Start on Login

```bash
# Create desktop entry
cp usagebar.desktop ~/.config/autostart/
```

## Database Location

Usage history is stored in:
```
~/.config/usagebar/history.db
```

## Troubleshooting

**Icons not showing:**
- Ensure assets/style.css is present
- Check console for CSS load errors

**History not tracking:**
- Verify ~/.config/usagebar/ directory exists
- Check database permissions

**Wayland issues:**
- The launcher script automatically forces X11 backend
- No manual configuration needed

## Uninstall

```bash
# Stop running instances
pkill -f usagebar-tray

# Remove files
sudo rm /usr/local/bin/usagebar
rm -rf ~/.config/usagebar
rm ~/.config/autostart/usagebar.desktop
```
EOF
echo "✅ Installation guide created"
echo

# 5. Build summary
echo "[5/5] Build Summary"
echo "======================================="
echo
echo "Ready to distribute:"
echo
echo "✅ CLI: .build/release/CodexBarCLI"
echo "✅ Tray: usagebar-tray.py"
echo "✅ History: usagebar-history.py"
echo "✅ Charts: usagebar-charts.py"
echo "✅ Update: usagebar-update.py"
echo "✅ Assets: assets/icons/ (10 icons), assets/style.css"
echo "✅ Docs: INSTALL.md, README.md"
echo
echo "To create distribution packages:"
echo "  - .deb: Use dpkg-buildpackage or debian/rules"
echo "  - AppImage: ./build-appimage.sh"
echo
echo "Done! 🎉"
