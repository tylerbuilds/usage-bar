#!/usr/bin/python3
"""
UsageBar: A premium AI usage tracker for Linux system trays.
Inspired by CodexBar.app (macOS).

This script provides a GTK3-based system tray icon with an expandable menu
to monitor usage limits across various AI providers.
"""

import gi

# Ensure we have the correct GTK and AppIndicator versions
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
except ValueError as e:
    print(f"Error: Missing system dependencies. {e}")
    print("Please install libappindicator3-1 and python3-gi.")
    sys.exit(1)

from gi.repository import Gtk, AppIndicator3, GLib
import subprocess
import json
import sys
import webbrowser
from datetime import datetime
import threading
import os

# --- Configuration & Constants ---

# Application directory for settings
CONFIG_DIR = os.path.expanduser("~/.config/usagebar")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

# Provider display configuration
# Icons and Dashboard URLs
PROVIDER_CONFIG = {
    'codex': {'icon': '🤖', 'name': 'Codex', 'url': 'https://platform.openai.com/usage'},
    'claude': {'icon': '🧠', 'name': 'Claude', 'url': 'https://claude.ai'},
    'cursor': {'icon': '⚡', 'name': 'Cursor', 'url': 'https://cursor.com'},
    'gemini': {'icon': '💎', 'name': 'Gemini', 'url': 'https://aistudio.google.com'},
    'zai': {'icon': '⚡', 'name': 'Z.ai', 'url': 'https://z.ai'},
    'antigravity': {'icon': '🚀', 'name': 'Antigravity', 'url': 'https://antigravity.dev'},
    'factory': {'icon': '🏭', 'name': 'Factory', 'url': 'https://app.factory.ai'}
}

# providers that are considered "critical" for the tray icon label
PRIMARY_PROVIDERS = ['codex', 'claude', 'gemini', 'zai']

