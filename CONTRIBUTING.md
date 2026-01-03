# Contributing to UsageBar

We're excited that you're interested in contributing! UsageBar is a community-driven project dedicated to bringing the best AI usage tracking experience to Linux.

## 🏗 Project Architecture

UsageBar is composed of two main parts:
1. **The CLI (Swift)**: Located in `Sources/`, this handles the heavy lifting of talking to APIs, parsing output, and managing sessions.
2. **The Tray UI (Python)**: Located in `usagebar-tray.py`, this is a GTK3 application that consumes the CLI's JSON output.

## 🛠 Development Setup

### Prerequisites
- Swift 6.0+
- Python 3.x
- `libappindicator3-dev` and `python3-gi`

### Building the Project
```bash
# Build the CLI
swift build

# Run the Tray App in debug mode
export GDK_BACKEND=x11
python3 usagebar-tray.py
```

## 🧪 Testing
We use Swift Testing for the core logic.
```bash
swift test
```

## 📝 Coding Guidelines
- **Swift**: Follow standard Swift community styles (we include `.swiftformat` and `.swiftlint.yml`).
- **Python**: PEP 8 is preferred. Keep the tray app lightweight.
- **Commits**: Please use descriptive commit messages (e.g., `feat: add support for X provider`).

## 🛡 Security
If you find a security vulnerability, please do NOT open a public issue. Email **tc@tylerbuilds.com** directly or use the GitHub security advisory feature.

---

*Thank you for making UsageBar better for everyone!*
