# UsageBar for Linux

**CodexBar v0.14.0 ported to Ubuntu/Linux**

Track your AI usage across multiple providers from the command line.

## ✅ Supported Providers on Linux

| Provider | Status | Notes |
|----------|--------|-------|
| **Claude** | ✅ Working | Uses OAuth (default on Linux) |
| **Codex** | ✅ Working | CLI-based |
| **Gemini** | ✅ Working | CLI-based |
| **z.ai** | ✅ Working | API token in config file |

### ⚠️ Unsupported on Linux

- **Cursor** - macOS-only (requires browser cookie decryption)
- **Factory** - macOS-only
- **Antigravity** - Language server not exposing required ports

## Installation

### Prerequisites

Ubuntu 24.04 (Noble) with Swift 6.0+:

```bash
# Install Swift 6.0.3
wget -q https://download.swift.org/swift-6.0.3-release/ubuntu2404/swift-6.0.3-RELEASE/swift-6.0.3-RELEASE-ubuntu24.04.tar.gz -O /tmp/swift.tar.gz
cd /tmp
tar xzf swift.tar.gz
sudo mv swift-6.0.3-RELEASE-ubuntu24.04 /usr/share/swift
sudo ln -sf /usr/share/swift/usr/bin/swift /usr/bin/swift
sudo ln -sf /usr/share/swift/usr/bin/swiftc /usr/bin/swiftc
```

### Build from Source

```bash
git clone <this-repo> /tmp/usagebar-build
cd /tmp/usagebar-build
swift build --product CodexBarCLI
sudo cp .build/debug/CodexBarCLI /usr/local/bin/usagebar
```

## Configuration

### z.ai API Token

Create `~/.config/codexbar/config.toml`:

```toml
[zai]
zai_token = "your_api_token_here"
```

Or set environment variable:

```bash
export Z_AI_API_KEY="your_api_token_here"
```

### Claude OAuth

Claude uses OAuth by default on Linux. Make sure you're authenticated:

```bash
# Check if claude CLI is authenticated
claude --version

# OAuth will be used automatically by usagebar
```

## Usage

```bash
# Check all providers
usagebar usage --provider all

# Check specific provider
usagebar usage --provider claude
usagebar usage --provider codex
usagebar usage --provider gemini
usagebar usage --provider zai

# JSON output
usagebar usage --provider all --format json --pretty

# Use specific source (web only works on macOS)
usagebar usage --source cli       # Use CLI probes
usagebar usage --source oauth     # Use OAuth (Claude only)
```

## Changes from CodexBar

### Linux-Specific Modifications

1. **Claude defaults to OAuth** - The CLI probe (`/usage` command) was repurposed in Claude v2.0.76+ to show memory context instead of API usage. On Linux, we now default to OAuth.

2. **Web source restricted to macOS** - Browser cookie import uses macOS Keychain. On Linux, `--source web` is disabled; use `--source cli` or `--source oauth` instead.

3. **z.ai config file support** - Added `~/.config/codexbar/config.toml` for storing API tokens on Linux (alternative to macOS Keychain).

4. **Swift 6.0 compatibility** - Downgraded from Swift 6.2 to Swift 6.0 for Ubuntu compatibility, removed experimental feature flags.

### Package.swift Changes

```swift
// swift-tools-version: 6.0  // Downgraded from 6.2
```

### Files Modified

- `Sources/CodexBarCLI/CLIEntry.swift` - Platform-specific source handling
- `Sources/CodexBarCore/Providers/Zai/ZaiSettingsReader.swift` - Config file support
- `Sources/CodexBarCore/Providers/Zai/ZaiUsageStats.swift` - Linux networking imports
- `Package.swift` - Swift version compatibility

## Troubleshooting

### Claude shows "Missing Current session" error

**Solution:** This is expected with Claude CLI v2.0.76+. We fixed this by defaulting to OAuth on Linux. Make sure you're not using `--source cli` for Claude.

### z.ai shows "API token not found"

**Solution:** Create `~/.config/codexbar/config.toml` with your token:

```bash
mkdir -p ~/.config/codexbar
cat > ~/.config/codexbar/config.toml << EOF
[zai]
zai_token = "your_token_here"
