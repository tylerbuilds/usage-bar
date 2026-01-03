#!/bin/bash
# Build UsageBar AppImage for distribution across Linux distributions

set -e

echo "Building UsageBar AppImage..."

VERSION="1.0.0"
APPDIR="UsageBar.AppDir"
OUTPUT="UsageBar-${VERSION}-x86_64.AppImage"

# Clean previous builds
rm -rf "$APPDIR" "$OUTPUT"

# Create AppDir structure
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/lib/usagebar/assets"
mkdir -p "$APPDIR/usr/lib/usagebar/assets/icons"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/512x512/apps"

# Build the CLI if not already built
if [ ! -f ".build/release/CodexBarCLI" ]; then
    echo "Building CLI..."
    swift build -c release --product CodexBarCLI
fi

# Copy binaries
echo "Copying binaries..."
install -m 755 .build/release/CodexBarCLI "$APPDIR/usr/bin/usagebar"
install -m 755 usagebar-tray.py "$APPDIR/usr/lib/usagebar/usagebar-tray.py"
install -m 755 usagebar-history.py "$APPDIR/usr/lib/usagebar/usagebar-history.py"
install -m 755 usagebar-charts.py "$APPDIR/usr/lib/usagebar/usagebar-charts.py"

# Create launcher script
cat > "$APPDIR/usr/bin/usagebar-tray" << 'LAUNCHEREOF'
#!/bin/bash
# UsageBar launcher for AppImage
export GDK_BACKEND=x11
export PYTHONPATH="${APPDIR}/usr/lib/usagebar:${PYTHONPATH}"
python3 "${APPDIR}/usr/lib/usagebar/usagebar-tray.py" "$@"
LAUNCHEREOF
chmod +x "$APPDIR/usr/bin/usagebar-tray"

# Copy assets
echo "Copying assets..."
install -m 644 assets/style.css "$APPDIR/usr/lib/usagebar/assets/"
install -m 644 assets/icons/*.svg "$APPDIR/usr/lib/usagebar/assets/icons/"

# Copy desktop file
cp usagebar.desktop "$APPDIR/usr/share/applications/"

# Copy icon
cp assets/icons/usagebar-icon.svg "$APPDIR/usr/share/icons/hicolor/512x512/apps/usagebar.svg"

# Create AppRun
cat > "$APPDIR/AppRun" << 'APPRUNEOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PYTHONPATH="${HERE}/usr/lib/usagebar:${PYTHONPATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/usagebar-tray" "$@"
APPRUNEOF
chmod +x "$APPDIR/AppRun"

# Download appimage-builder if not present
if [ ! -f "appimage-builder-x86_64.AppImage" ]; then
    echo "Downloading appimage-builder..."
    wget -c "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimage-builder-x86_64.AppImage"
    chmod +x appimage-builder-x86_64.AppImage
fi

# Build AppImage
echo "Building AppImage..."
./appimage-builder-x86_64.AppImage --appdir "$APPDIR" --output "$OUTPUT"

echo "✅ Built: $OUTPUT"
ls -lh "$OUTPUT"
