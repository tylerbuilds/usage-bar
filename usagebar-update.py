#!/usr/bin/env python3
"""
UsageBar Auto-Update Checker

Checks for new releases on GitHub and notifies users.
"""

import urllib.request
import json
from typing import Optional, Dict

# Current version
CURRENT_VERSION = "0.0.2"
REPO_API = "https://api.github.com/repos/tylerisbuilding/UsageBar/releases/latest"
CACHE_FILE = "~/.config/usagebar/update_check.txt"


def check_for_updates() -> Optional[Dict]:
    """
    Check GitHub releases API for new version.

    Returns:
        Dict with update info if available, None if up-to-date
    """
    try:
        with urllib.request.urlopen(REPO_API, timeout=5) as response:
            release = json.loads(response.read().decode())

            latest_version = release['tag_name'].lstrip('v')

            # Simple version comparison
            if latest_version > CURRENT_VERSION:
                return {
                    'available': True,
                    'current_version': CURRENT_VERSION,
                    'latest_version': latest_version,
                    'url': release['html_url'],
                    'notes': release.get('body', '')[:200] + '...',
                    'published_at': release.get('published_at', '')
                }

            return {'available': False, 'current_version': CURRENT_VERSION, 'latest_version': latest_version}

    except Exception as e:
        print(f"[UsageBar] Update check failed: {e}")
        return None


def should_check_cache() -> bool:
    """
    Check if enough time has passed since last check (hourly).

    Returns:
        True if should check, False otherwise
    """
    import os
    from datetime import datetime, timedelta

    cache_path = os.path.expanduser(CACHE_FILE)

    if not os.path.exists(cache_path):
        return True

    try:
        with open(cache_path, 'r') as f:
            last_check = datetime.fromisoformat(f.read().strip())

        # Only check once per hour
        if datetime.now() - last_check > timedelta(hours=1):
            return True

        return False
    except:
        return True


def update_cache():
    """Update the cache file with current timestamp."""
    import os
    from datetime import datetime

    cache_path = os.path.expanduser(CACHE_FILE)
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    with open(cache_path, 'w') as f:
        f.write(datetime.now().isoformat())


def main():
    """CLI interface for update checking."""
    import sys

    print("UsageBar Update Checker")
    print(f"Current version: {CURRENT_VERSION}")
    print()

    update_info = check_for_updates()

    if update_info:
        if update_info['available']:
            print("✅ New version available!")
            print(f"   Your version: {update_info['current_version']}")
            print(f"   Latest version: {update_info['latest_version']}")
            print(f"   Download: {update_info['url']}")
            print()
            print("Release notes:")
            print(update_info['notes'])
        else:
            print(f"✅ You're up-to-date! (v{update_info['latest_version']})")
    else:
        print("⚠️  Could not check for updates")


if __name__ == "__main__":
    main()
