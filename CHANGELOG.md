# Changelog

All notable changes to UsageBar will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-01-03

### Added
- **Static CLI binary** (56MB) - No Swift runtime dependency!
- Cross-distribution Linux compatibility
- Quick Install guide in README
- Linux compatibility documentation (LINUX_COMPATIBILITY.md)
- SHA256 checksums for release verification

### Changed
- Built CLI with `--static-swift-stdlib` flag
- Updated installation instructions (no Swift required)
- Improved README with Quick Start section
- Updated debian/changelog and debian/control

### Fixed
- Eliminated Swift runtime dependency
- Binary now works on any Linux distro without Swift installed
- Reduced dependencies from 19 Swift libraries to only 4 system libs

### Technical Details
**Before (v0.0.1)**:
- 7.3MB binary, dynamically linked
- Required Swift 6.0+ runtime installed
- 19 Swift library dependencies

**After (v0.0.2)**:
- 56MB binary, statically linked (22MB compressed)
- No Swift runtime required
- Only standard system libraries: libsqlite3, libcurl, libssl, libcrypto

---

## [0.0.1] - 2026-01-03

### Added
- Initial public release of UsageBar for Linux
- Multi-provider support: Claude, Codex, Gemini, Cursor, Z.ai, Antigravity, Factory
- Real-time usage monitoring with visual progress bars (🟢/🟡/🔴)
- Historical analytics with SQLite database (90-day retention)
- Sparkline charts for 24-hour usage trends using Unicode blocks
- Custom SVG icons for tray and providers (10 icons)
- Dark/light theme auto-detection via GTK settings
- Smart usage notifications at 50%, 20%, 5% thresholds
- Provider dashboard shortcuts
- Auto-update checker via GitHub Releases API
- Debian packaging (.deb) for Ubuntu/Debian
- AppImage distribution for universal Linux support
- Comprehensive documentation (README, INSTALL, USER_GUIDE)

### Technical Details
- Backend: Swift 6.0 CLI (CodexBarCLI)
- Frontend: Python 3.8+, GTK3, AppIndicator3
- Database: SQLite with automatic pruning
- Async data fetching for smooth UI performance
- CSS3 styling system with theme support

### Distribution
- Source installation from git
- Debian package (.deb) for apt-based systems
- AppImage for universal Linux distribution
- GitHub Releases with auto-update integration

### Known Limitations
- GTK3 menus don't support SVG icons (using emoji fallback)
- CSS animations not supported (GTK3 limitation)
- Tooltips may not work on all Ubuntu versions

### Documentation
- README.md with installation and usage guides
- INSTALL.md with troubleshooting
- CONTRIBUTING.md for contributors
- USER_GUIDE.md for end users
- Phase summaries (PHASE1-4_SUMMARY.md)

---

## [Unreleased]

### Planned Features
- Settings UI (GTK preferences window)
- Custom alert thresholds per provider
- Export history to CSV/JSON
- Cost calculation per provider
- Flatpak distribution
- More provider integrations
