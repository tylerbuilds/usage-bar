#!/bin/bash
# UsageBar Release Script for Linux

echo "🚀 Preparing UsageBar Release..."

# 1. Clean and Build CLI
echo "📦 Building Swift CLI..."
swift build -c release --product CodexBarCLI

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

CLI_BIN=".build/release/CodexBarCLI"

# 2. Package assets
echo "📁 Packaging assets..."
mkdir -p dist

# Copy binaries and scripts
cp "$CLI_BIN" dist/usagebar
cp usagebar-tray.py dist/
cp usagebar-tray-launcher.sh dist/
cp usagebar-tray.desktop dist/
cp LICENSE dist/
cp README.md dist/
cp USER_GUIDE.md dist/

# 3. Create archive
VERSION=$(cat version.env | cut -d'=' -f2)
ARCHIVE="usagebar-linux-v${VERSION}.tar.gz"
tar -czf "$ARCHIVE" -C dist .

echo "✅ Release prepared: $ARCHIVE"
echo "Done!"
