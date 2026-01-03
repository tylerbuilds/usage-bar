# UsageBar - Portfolio Landing Page Copy

**Hero Section**

# UsageBar
### Track Your LLM Usage Without Leaving the Terminal

A CLI/IDE usage tracker for LLM providers that lives in your Linux top bar. Never hit an API limit surprise again.

[View on GitHub →](https://github.com/tylerbuilds/usage-bar) [Download →]

---

**What It Does**

UsageBar is a Linux system tray application that gives you real-time visibility into your LLM API consumption across multiple providers. Inspired by [CodexBar](https://codexbar.app) for macOS, it brings the same professional monitoring capabilities to Linux.

**Key Features:**
- 📊 **Real-time monitoring** with color-coded progress bars (🟢/🟡/🔴)
- 📈 **24-hour sparkline charts** showing usage trends
- 🔔 **Smart notifications** when you hit 50%, 20%, and 5% thresholds
- 🏢 **Multi-provider support**: Claude, Codex, Gemini, Cursor, Z.ai, Antigravity, Factory
- 💾 **Historical analytics** with 90-day SQLite database
- 🎨 **Modern UI** with dark/light theme auto-detection
- 🔒 **Privacy-first** - all data stored locally, no telemetry
- 🔄 **Auto-update** via GitHub Releases

---

**The Problem**

While macOS users have CodexBar, Linux developers were left in the dark. LLM providers have complex usage limits:
- Session quotas (5-hour rolling windows)
- Weekly/monthly caps
- Model-specific restrictions (Sonnet vs Opus)
- Per-provider billing dashboards

**Missing from the Linux ecosystem:**
- No unified view across providers
- No visual progress indicators
- No trend analysis
- Manual checking required

---

**The Solution**

UsageBar solves this by:

1. **Top Bar Integration** - Lives in your system tray, always visible
2. **Auto-Refresh** - Background polling keeps data fresh
3. **Provider Dashboards** - Quick links to billing/usage pages
4. **Historical Trends** - See usage patterns over time
5. **Privacy-First** - Local SQLite database, no cloud sync

---

**How It Works**

**Architecture:**
- **Backend**: Swift 6.0 CLI (`CodexBarCLI`) for high-performance API polling
- **Frontend**: Python 3.8+, GTK3, AppIndicator3 for native Linux UI
- **Database**: SQLite with automatic 90-day pruning
- **Async Hub**: Background threads ensure smooth UI performance

**Data Sources:**
- Official CLI tools (Claude, Codex, Gemini)
- Browser cookies (with permission)
- Local configuration files
- OAuth credentials (stored securely)

---

**Progress & Status**

**Current Release: v0.0.1** (January 2026)

**Completed Features:**
- ✅ Core tray application with expandable menus
- ✅ 7 provider integrations (Claude, Codex, Gemini, Cursor, Z.ai, Antigravity, Factory)
- ✅ Historical tracking with SQLite
- ✅ Sparkline visualization
- ✅ Custom SVG icons (10 icons)
- ✅ Dark/light theme detection
- ✅ Debian packaging (.deb)
- ✅ AppImage distribution
- ✅ Auto-update checker

**Known Limitations:**
- ⚠️ **GTK3 menu rendering** - SVG icons don't render in menus (using emoji fallback)
- ⚠️ **CSS animations** - Not supported in GTK3 (removed for compatibility)
- ⚠️ **Tooltips** - May not work on all Ubuntu versions
- ⚠️ **Linux-only** - No Windows/macOS support (by design)

**Tech Constraints:**
- Requires Ubuntu 24.04+ or compatible GTK3 distribution
- Swift 6.0+ for building CLI (pre-built binaries available)
- Python 3.8+ for tray app
- AppIndicator3 dependency

---

**Distribution**

**Available Install Methods:**
1. **Source** - `git clone` + Swift build
2. **Debian Package** - `.deb` for apt-based systems
3. **AppImage** - Universal Linux executable

**Download Stats:**
- [GitHub Releases](https://github.com/tylerbuilds/usage-bar/releases)

---

**Technical Deep Dive**

**Why Two Languages?**
- **Swift**: High-performance backend with excellent concurrency, type safety, and existing CodexBar codebase
- **Python**: Native GTK3 bindings, AppIndicator3 support, rapid prototyping

**Design Decisions:**
- **SQLite over JSON**: Faster queries, automatic indexing, 90-day auto-pruning
- **Unicode sparklines**: No external charting libraries, terminal-compatible
- **importlib for modules**: More reliable than regular imports in Python 3.14
- **Cookie-based auth**: Avoids storing raw tokens, respects browser sessions

**Performance:**
- Menu refresh: <500ms
- Memory footprint: ~30-50MB
- Background polling: Configurable (1/5/15 min)

---

**Screenshots**

**Main Menu:**
[Add screenshot showing provider list with progress bars]

**Historical Trends:**
[Add screenshot showing 24h sparkline charts]

**Dark Theme:**
[Add screenshot showing dark theme]

---

**Roadmap**

**Planned Features:**
- [ ] Settings UI (GTK preferences window)
- [ ] Custom alert thresholds per provider
- [ ] Export history to CSV/JSON
- [ ] Cost calculation per provider
- [ ] Flatpak distribution
- [ ] More provider integrations

**Community Requests Welcome:**
- Open to feature requests via [GitHub Issues](https://github.com/tylerbuilds/usage-bar/issues)

---

**Development**

**Built by**: Tyler Casey
**Inspired by**: [CodexBar.app](https://codexbar.app) by [steipete](https://github.com/steipete)
**License**: MIT
**Source Code**: [github.com/tylerbuilds/usage-bar](https://github.com/tylerbuilds/usage-bar)

**Contributors Welcome**: See [CONTRIBUTING.md](https://github.com/tylerbuilds/usage-bar/blob/master/CONTRIBUTING.md)

**Tech Stack:**
- Swift 6.0, Python 3.8+, GTK3, AppIndicator3, SQLite

---

**Press & Awards**

*Add any press coverage, features, or awards here*

---

**FAQ**

**Q: Is this affiliated with CodexBar?**
A: No, this is an independent Linux port. CodexBar is macOS-only.

**Q: Does this send my data anywhere?**
A: No. All data is stored locally in `~/.config/usagebar/history.db`. The only network traffic is to provider APIs (same as your CLI tools).

**Q: Can I trust this with my credentials?**
A: UsageBar doesn't store credentials. It reads from:
- Official CLI tools' credential stores
- Browser cookies (with your permission)
- Config files you control

**Q: Will there be a Windows/macOS version?**
A: No. macOS has CodexBar. Windows users can use WSL + Ubuntu.

**Q: How much does it cost?**
A: Free and open-source (MIT License).

---

**Call to Action**

**Get UsageBar Today**

```bash
# Quick install (Ubuntu/Debian)
wget https://github.com/tylerbuilds/usage-bar/releases/latest/download/usagebar_0.0.1_amd64.deb
sudo dpkg -i usagebar_0.0.1_amd64.deb

# Or download AppImage for any distro
wget https://github.com/tylerbuilds/usage-bar/releases/latest/download/UsageBar-0.0.1-x86_64.AppImage
chmod +x UsageBar-0.0.1-x86_64.AppImage
./UsageBar-0.0.1-x86_64.AppImage
```

**Star on GitHub** ⭐
[github.com/tylerbuilds/usage-bar](https://github.com/tylerbuilds/usage-bar)

**Report Issues**
[github.com/tylerbuilds/usage-bar/issues](https://github.com/tylerbuilds/usage-bar/issues)

**Follow for Updates**
- GitHub: [@tylerbuilds](https://github.com/tylerbuilds)
- Web: [www.tylerbuilds.com](https://www.tylerbuilds.com)

---

**Footer**

Built with ❤️ by [Tyler Casey](https://www.tylerbuilds.com)

Copyright © 2026 | [MIT License](https://github.com/tylerbuilds/usage-bar/blob/master/LICENSE)

---

## Usage Notes for Portfolio Website

**How to Use This Copy:**

1. **Hero Section**: Use for the top of your portfolio page
2. **Features**: Can be broken into bullet points or cards
3. **Problem/Solution**: Good for "About" or "Why" sections
4. **Technical Deep Dive**: For a technical blog post or case study
5. **Screenshots**: Replace placeholders with actual app screenshots
6. **FAQ**: Can be a collapsible section or separate page
7. **CTA**: Use buttons/links for download and GitHub

**Suggested Sections for Your Portfolio:**
- Hero (What it is + download buttons)
- Features grid
- Technical architecture diagram
- Screenshots/carousel
- Installation instructions (collapsible)
- GitHub link
- Other projects link

**Tone**: Professional but approachable, developer-focused
