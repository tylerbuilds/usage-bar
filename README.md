# UsageBar - Linux AI Usage Tracker

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: Linux](https://img.shields.io/badge/Platform-Linux-orange.svg)
![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-green.svg)

A professional system tray application for tracking AI API usage across multiple providers. The Linux port of CodexBar, built with GTK3 and Python.

**[www.tylerbuilds.com](https://www.tylerbuilds.com) | [github.com/tylerbuilds](https://github.com/tylerbuilds)**

![UsageBar Tray Preview](codexbar.png)

## ✨ Features

- **Multi-Provider Support**: Claude, Codex, Gemini, Cursor, Z.ai, Antigravity, Factory
- **Real-Time Monitoring**: Live usage tracking with visual progress bars
- **Historical Analytics**: SQLite-based history with 90-day retention
- **Sparkline Charts**: Beautiful 24h trend visualization using Unicode
- **Privacy-First**: Local data storage, no telemetry
- **Smart Notifications**: Usage alerts with 50%/20%/5% thresholds
- **Modern UI**: Custom SVG icons, CSS styling, dark/light theme support
- **Auto-Update**: GitHub Releases integration for seamless updates

## ✨ Why UsageBar?

While macOS users have CodexBar, Linux users were left in the dark—literally. UsageBar was created to bridge that gap, offering:

- **Rich System Tray UI**: Color-coded progress bars (🟢/🟡/🔴) that show your status at a glance
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

### Ubuntu/Debian (.deb)
```bash
wget https://github.com/tylerbuilds/UsageBar/releases/latest/download/usagebar_1.0.0_amd64.deb
sudo dpkg -i usagebar_1.0.0_amd64.deb
```

### AppImage (Universal Linux)
```bash
wget https://github.com/tylerbuilds/UsageBar/releases/latest/download/UsageBar-1.0.0-x86_64.AppImage
chmod +x UsageBar-1.0.0-x86_64.AppImage
./UsageBar-1.0.0-x86_64.AppImage
```

### From Source
```bash
git clone https://github.com/tylerbuilds/UsageBar.git
cd UsageBar
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
1. **Core (Swift)**: A high-performance usage bridge that talks to provider APIs and local CLI tools
2. **Tray UI (Python/GTK3)**: A lightweight, responsive menu system using `AppIndicator3`
3. **Async Hub**: All data fetching happens in background threads to ensure your desktop environment remains buttery smooth

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
- **Inspired by**: [CodexBar.app](https://codexbar.app) (macOS)

---

**Keywords**: `ai-usage-tracker` `linux` `gtk3` `system-tray` `claude` `openai` `api-monitoring` `python` `swift` `ubuntu`
