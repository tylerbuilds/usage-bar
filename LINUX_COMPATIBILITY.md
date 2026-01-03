# Linux Compatibility & Distribution Analysis

## Current Status: ⚠️ Partially Compatible

**Last Updated**: January 3, 2026

---

## What Works ✅

### Source Installation
- **Platforms**: Ubuntu 24.04+, Debian 12+, Arch, Fedora (with Swift 6.0+)
- **Requirements**: Swift 6.0+ compiler, Python 3.8+, GTK3, AppIndicator3
- **Method**: `swift build` from source
- **Status**: ✅ Fully functional

### Pre-built CLI Binaries
- **Available in Release**:
  - `CodexBarCLI-v0.0.1-linux-x86_64.tar.gz` (26MB)
  - `CodexBarCLI-v0.0.1-linux-aarch64.tar.gz` (25MB)
- **Built by**: GitHub Actions CI
- **Status**: ✅ Downloadable from v0.0.1 release

---

## Critical Issues ⚠️

### 1. Swift Runtime Dependency

**Problem**: The CLI binary is **dynamically linked** against Swift runtime libraries.

```bash
$ ldd .build/release/CodexBarCLI
libswiftCore.so => /usr/share/swift/usr/lib/swift/linux/libswiftCore.so
libswift_Concurrency.so => /usr/share/swift/usr/lib/swift/linux/libswift_Concurrency.so
libFoundation.so => /usr/share/swift/usr/lib/swift/linux/libFoundation.so
... (19 Swift libraries total)
```

**Impact**:
- Users **must have Swift 6.0+ runtime installed** to run the binary
- Simply downloading the CLI binary won't work without Swift runtime
- The `.deb` package and AppImage don't include Swift runtime libraries

**What This Means**:
```bash
# This WILL FAIL without Swift runtime:
$ wget https://github.com/.../CodexBarCLI-v0.0.1-linux-x86_64.tar.gz
$ tar xzf ...
$ ./CodexBarCLI
error: while loading shared libraries: libswiftCore.so: cannot open shared object file
```

---

### 2. Debian Package (`.deb`)

**File**: `debian/control`

**Current Depends**:
```
Depends: python3 (>= 3.8), python3-gi, gir1.2-appindicator3-0.1, libsqlite3-0
```

**Missing**:
- ❌ Swift runtime dependencies
- ❌ Swift library paths

**Result**: The `.deb` package will install, but the `usagebar` CLI binary won't run without Swift installed.

---

### 3. AppImage Build Script

**File**: `build-appimage.sh`

**Issues**:
1. **Wrong Tool**: Uses `appimage-builder` (deprecated) instead of `appimagetool`
2. **Missing Swift Runtime**: Doesn't bundle Swift libraries into AppImage
3. **Incomplete Library Path**: Sets `LD_LIBRARY_PATH` but doesn't include Swift libs

**Current Script (Line 76)**:
```bash
./appimage-builder-x86_64.AppImage --appdir "$APPDIR" --output "$OUTPUT"
```

**Should Be**:
```bash
./appimagetool --appdir "$APPDIR" --output "$OUTPUT"
```

**Missing from AppDir**:
- `/usr/share/swift/usr/lib/swift/linux/*.so` (Swift runtime)

---

## What Needs to Be Fixed 🔧

### Priority 1: Fix Swift Runtime Distribution

**Option A: Static Linking (Recommended)**
Build the CLI with statically linked Swift runtime:

```bash
swift build -c release --product CodexBarCLI \
  -Xlinker -static-libswift-core \
  --static-swift-stdlib
```

**Pros**:
- Single binary, no runtime dependencies
- Works on any Linux distro
- Smaller download

**Cons**:
- Larger binary size (~15MB increase)
- Longer build time

---

**Option B: Bundle Swift Runtime**

Include Swift libraries in the distribution:

**For .deb**:
```makefile
# debian/rules
install -m 644 /usr/share/swift/usr/lib/swift/linux/*.so \
  debian/usagebar/usr/lib/usagebar/swift/
```

**For AppImage**:
```bash
# build-appimage.sh
mkdir -p "$APPDIR/usr/share/swift/usr/lib/swift/linux"
cp /usr/share/swift/usr/lib/swift/linux/*.so \
  "$APPDIR/usr/share/swift/usr/lib/swift/linux/"
```

**Pros**:
- Keeps binary size smaller
- Can share Swift runtime between tools

**Cons**:
- More complex packaging
- Version conflicts possible

---

### Priority 2: Fix AppImage Build Script

**Changes Required**:

1. **Use appimagetool**:
```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

./appimagetool-x86_64.AppImage "$APPDIR" "$OUTPUT"
```

2. **Bundle Swift runtime**:
```bash
mkdir -p "$APPDIR/usr/share/swift/usr/lib/swift/linux"
cp -r /usr/share/swift/usr/lib/swift/linux/*.so "$APPDIR/usr/share/swift/usr/lib/swift/linux/"
```

3. **Update AppRun**:
```bash
export LD_LIBRARY_PATH="${HERE}/usr/share/swift/usr/lib/swift/linux:${LD_LIBRARY_PATH}"
```

---

### Priority 3: Update .deb Control File

**File**: `debian/control`

**Add Swift Runtime Dependency**:
```
Depends: python3 (>= 3.8), python3-gi, gir1.2-appindicator3-0.1, libsqlite3-0,
 swift6-runtime (>= 6.0) | libswift-core-dev
```

**Better**: Recommend static linking so no Swift runtime dep needed.

---

### Priority 4: Document Swift Requirement

**File**: `README.md`

