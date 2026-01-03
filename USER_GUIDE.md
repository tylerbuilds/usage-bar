# UsageBar User Guide

Welcome to UsageBar! This guide will help you set up and configure your AI providers so you can monitor your usage directly from your system tray.

## 🔐 Security and Privacy

UsageBar is designed with privacy as its first priority:
- **Local Storage**: Your API keys and session tokens are stored only on your machine.
- **No Cloud Bridge**: Data is fetched directly from providers to your local instance.
- **Secure Integration**: We use official CLI tools and secure environment variables where possible.

---

## 🛠 Provider Setup

### 1. Claude (Anthropic)
UsageBar uses the official Claude CLI for data.
- **Installation**: `npm install -g @anthropic-ai/sdk` (or as per official docs).
- **Authentication**: UsageBar will automatically detect your OAuth session if you are logged in via the CLI.
- **Manual Check**: Run `claude --version` to ensure it's accessible.

### 2. OpenAI (Codex)
We check your OpenAI platform usage.
- **Setup**: Ensure the `openai` CLI is installed and configured with your API key (`OPENAI_API_KEY`).

### 3. z.ai
For z.ai, we support a dedicated configuration file on Linux.
- **Config Path**: `~/.config/codexbar/config.toml`
- **Format**:
  ```toml
  [zai]
  zai_token = "your-api-token-here"
  ```
- **Environment Variable**: Alternatively, set `export Z_AI_API_KEY="your-token"`.

### 4. Google Gemini
Gemini usage is currently supported via the official Google AI Studio integration.
- **Setup**: Ensure your Gemini API credentials are available in your environment or CLI config.

---

## ⚙️ Customization

### Detailed Mode
You can toggle **Detailed Mode** via the ⚙️ Settings menu.
- **Standard**: Shows clean progress bars and remaining percentages.
- **Detailed**: Shows version numbers, raw reset timestamps, and extra metadata.

### Refresh Interval
Adjust how often UsageBar checks for updates (Manual, 1min, 5min, 15min) via the Settings menu. Settings are saved to `~/.config/usagebar/settings.json`.

---

## 🚀 Troubleshooting

### Tray Icon Not Appearing
If you are on Wayland (e.g., modern Ubuntu), run the app using the launcher script:
```bash
./usagebar-tray-launcher.sh
```
This ensures `GDK_BACKEND=x11` is set, which is required for GTK AppIndicators.

### Data Not Refreshing
Check the logs for error messages:
```bash
tail -f /tmp/usagebar-tray.log
```
Common issues include expired OAuth sessions or missing environment variables.

### Missing Providers
Some providers (like Cursor) require browser cookie decryption which is currently macOS-only. We are working on a secure Linux implementation!
