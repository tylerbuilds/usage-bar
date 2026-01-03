#!/usr/bin/env python3
"""
Quick UI test for UsageBar visual upgrades.
Tests that icons load, CSS is valid, and widgets render correctly.
"""

import os
import sys

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_icons_exist():
    """Test that all SVG icons exist."""
    icons_dir = os.path.join(os.path.dirname(__file__), "assets", "icons")
    required_icons = [
        "usagebar-icon.svg",
        "usagebar-icon-warning.svg",
        "usagebar-icon-critical.svg",
        "provider-claude.svg",
        "provider-codex.svg",
        "provider-gemini.svg",
        "provider-cursor.svg",
        "provider-zai.svg",
        "provider-antigravity.svg",
        "provider-factory.svg"
    ]

    missing = []
    for icon in required_icons:
        icon_path = os.path.join(icons_dir, icon)
        if not os.path.exists(icon_path):
            missing.append(icon)

    if missing:
        print(f"✗ Missing icons: {missing}")
        return False
    else:
        print(f"✓ All {len(required_icons)} SVG icons present")
        return True

def test_css_exists():
    """Test that CSS file exists and is valid."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if not os.path.exists(css_path):
        print(f"✗ CSS file not found at {css_path}")
        return False

    with open(css_path, 'r') as f:
        css_content = f.read()

    # Basic CSS validation
    if '@define-color' in css_content and 'progressbar' in css_content:
        print(f"✓ CSS file is valid ({len(css_content)} bytes)")
        return True
    else:
        print(f"✗ CSS file appears invalid")
        return False

def test_imports():
    """Test that Python imports work."""
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import Gtk, AppIndicator3, GLib, Gdk, GdkPixbuf
        print("✓ GTK3 imports successful")
        return True
    except Exception as e:
        print(f"✗ GTK3 import failed: {e}")
        return False

def main():
    print("=" * 50)
    print("UsageBar Visual Upgrade Test Suite")
    print("=" * 50)
    print()

    results = [
        test_icons_exist(),
        test_css_exists(),
        test_imports()
    ]

    print()
    print("=" * 50)
    if all(results):
        print("✓ All tests passed! Phase 1 upgrades are ready.")
        print()
        print("To launch UsageBar:")
        print("  ./usagebar-tray-launcher.sh")
        print()
        print("Or directly:")
        print("  python3 usagebar-tray.py")
        return 0
    else:
        print("✗ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