**Add to Installation Section**:
```markdown
### Prerequisites

**Important**: UsageBar requires Swift 6.0+ runtime.

**Check if Swift is installed**:
```bash
swift --version
```

**Install Swift Runtime**:

Ubuntu/Debian:
```bash
# Install Swift runtime
wget https://download.swift.org/swift-6.0.3-release/ubuntu2404/swift-6.0.3-RELEASE/swift-6.0.3-RELEASE-ubuntu24.04.tar.gz
tar xzf swift-6.0.3-RELEASE-ubuntu24.04.tar.gz
sudo mv swift-6.0.3-RELEASE /usr/share/swift
```

Alternatively, install the full Swift toolchain:
```bash
sudo apt install swiftswift
```
```

---

## Distribution Compatibility Matrix

| Distribution | Source Install | Pre-built Binary | .deb | AppImage |
|--------------|----------------|------------------|------|----------|
| **Ubuntu 24.04** | ✅ (with Swift) | ⚠️ (needs Swift) | ⚠️ (missing dep) | ❌ (broken) |
| **Ubuntu 22.04** | ✅ (with Swift) | ⚠️ (needs Swift) | ⚠️ (missing dep) | ❌ (broken) |
| **Debian 12** | ✅ (with Swift) | ⚠️ (needs Swift) | ⚠️ (missing dep) | ❌ (broken) |
| **Fedora 40** | ✅ (with Swift) | ⚠️ (needs Swift) | N/A | ❌ (broken) |
| **Arch Linux** | ✅ (AUR: swift) | ⚠️ (needs Swift) | N/A | ❌ (broken) |

**Legend**:
- ✅ Works
- ⚠️ Works with manual setup
- ❌ Doesn't work
- N/A Not available

---

## Quick Fix Options

### Option 1: Static Binary (Easiest)

Rebuild the CLI with static linking:

```bash
# Clean build
rm -rf .build

# Build with static Swift stdlib
swift build -c release --product CodexBarCLI \
  --static-swift-stdlib \
  -Xlinker -s

# Verify
ldd .build/release/CodexBarCLI
# Should show: not a dynamic executable
```

Then update release with this static binary.

---

### Option 2: Document Swift Requirement (Quickest)

Add clear installation instructions for Swift runtime:

```markdown
## Installation

### Option A: From Pre-built Binary

1. Install Swift 6.0+ runtime:
   ```bash
   # Ubuntu/Debian
   sudo apt install swiftswift

   # Fedora
   sudo dnf install swift-lang

   # Arch
   yay -s swift
   ```

2. Download UsageBar CLI:
   ```bash
   wget https://github.com/tylerbuilds/usage-bar/releases/latest/download/CodexBarCLI-v0.0.1-linux-x86_64.tar.gz
   tar xzf CodexBarCLI-v0.0.1-linux-x86_64.tar.gz
   sudo cp CodexBarCLI /usr/local/bin/usagebar
   ```

3. Install Python dependencies:
   ```bash
   sudo apt install python3-gi gir1.2-appindicator3-0.1
   ```

4. Run:
   ```bash
   ./usagebar-tray-launcher.sh
   ```
```

---

### Option 3: Use Existing CI Binaries

The GitHub release already has pre-built binaries from CI:

```bash
# Download CI-built binary (has same Swift runtime issue)
wget https://github.com/tylerbuilds/usage-bar/releases/download/v0.0.1/CodexBarCLI-v0.0.1-linux-x86_64.tar.gz
tar xzf CodexBarCLI-v0.0.1-linux-x86_64.tar.gz

# Verify Swift is installed
swift --version || (echo "Install Swift first" && exit 1)

# Copy to PATH
sudo cp CodexBarCLI /usr/local/bin/usagebar
```

---

## Recommendations

### For Immediate Release (Today)

**Do This**:
1. ✅ Keep current binaries in release
2. ✅ Add Swift runtime requirement to README
3. ✅ Add troubleshooting section for "libswiftCore.so not found"
4. ⚠️ Document that .deb and AppImage are experimental

**README Addition**:
```markdown
### ⚠️ Important: Swift Runtime Required

UsageBar's CLI requires Swift 6.0+ runtime to be installed on your system.

**Check if you have Swift**:
```bash
swift --version
```

**If not installed**:
```bash
# Ubuntu/Debian
sudo apt install swiftswift

# Or download from swift.org
wget https://download.swift.org/swift-6.0.3-release/ubuntu2404/swift-6.0.3-RELEASE/swift-6.0.3-RELEASE-ubuntu24.04.tar.gz
```
```

---

### For Next Release (v0.0.2)

**Do This**:
1. 🔧 Build static binary (`--static-swift-stdlib`)
2. 🔧 Fix AppImage script to use `appimagetool`
3. 🔧 Update .deb to either:
   - Depend on `swift-runtime`, OR
   - Bundle Swift libraries
4. ✅ Test on clean Ubuntu 24.04 VM
5. ✅ Test on Fedora
6. ✅ Test AppImage on multiple distros

---

## Testing Checklist

Before calling it "fully Linux-friendly":

- [ ] Install on clean Ubuntu 24.04 VM (no Swift pre-installed)
- [ ] Install on clean Fedora 40 VM
- [ ] Test AppImage on Ubuntu, Fedora, Arch
- [ ] Verify .deb installs and runs
- [ ] Test all 7 providers
- [ ] Verify history tracking works
- [ ] Check dark/light theme switching
- [ ] Test auto-update checker

---

## Summary

**Current Status**: ⚠️ **Partially Linux-Friendly**

**Works**: Source installation for users with Swift 6.0+ installed

**Doesn't Work**: Plug-and-play installation for users without Swift

**To Fix**: Either static link the binary OR bundle Swift runtime in distributions

**Time to Fix**: 1-2 hours for static binary, 4-6 hours for full bundling solution

---

**Generated for**: UsageBar v0.0.1
**Author**: Tyler Casey
**Date**: January 3, 2026
