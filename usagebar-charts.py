#!/usr/bin/env python3
"""
UsageBar Chart Rendering Module

Provides Cairo-based visualization for usage trends,
including sparklines and mini charts for the tray UI.
"""

import math


class UsageChart:
    """Renders usage visualizations using Cairo."""

    @staticmethod
    def render_sparkline_text(history_points, width=30):
        """
        Render a sparkline as Unicode text (fallback for no Cairo).

        Args:
            history_points: List of usage dicts with 'usedPercent'
            width: Width of sparkline in characters

        Returns:
            String sparkline like "▂▅▇█▇▅▃"
        """
        if len(history_points) < 2:
            return "▄▄▄▄▄"[:width]

        # Extract percentages
        percentages = []
        for p in history_points:
            data = p.get('data', {})
            usage = data.get('usage', {})
            primary = usage.get('primary', {})
            pct = primary.get('usedPercent', 0)
            percentages.append(pct)

        if not percentages:
            return "▄▄▄▄▄"[:width]

        # Normalize to 0-1 range
        min_val = min(percentages)
        max_val = max(percentages)
        range_val = max_val - min_val or 1

        # Map to Unicode block elements
        # 8 levels: ▁ ▂ ▃ ▄ ▅ ▆ ▇ █
        blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

        # Resample to width
        if len(percentages) > width:
            # Downsample
            step = len(percentages) / width
            resampled = []
            for i in range(width):
                idx = int(i * step)
                resampled.append(percentages[idx])
            percentages = resampled

        # Convert to blocks
        sparkline = ""
        for pct in percentages:
            normalized = (pct - min_val) / range_val
            block_idx = min(int(normalized * 8), 7)
            sparkline += blocks[block_idx]

        return sparkline

    @staticmethod
    def calculate_trend(history_points):
        """
        Calculate usage trend direction and rate.

        Args:
            history_points: List of usage dicts

        Returns:
            Dict with 'direction' (up/down/stable) and 'rate' (percent/hour)
        """
        if len(history_points) < 2:
            return {'direction': 'stable', 'rate': 0}

        # Get first and last
        first = history_points[0].get('data', {}).get('usage', {}).get('primary', {}).get('usedPercent', 0)
        last = history_points[-1].get('data', {}).get('usage', {}).get('primary', {}).get('usedPercent', 0)

        # Calculate rate
        diff = last - first
        direction = 'up' if diff > 5 else 'down' if diff < -5 else 'stable'

        return {
            'direction': direction,
            'change': diff,
            'first_pct': first,
            'last_pct': last
        }


def render_ascii_chart(values, width=40, height=8):
    """
    Render an ASCII chart of values.

    Args:
        values: List of numeric values
        width: Chart width in characters
        height: Chart height in characters

    Returns:
        Multi-line string chart
    """
    if not values:
        return " " * width

    # Normalize values
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val or 1

    # Create chart rows (top to bottom)
    chart = []
    for row in range(height):
        line = ""
        threshold = max_val - (row / height) * range_val

        for val in values:
            if val >= threshold:
                line += "█"
            else:
                line += " "

        chart.append(line)

    # Add x-axis
    chart.append("─" * width)

    return "\n".join(chart)


def main():
    """Test chart rendering."""
    import sys

    # Sample data
    sample_data = [
        {'data': {'usage': {'primary': {'usedPercent': 10}}}},
        {'data': {'usage': {'primary': {'usedPercent': 15}}}},
        {'data': {'usage': {'primary': {'usedPercent': 20}}}},
        {'data': {'usage': {'primary': {'usedPercent': 18}}}},
        {'data': {'usage': {'primary': {'usedPercent': 25}}}},
        {'data': {'usage': {'primary': {'usedPercent': 30}}}},
        {'data': {'usage': {'primary': {'usedPercent': 35}}}},
    ]

    print("Sparkline Test")
    print("=" * 40)
    sparkline = UsageChart.render_sparkline_text(sample_data, width=20)
    print(f"Sparkline: {sparkline}")

    print("\nTrend Analysis")
    print("=" * 40)
    trend = UsageChart.calculate_trend(sample_data)
    print(f"Direction: {trend['direction']}")
    print(f"Change: {trend['change']:+.1f}%")
    print(f"Range: {trend['first_pct']:.0f}% → {trend['last_pct']:.0f}%")


if __name__ == "__main__":
    main()
