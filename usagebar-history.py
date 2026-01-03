#!/usr/bin/env python3
"""
UsageBar History Tracking Module

Provides SQLite-based persistence for usage snapshots,
enabling historical analysis and trend visualization.
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Database location
HISTORY_DB = Path.home() / ".config" / "usagebar" / "history.db"

# Pruning settings
MAX_HISTORY_DAYS = 90  # Keep 90 days of data
MAX_SNAPSHOTS_PER_DAY = 24  # Max one per hour


class UsageHistory:
    """Manages usage data persistence and retrieval."""

    def __init__(self, db_path=HISTORY_DB):
        """Initialize history database."""
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Create database schema if it doesn't exist."""
        # Ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                provider TEXT NOT NULL,
                data_json TEXT NOT NULL,
                UNIQUE(provider, timestamp)
            )
        """)

        # Indexes for fast queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_provider_timestamp
            ON usage_snapshots(provider, timestamp DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON usage_snapshots(timestamp DESC)
        """)

        conn.commit()
        conn.close()

    def save_snapshot(self, provider_data):
        """
        Save a usage snapshot for all providers.

        Args:
            provider_data: List of provider dicts from usagebar CLI
        """
        if not provider_data:
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for provider in provider_data:
            p_id = provider.get('provider')
            if not p_id:
                continue

            # Check if we already have a snapshot for this provider in the last hour
            cursor.execute("""
                SELECT COUNT(*) FROM usage_snapshots
                WHERE provider = ?
                AND datetime(timestamp) > datetime('now', '-1 hour')
            """, (p_id,))

            count = cursor.fetchone()[0]

            # Only save if we don't have a recent snapshot (avoid spam)
            if count == 0:
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO usage_snapshots (provider, timestamp, data_json)
                        VALUES (?, ?, ?)
                    """, (p_id, datetime.now().isoformat(), json.dumps(provider)))
                except Exception as e:
                    print(f"[UsageBar] Warning: Failed to save snapshot for {p_id}: {e}")

        conn.commit()
        conn.close()

        # Prune old data periodically
        self.prune_old_data()

    def get_history(self, provider_id, hours=24):
        """
        Get usage history for a specific provider.

        Args:
            provider_id: Provider name (e.g., 'claude', 'codex')
            hours: Number of hours of history to retrieve

        Returns:
            List of dicts with 'timestamp' and 'data' keys
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, data_json
            FROM usage_snapshots
            WHERE provider = ?
            AND datetime(timestamp) >= datetime('now', '-{} hours')
            ORDER BY timestamp ASC
        """.format(hours), (provider_id,))

        results = []
        for ts, data_json in cursor.fetchall():
            try:
                results.append({
                    'timestamp': ts,
                    'data': json.loads(data_json)
                })
            except json.JSONDecodeError:
                continue

        conn.close()
        return results

    def get_latest_snapshots(self, provider_ids=None):
        """
        Get the most recent snapshot for each provider.

        Args:
            provider_ids: List of provider IDs (or None for all)

        Returns:
            Dict mapping provider_id -> latest snapshot data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if provider_ids:
            placeholders = ','.join(['?' for _ in provider_ids])
            cursor.execute(f"""
                SELECT provider, timestamp, data_json
                FROM usage_snapshots
                WHERE provider IN ({placeholders})
                AND id IN (
                    SELECT MAX(id) FROM usage_snapshots GROUP BY provider
                )
            """, provider_ids)
        else:
            cursor.execute("""
                SELECT provider, timestamp, data_json
                FROM usage_snapshots
                WHERE id IN (
                    SELECT MAX(id) FROM usage_snapshots GROUP BY provider
                )
            """)

        results = {}
        for provider, ts, data_json in cursor.fetchall():
            try:
                results[provider] = {
                    'timestamp': ts,
                    'data': json.loads(data_json)
                }
            except json.JSONDecodeError:
                continue

        conn.close()
        return results

    def prune_old_data(self):
        """Remove old data to keep database size manageable."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Delete snapshots older than MAX_HISTORY_DAYS
        cursor.execute("""
            DELETE FROM usage_snapshots
            WHERE datetime(timestamp) < datetime('now', '-{} days')
        """.format(MAX_HISTORY_DAYS))

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted > 0:
            print(f"[UsageBar] Pruned {deleted} old snapshots (> {MAX_HISTORY_DAYS} days)")

    def get_stats(self):
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total snapshots
        cursor.execute("SELECT COUNT(*) FROM usage_snapshots")
        total = cursor.fetchone()[0]

        # Providers tracked
        cursor.execute("SELECT COUNT(DISTINCT provider) FROM usage_snapshots")
        providers = cursor.fetchone()[0]

        # Date range
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM usage_snapshots")
        min_ts, max_ts = cursor.fetchone()

        # Database size
        db_size = self.db_path.stat().st_size if self.db_path.exists() else 0

        conn.close()

        return {
            'total_snapshots': total,
            'providers_tracked': providers,
            'oldest_snapshot': min_ts,
            'newest_snapshot': max_ts,
            'db_size_bytes': db_size
        }


def main():
    """CLI interface for history management."""
    import sys

    history = UsageHistory()

    if len(sys.argv) < 2:
        # Show stats
        stats = history.get_stats()
        print("UsageBar History Statistics")
        print("=" * 40)
        print(f"Total snapshots: {stats['total_snapshots']}")
        print(f"Providers tracked: {stats['providers_tracked']}")
        print(f"Date range: {stats['oldest_snapshot']} to {stats['newest_snapshot']}")
        print(f"Database size: {stats['db_size_bytes']:,} bytes")
        return

    command = sys.argv[1]

    if command == "prune":
        history.prune_old_data()
        print("Pruned old data")
    elif command == "stats":
        stats = history.get_stats()
        for key, value in stats.items():
            print(f"{key}: {value}")
    elif command == "export":
        # Export history as JSON
        provider_id = sys.argv[2] if len(sys.argv) > 2 else None
        hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24

        if provider_id:
            data = history.get_history(provider_id, hours)
        else:
            data = history.get_latest_snapshots()

        print(json.dumps(data, indent=2))
    else:
        print(f"Unknown command: {command}")
        print("Available: prune, stats, export [provider] [hours]")


if __name__ == "__main__":
    main()
