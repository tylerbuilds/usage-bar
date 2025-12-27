#!/usr/bin/python3
"""
UsageBar System tray application fixed
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GLib
import subprocess
import json
import sys
import webbrowser
from datetime import datetime
import threading
import os

# Provider configuration
PROVIDER_CONFIG = {
    'codex': {'icon': '🤖', 'name': 'Codex', 'url': 'https://platform.openai.com/usage'},
    'claude': {'icon': '🧠', 'name': 'Claude', 'url': 'https://claude.ai'},
    'cursor': {'icon': '⚡', 'name': 'Cursor', 'url': 'https://cursor.com'},
    'gemini': {'icon': '💎', 'name': 'Gemini', 'url': 'https://aistudio.google.com'},
    'zai': {'icon': '⚡', 'name': 'Z.ai', 'url': 'https://z.ai'},
    'antigravity': {'icon': '🚀', 'name': 'Antigravity', 'url': 'https://antigravity.dev'},
    'factory': {'icon': '🏭', 'name': 'Factory', 'url': 'https://app.factory.ai'}
}

class UsageBarTray:
    def __init__(self):
        print("Tray app init start")
        self.indicator = AppIndicator3.Indicator.new(
            "usagebar-tray",
            "utilities-system-monitor",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_label("⏳", "")

        self.provider_data = []
        self.last_refresh = None
        self.is_refreshing = False
        self.refresh_interval = 300

        self.set_loading_menu()
        print("Initial menu set")

        # Start first refresh
        GLib.timeout_add(500, self.trigger_refresh)
        
        # Schedule auto-refresh
        GLib.timeout_add_seconds(self.refresh_interval, self.trigger_refresh_loop)
        print("Tray app init complete")

    def trigger_refresh_loop(self):
        self.trigger_refresh()
        return True

    def trigger_refresh(self):
        if self.is_refreshing:
            print("Refresh already in progress")
            return False
            
        print("Triggering background refresh")
        self.is_refreshing = True
        self.indicator.set_label("⏳", "")
        
        thread = threading.Thread(target=self.fetch_all_data_thread, daemon=True)
        thread.start()
        return False

    def fetch_all_data_thread(self):
        try:
            print("Background thread started")
            cmd = ["usagebar", "usage", "--provider", "all", "--format", "json"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            print(f"CLI finished (code {result.returncode})")
            
            data = None
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line.startswith('['):
                    try:
                        data = json.loads(line)
                        print(f"Parsed {len(data)} providers")
                        break
                    except:
                        continue
            
            if data:
                GLib.idle_add(self.on_data_ready, data)
            else:
                print("No data found in CLI output")
                GLib.idle_add(self.on_error, "No data from CLI")
                
        except Exception as e:
            print(f"Thread error: {e}")
            GLib.idle_add(self.on_error, str(e))
        finally:
            self.is_refreshing = False

    def on_data_ready(self, data):
        print("Main thread received data")
        self.provider_data = data
        self.last_refresh = datetime.now()
        self.build_full_menu()
        print("Menu updated")
        return False

    def on_error(self, msg):
        print(f"Main thread received error: {msg}")
        self.build_error_menu(msg)
        return False

    def set_loading_menu(self):
        menu = Gtk.Menu()
        item = Gtk.MenuItem(label="⏳ Loading providers...")
        item.set_sensitive(False)
        menu.append(item)
        menu.append(Gtk.SeparatorMenuItem())
        refresh = Gtk.MenuItem(label="🔄 Refresh Now")
        refresh.connect("activate", lambda w: self.trigger_refresh())
        menu.append(refresh)
        menu.append(Gtk.SeparatorMenuItem())
        quit_item = Gtk.MenuItem(label="❌ Quit")
        quit_item.connect("activate", lambda w: Gtk.main_quit())
        menu.append(quit_item)
        menu.show_all()
        self.indicator.set_menu(menu)

    def make_progress_bar(self, percent_remaining):
        width = 10
        if percent_remaining >= 50:
            color, fill = '🟢', '█'
        elif percent_remaining >= 20:
            color, fill = '🟡', '▓'
        else:
            color, fill = '🔴', '░'
        filled = int((percent_remaining / 100) * width)
        bar = fill * filled + '░' * (width - filled)
        return f"{color} [{bar}] {percent_remaining:.0f}%"

    def get_status_color(self, percent):
        return '🟢' if percent >= 50 else '🟡' if percent >= 20 else '🔴'

    def build_error_menu(self, error_msg):
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
        print("Starting menu rebuild")
        menu = Gtk.Menu()
        lowest = 100
        critical_id = None

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

            if p_rem < lowest:
                lowest = p_rem
                critical_id = p_id

            header = f"{config['icon']} {config['name']} {self.get_status_color(p_rem)} {p_rem:.0f}%"
            sub = Gtk.Menu()
            item = Gtk.MenuItem(label=header)
            item.set_submenu(sub)
            menu.append(item)

            if usage.get('accountEmail'):
                mi = Gtk.MenuItem(label=f"📧 {usage.get('accountEmail')}")
                mi.set_sensitive(False)
                sub.append(mi)
                sub.append(Gtk.SeparatorMenuItem())

            # Session
            bar = self.make_progress_bar(p_rem)
            mi = Gtk.MenuItem(label=f"Session: {bar}")
            mi.set_sensitive(False)
            sub.append(mi)
            if primary.get('resetDescription'):
                ri = Gtk.MenuItem(label=f"    ⏰ {primary.get('resetDescription')}")
                ri.set_sensitive(False)
                sub.append(ri)

            # Weekly
            sec = usage.get('secondary')
            if sec:
                sec_rem = 100 - sec.get('usedPercent', 0)
                mi = Gtk.MenuItem(label=f"Weekly:  {self.make_progress_bar(sec_rem)}")
                mi.set_sensitive(False)
                sub.append(mi)
                if sec.get('resetDescription'):
                    ri = Gtk.MenuItem(label=f"    ⏰ {sec.get('resetDescription')}")
                    ri.set_sensitive(False)
                    sub.append(ri)

            # Sonnet/Tertiary
            tert = usage.get('tertiary')
            if tert:
                tert_rem = 100 - tert.get('usedPercent', 0)
                label = "Sonnet:" if p_id == 'claude' else "Other:"
                mi = Gtk.MenuItem(label=f"{label}   {self.make_progress_bar(tert_rem)}")
                mi.set_sensitive(False)
                sub.append(mi)

            # Credits
            creds = p_data.get('credits', {})
            if creds and creds.get('remaining') is not None:
                mi = Gtk.MenuItem(label=f"💰 ${creds.get('remaining'):.2f} left")
                mi.set_sensitive(False)
                sub.append(mi)

            if config['url']:
                sub.append(Gtk.SeparatorMenuItem())
                oi = Gtk.MenuItem(label=f"🌐 Open Dashboard")
                u = config['url']
                oi.connect("activate", lambda w, url=u: webbrowser.open(url))
                sub.append(oi)

        menu.append(Gtk.SeparatorMenuItem())
        if self.last_refresh:
            mi = Gtk.MenuItem(label=f"🕐 {self.last_refresh.strftime('%H:%M:%S')}")
            mi.set_sensitive(False)
            menu.append(mi)

        refresh = Gtk.MenuItem(label="🔄 Refresh Now")
        refresh.connect("activate", lambda w: self.trigger_refresh())
        menu.append(refresh)

        menu.append(Gtk.SeparatorMenuItem())
        quit_item = Gtk.MenuItem(label="❌ Quit")
        quit_item.connect("activate", lambda w: Gtk.main_quit())
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

        if critical_id:
            status = self.get_status_color(lowest)
            self.indicator.set_label(f"{status} {lowest:.0f}%", "")
        else:
            self.indicator.set_label("✅", "")
        print("Menu rebuild complete")

def main():
    print("Main start")
    app = UsageBarTray()
    Gtk.main()

if __name__ == "__main__":
    main()
