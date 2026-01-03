# UsageBar 🚀

**The premium AI usage tracker for Linux.**

UsageBar is a Linux-native system tray application that provides real-time visibility into your AI provider limits. Inspired by the excellent [CodexBar.app](https://codexbar.app) for macOS, UsageBar brings a rich, expandable UI to Ubuntu and other Linux distributions, ensuring you never hit a "limit reached" surprise again.

![UsageBar Tray Preview](codexbar.png)

## ✨ Why UsageBar?

While macOS users have CodexBar, Linux users were left in the dark—literally. UsageBar was created to bridge that gap, offering:

- **Rich System Tray UI**: Color-coded progress bars (🟢/🟡/🔴) that show your status at a glance.
- **Expandable Menus**: Deep dives into Session, Weekly, and Model-specific usage (like Claude Sonnet).
- **Auto-Refresh**: Background updates keep your data fresh without manual intervention.
- **Detailed Mode**: Toggle technical details like precise reset timestamps and token counts.
- **Provider Dashboard Shortcuts**: Quick access to your billing and usage pages.

## 🛠 Supported Providers on Linux

| Provider | Status | Source |
|----------|--------|--------|
| **Claude** | ✅ Active | OAuth (Official CLI) |
| **Codex** | ✅ Active | Official CLI |
| **Gemini** | ✅ Active | Official CLI |
| **z.ai** | ✅ Active | Config / Token |
| **Antigravity** | ⏳ Planned | Desktop Integration |
| **Cursor** | ⚠️ Limited | macOS Keyring Dependency |

## 🚀 Quick Start

### 1. Prerequisites
Ubuntu 24.04+ and Swift 6.0+ are recommended.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/user/UsageBar.git
cd UsageBar

# Build the CLI tool
swift build -c release --product CodexBarCLI
sudo cp .build/release/CodexBarCLI /usr/local/bin/usagebar

# Run the Tray App
./usagebar-tray-launcher.sh
```

### 3. Setup (API Keys)
UsageBar pulls data from official CLI tools. For specific providers like **z.ai**, create a config file:
```bash
mkdir -p ~/.config/codexbar
echo 'zai_token = "your_token"' > ~/.config/codexbar/config.toml
```
*Your secrets are stored locally and never transmitted to third parties.*

## 📐 Technical Build Details

UsageBar is built with a decoupled architecture:
1. **Core (Swift)**: A high-performance usage bridge that talks to provider APIs and local CLI tools.
2. **Tray UI (Python/GTK3)**: A lightweight, responsive menu system using `AppIndicator3`.
3. **Async Hub**: All data fetching happens in background threads to ensure your desktop environment remains buttery smooth.

## 🐧 Distro Compatibility

While UsageBar is designed with portability in mind, it is currently primarily tested on **Ubuntu 24.04 (Noble)**. 

If you get it running on Arch, Fedora, openSUSE, or other distributions, please let us know or submit a PR to update the documentation!

## 🤝 Contributing

We love contributions! Whether it's adding support for new providers or fixing bugs on different Linux flavors, check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## 📜 License

Created with ❤️ by **Tyler Casey** ([@TylerIsBuilding](https://x.com/TylerIsBuilding)).  
Email: [tc@tylerbuilds.com](mailto:tc@tylerbuilds.com)

Licensed under the [MIT License](LICENSE).

---
*Inspired by [CodexBar.app](https://codexbar.app). This project is not affiliated with the original CodexBar team.*
