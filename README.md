# UsageBar - Linux LLM Usage Tracker

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: Linux](https://img.shields.io/badge/Platform-Linux-orange.svg)
![Version: 0.0.2](https://img.shields.io/badge/Version-0.0.2-green.svg)

UsageBar is a CLI/IDE usage tracker for LLM providers on Linux that lives in the top bar. Inspired by steipete's CodexBar.

**[www.tylerbuilds.com](https://www.tylerbuilds.com) | [github.com/tylerbuilds](https://github.com/tylerbuilds)**

## ✨ Features

- **Multi-Provider Support**: Claude, Codex, Gemini, Cursor, Z.ai, Antigravity, Factory
- **CLI & IDE Usage Tracking**: Monitors LLM usage from command-line tools and IDEs
- **Top Bar Integration**: Lives in the system tray for at-a-glance visibility
- **Historical Analytics**: SQLite-based history with 90-day retention
- **Sparkline Charts**: Beautiful 24h trend visualization using Unicode
- **Privacy-First**: Local data storage, no telemetry
- **Smart Notifications**: Usage alerts at 50%, 20%, 5% thresholds
- **Modern UI**: Custom SVG icons, CSS styling, dark/light theme support
- **Auto-Update**: GitHub Releases integration for seamless updates

## ✨ Why UsageBar?

Inspired by steipete's CodexBar for macOS, UsageBar brings similar LLM usage tracking capabilities to Linux. It runs in the top bar and offers:

- **Rich Top Bar UI**: Color-coded progress bars (🟢/🟡/🔴) that show your status at a glance
- **Expandable Menus**: Deep dives into Session, Weekly, and Model-specific usage (like Claude Sonnet)
- **Auto-Refresh**: Background updates keep your data fresh without manual intervention
- **Detailed Mode**: Toggle technical details like precise reset timestamps and token counts
- **Provider Dashboard Shortcuts**: Quick access to your billing and usage pages
- **Historical Trends**: 24-hour sparkline charts showing usage patterns

## 🛠 Supported Providers

| Provider | Status | Source |
|----------|--------|--------|
| **Claude** | ✅ Active | OAuth (Official CLI) |
| **Codex** | ✅ Active | Official CLI |
| **Gemini** | ✅ Active | Official CLI |
| **Cursor** | ✅ Active | Official CLI |
| **Z.ai** | ✅ Active | Config / Token |
| **Antigravity** | ✅ Active | Official CLI |
| **Factory** | ✅ Active | Official CLI |

## 📦 Installation

### Quick Install (Static Binary - Recommended)

**No Swift runtime required!** The v0.0.2 static binary works on any Linux distro.

```bash
# Download static binary (22MB)
wget https://github.com/tylerbuilds/usage-bar/releases/download/v0.0.2/usagebar-0.0.2-linux-x86_64-static.tar.gz
tar xzf usagebar-0.0.2-linux-x86_64-static.tar.gz

# Install binary
sudo cp usagebar /usr/local/bin/usagebar
usagebar --version

# Install Python dependencies
sudo apt install python3-gi gir1.2-appindicator3-0.1 libsqlite3-0

# Run the tray app
./usagebar-tray-launcher.sh
```

### Ubuntu/Debian (.deb)
```bash
wget https://github.com/tylerbuilds/usage-bar/releases/download/v0.0.2/usagebar_0.0.2_amd64.deb
sudo dpkg -i usagebar_0.0.2_amd64.deb
```

### AppImage (Universal Linux)
```bash
wget https://github.com/tylerbuilds/usage-bar/releases/download/v0.0.2/UsageBar-0.0.2-x86_64.AppImage
chmod +x UsageBar-0.0.2-x86_64.AppImage
./UsageBar-0.0.2-x86_64.AppImage
```

### From Source
```bash
git clone https://github.com/tylerbuilds/usage-bar.git
cd usage-bar
swift build -c release --product CodexBarCLI
sudo cp .build/release/CodexBarCLI /usr/local/bin/usagebar
./usagebar-tray-launcher.sh
```

## 🎯 Quick Start

1. **Configure Providers**: Edit `~/.config/usagebar/config.json`
2. **Launch**: Run `usagebar-tray-launcher.sh` or start from Applications menu
3. **View Usage**: Click the tray icon to see real-time stats
4. **Check History**: Usage data stored in `~/.config/usagebar/history.db`

### Configuration for Token-Based Providers

For providers like **Z.ai**, create a config file:
```bash
mkdir -p ~/.config/codexbar
echo 'zai_token = "your_token"' > ~/.config/codexbar/config.toml
```
*Your secrets are stored locally and never transmitted to third parties.*

## 🛠️ Tech Stack

- **Backend**: Swift 6.0 (CodexBarCLI)
- **Frontend**: Python 3.8+, GTK3, AppIndicator3
- **Database**: SQLite (historical tracking)
- **Styling**: CSS3 with dark/light theme support
- **Packaging**: Debian (.deb), AppImage

### Architecture

UsageBar is built with a decoupled architecture:
1. **Core (Swift)**: A high-performance usage bridge that talks to provider APIs and local CLI/IDE tools
2. **Top Bar UI (Python/GTK3)**: A lightweight, responsive menu system using `AppIndicator3`
3. **Async Hub**: All data fetching happens in background threads to ensure your desktop environment remains smooth

## 🐧 Distro Compatibility

**Tested on**: Ubuntu 24.04 (Noble)

**Compatible with**: Debian, Fedora, Arch, openSUSE, and other GTK3-based distributions via AppImage.

If you get it running on other distributions, please let us know or submit a PR to update the documentation!

## 📈 Features Roadmap

- [ ] Settings UI (GTK preferences window)
- [ ] Custom alert thresholds per provider
- [ ] Export history to CSV/JSON
- [ ] Cost calculation per provider
- [ ] Flatpak distribution

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

We love contributions! Whether it's adding support for new providers or fixing bugs on different Linux flavors, your help is appreciated.

## 📜 License

Copyright © 2026 Tyler Casey

[MIT License](LICENSE)

## 🔗 Links

- **Website**: [www.tylerbuilds.com](https://www.tylerbuilds.com)
- **GitHub**: [github.com/tylerbuilds](https://github.com/tylerbuilds)
- **Inspired by**: [CodexBar](https://github.com/steipete/codexbar) by steipete

---

**Keywords**: `llm-usage-tracker` `linux` `gtk3` `top-bar` `claude` `openai` `ide` `cli` `python` `swift` `ubuntu`