class UsageBarTray:
    """The main application class for the UsageBar system tray."""

    def __init__(self):
        print("[UsageBar] Initializing system tray application...")
        
        # Initialize the AppIndicator
        self.indicator = AppIndicator3.Indicator.new(
            "usagebar-tray",
            "utilities-system-monitor", # Standard system icon name
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_label("⏳", "")

        self.provider_data = []
        self.last_refresh = None
        self.is_refreshing = False
        
        # Load user settings or set defaults
        self.load_settings()

        # Set the initial menu state
        self.set_loading_menu()

        # Trigger the first data fetch
        GLib.timeout_add(500, self.trigger_refresh)
        
        # Schedule periodic background refreshes
        GLib.timeout_add_seconds(self.refresh_interval, self.trigger_refresh_loop)
        print("[UsageBar] Initialization complete.")

    def load_settings(self):
        """Load settings from the local config file."""
        self.refresh_interval = 300 # Default: 5 minutes
        self.show_details = False
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    s = json.load(f)
                    self.refresh_interval = s.get('refresh_interval', 300)
                    self.show_details = s.get('show_details', False)
        except Exception as e:
            print(f"[UsageBar] Warning: Failed to load settings: {e}")

    def save_settings(self):
        """Save current settings to the local config file."""
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(SETTINGS_FILE, 'w') as f:
                json.dump({
                    'refresh_interval': self.refresh_interval,
                    'show_details': self.show_details
                }, f)
        except Exception as e:
            print(f"[UsageBar] Error: Failed to save settings: {e}")

    def trigger_refresh_loop(self):
        """Callback for periodic status updates."""
        self.trigger_refresh()
        return True # Keep the timer running

    def trigger_refresh(self):
        """Asynchronously trigger a refresh of usage data."""
        if self.is_refreshing:
            return False
            
        self.is_refreshing = True
        # Set loading icon in tray
        if not self.last_refresh:
            self.indicator.set_label("⏳", "")
        
        # Run the CLI in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.fetch_all_data_thread, daemon=True)
        thread.start()
        return False

    def fetch_all_data_thread(self):
        """Background thread logic for calling the Swift CLI."""
        try:
            # Call the 'usagebar' CLI (must be in system PATH)
            cmd = ["usagebar", "usage", "--provider", "all", "--format", "json"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # Parse the JSON output from the CLI
            data = None
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line.startswith('['):
                    try:
                        data = json.loads(line)
                        break
                    except json.JSONDecodeError:
                        continue
            
            if data:
                # Update UI on the main GTK thread
                GLib.idle_add(self.on_data_ready, data)
            else:
                GLib.idle_add(self.on_error, "CLI returned no data")
                
        except Exception as e:
            print(f"[UsageBar] Data fetch error: {e}")
            GLib.idle_add(self.on_error, str(e))
        finally:
            self.is_refreshing = False

    def on_data_ready(self, data):
        """Main thread callback for successful data fetch."""
        self.provider_data = data
        self.last_refresh = datetime.now()
        self.build_full_menu()
        return False

    def on_error(self, msg):
        """Main thread callback for data fetch failures."""
        self.build_error_menu(msg)
        return False

    def set_loading_menu(self):
        """Build the initial 'Loading' menu."""
        menu = Gtk.Menu()
        item = Gtk.MenuItem(label="⏳ Loading providers...")
        item.set_sensitive(False)
        menu.append(item)
        menu.append(Gtk.SeparatorMenuItem())
        
        refresh = Gtk.MenuItem(label="🔄 Refresh Now")
        refresh.connect("activate", lambda w: self.trigger_refresh())
        menu.append(refresh)
        
        menu.append(Gtk.SeparatorMenuItem())
        quit_item = Gtk.MenuItem(label="❌ Quit UsageBar")
        quit_item.connect("activate", lambda w: Gtk.main_quit())
        menu.append(quit_item)
        
        menu.show_all()
        self.indicator.set_menu(menu)

    def make_progress_bar(self, percent_remaining):
        """Generate a visual Unicode progress bar based on percentage."""
        width = 10
        if percent_remaining >= 50:
            color, fill = '🟢', '█' # Healthy
        elif percent_remaining >= 20:
            color, fill = '🟡', '▓' # Warning
        else:
            color, fill = '🔴', '░' # Critical
            
        filled = int((percent_remaining / 100) * width)
        bar = fill * filled + '░' * (width - filled)
        return f"{color} [{bar}] {percent_remaining:.0f}%"

    def get_status_emoji(self, percent):
        """Get the status indicator emoji."""
        if percent >= 50: return '🟢'
        if percent >= 20: return '🟡'
        return '🔴'

    def build_error_menu(self, error_msg):
        """Build the menu for error states."""
        menu = Gtk.Menu()
        item = Gtk.MenuItem(label=f"⚠️ {error_msg}")
        item.set_sensitive(False)
        menu.append(item)
        
        menu.append(Gtk.SeparatorMenuItem())
        refresh = Gtk.MenuItem(label="🔄 Retry Now")
        refresh.connect("activate", lambda w: self.trigger_refresh())
        menu.append(refresh)
        
        menu.append(Gtk.SeparatorMenuItem())
        quit_item = Gtk.MenuItem(label="❌ Quit")
        quit_item.connect("activate", lambda w: Gtk.main_quit())
        menu.append(quit_item)
        
        menu.show_all()
        self.indicator.set_menu(menu)
        self.indicator.set_label("⚠️", "")

    def build_full_menu(self):
        """Build the rich, expandable main menu from provider data."""
        menu = Gtk.Menu()
        lowest_primary = 100
        critical_id = None

        # Sort providers by usage (highest used first)
        sorted_data = sorted(
            self.provider_data,
            key=lambda p: p.get('usage', {}).get('primary', {}).get('usedPercent', 0),
            reverse=True
        )

        for p_data in sorted_data:
            p_id = p_data.get('provider', '?').lower()
            usage = p_data.get('usage', {})
            if not usage: continue

            config = PROVIDER_CONFIG.get(p_id, {'icon': '📊', 'name': p_id.upper(), 'url': None})
            primary = usage.get('primary', {})
            p_rem = 100 - primary.get('usedPercent', 0)

            # Track health of primary providers for the tray hub label
            if p_id in PRIMARY_PROVIDERS and p_rem < lowest_primary:
                lowest_primary = p_rem
                critical_id = p_id

            # Main provider item with expandable submenu
            header_label = f"{config['icon']} {config['name']}  {self.get_status_emoji(p_rem)} {p_rem:.0f}%"
            provider_menu = Gtk.Menu()
            provider_root = Gtk.MenuItem(label=header_label)
            provider_root.set_submenu(provider_menu)
            menu.append(provider_root)

            # Account details
            if usage.get('accountEmail'):
                mi = Gtk.MenuItem(label=f"📧 {usage.get('accountEmail')}")
                mi.set_sensitive(False)
                provider_menu.append(mi)
                provider_menu.append(Gtk.SeparatorMenuItem())

            # Primary (Session) Usage
            bar = self.make_progress_bar(p_rem)
            mi = Gtk.MenuItem(label=f"Session: {bar}")
            mi.set_sensitive(False)
            provider_menu.append(mi)
            
            if primary.get('resetDescription'):
                # Detail Mode: show specific timestamp
                reset_text = f"⏰ {primary.get('resetDescription')}"
                if self.show_details and primary.get('resetsAt'):
                    reset_text += f" ({primary.get('resetsAt')})"
                ri = Gtk.MenuItem(label=f"    {reset_text}")
                ri.set_sensitive(False)
                provider_menu.append(ri)

            # Secondary (Weekly) Usage
            secondary = usage.get('secondary')
            if secondary:
                sec_rem = 100 - secondary.get('usedPercent', 0)
                mi = Gtk.MenuItem(label=f"Weekly:  {self.make_progress_bar(sec_rem)}")
                mi.set_sensitive(False)
                provider_menu.append(mi)
                if secondary.get('resetDescription'):
                    rm = Gtk.MenuItem(label=f"    ⏰ {secondary.get('resetDescription')}")
                    rm.set_sensitive(False)
                    provider_menu.append(rm)

            # Tertiary (Specific Model) Usage
            tertiary = usage.get('tertiary')
            if tertiary:
                tert_rem = 100 - tertiary.get('usedPercent', 0)
                label = "Sonnet:" if p_id == 'claude' else "Other:"
                mi = Gtk.MenuItem(label=f"{label}   {self.make_progress_bar(tert_rem)}")
                mi.set_sensitive(False)
                provider_menu.append(mi)

            # Credit Balance
            creds = p_data.get('credits', {})
            if creds and creds.get('remaining') is not None:
                mi = Gtk.MenuItem(label=f"💰 ${creds.get('remaining'):.2f} remaining")
                mi.set_sensitive(False)
                provider_menu.append(mi)

            # Technical details (Version, etc.)
            if self.show_details and p_data.get('version'):
                provider_menu.append(Gtk.SeparatorMenuItem())
                vi = Gtk.MenuItem(label=f"🏷 Version: {p_data.get('version')}")
                vi.set_sensitive(False)
                provider_menu.append(vi)

            # Dashboard Link
            if config.get('url'):
                provider_menu.append(Gtk.SeparatorMenuItem())
                oi = Gtk.MenuItem(label=f"🌐 Open {config['name']} Dashboard")
                dashboard_url = config['url']
                oi.connect("activate", lambda w, url=dashboard_url: webbrowser.open(url))
                provider_menu.append(oi)

        # Bottom Menu Section
        menu.append(Gtk.SeparatorMenuItem())
        
        if self.last_refresh:
            time_str = self.last_refresh.strftime('%H:%M:%S')
            mi = Gtk.MenuItem(label=f"🕐 Last updated: {time_str}")
            mi.set_sensitive(False)
            menu.append(mi)

        refresh = Gtk.MenuItem(label="🔄 Refresh Now")
        refresh.connect("activate", lambda w: self.trigger_refresh())
        menu.append(refresh)

        menu.append(Gtk.SeparatorMenuItem())
        
        # Settings Submenu
        settings_menu = Gtk.Menu()
        settings_root = Gtk.MenuItem(label="⚙️ Settings")
        settings_root.set_submenu(settings_menu)
        menu.append(settings_root)
        
        detail_item = Gtk.CheckMenuItem(label="Show Technical Details")
        detail_item.set_active(self.show_details)
        detail_item.connect("toggled", self.on_detail_toggled)
        settings_menu.append(detail_item)

        menu.append(Gtk.SeparatorMenuItem())
        
        quit_item = Gtk.MenuItem(label="❌ Quit UsageBar")
        quit_item.connect("activate", lambda w: Gtk.main_quit())
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

        # Update Hub Label: Show status icons or critical percentage
        if critical_id:
            status = self.get_status_emoji(lowest_primary)
            if status == '🟢':
                # Hub is healthy
                self.indicator.set_label("✅", "")
            else:
                # One or more primary providers are getting low
                self.indicator.set_label(f"{status} {lowest_primary:.0f}%", "")
        else:
            self.indicator.set_label("✅", "")

    def on_detail_toggled(self, widget):
        """Technical Detailed Mode toggle handler."""
        self.show_details = widget.get_active()
        self.save_settings()
        self.build_full_menu()

def main():
    """Application entry point."""
    app = UsageBarTray()
    try:
        Gtk.main()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
