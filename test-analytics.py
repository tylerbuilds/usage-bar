#!/usr/bin/env python3
"""
Populate test history data to demonstrate sparkline features.
Creates fake usage snapshots spanning 24 hours.
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from usagebar_history import UsageHistory

def create_test_snapshots():
    """Create test usage snapshots with varying usage patterns."""

    # Sample provider data template
    base_data = {
        "provider": "claude",
        "usage": {
            "primary": {
                "usedPercent": 10,
                "limit": 200000,
                "used": 20000,
                "resetsAt": "2026-01-04T00:00:00Z",
                "resetDescription": "in 6 hours"
            },
            "secondary": None,
            "tertiary": {
                "usedPercent": 5,
                "limit": 500000,
                "used": 25000,
                "model": "claude-3-5-sonnet-20241022"
            }
        },
        "credits": {
            "remaining": 15.50,
            "currency": "USD"
        },
        "accountEmail": "user@example.com",
        "version": "1.0.0"
    }

    history = UsageHistory()

    print("Creating test snapshots...")

    # Create 10 snapshots over 24 hours with increasing usage
    for i in range(10):
        # Vary usage from 10% to 45%
        usage_pct = 10 + (i * 3.5)

        snapshot = base_data.copy()
        snapshot["usage"]["primary"]["usedPercent"] = usage_pct
        snapshot["usage"]["primary"]["used"] = int(usage_pct * 2000)

        # Manually set timestamp
        timestamp = datetime.now() - timedelta(hours=24-(i*2.5))
        snapshot["timestamp"] = timestamp.isoformat()

        # Save directly to database
        import sqlite3
        conn = sqlite3.connect(history.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO usage_snapshots (provider, timestamp, data_json)
            VALUES (?, ?, ?)
        """, (snapshot["provider"], timestamp.isoformat(), json.dumps(snapshot)))
        conn.commit()
        conn.close()

        print(f"  Snapshot {i+1}: {usage_pct:.1f}% ({timestamp.strftime('%H:%M')})")

    print(f"\n✅ Created 10 test snapshots for 'claude'")
    print(f"Database: {history.db_path}")

    # Verify
    data = history.get_history("claude", hours=24)
    print(f"\n✅ Retrieved {len(data)} snapshots from database")

    if data:
        print(f"\nFirst snapshot: {data[0]['timestamp']}")
        print(f"Last snapshot: {data[-1]['timestamp']}")

        # Show sparkline
        from usagebar_charts import UsageChart
        sparkline = UsageChart.render_sparkline_text(data, width=20)
        trend = UsageChart.calculate_trend(data)

        print(f"\n📊 Sparkline Preview:")
        print(f"   {sparkline} {trend['direction']} ({trend['change']:+.1f}%)")

if __name__ == "__main__":
    create_test_snapshots()
