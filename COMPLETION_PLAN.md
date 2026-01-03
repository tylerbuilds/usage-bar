# UsageBar Linux Completion Plan

## Current Status ✅

**Working Providers:**
- ✅ Claude (OAuth)
- ✅ Codex (CLI)
- ✅ Gemini (CLI)
- ✅ z.ai (Config file)

**Need Implementation:**
- ❌ Cursor (Chrome cookies on Linux)
- ❌ Factory (Chrome cookies on Linux)
- ⚠️ Antigravity (Language server port detection)

---

## Task 1: Chrome Cookie Support for Linux (Cursor + Factory)

**Priority:** HIGH - Enables 2 more providers

### Overview

Cursor and Factory both use Chrome cookies on macOS. On Linux, we need to read Chrome's cookie database and decrypt the cookies.

### Implementation Steps

#### 1.1 Add Linux Chrome Cookie Decryption

**File:** `Sources/CodexBarCore/Host/Cookies/ChromeCookieImporter.swift`

**Current state:** Wrapped in `#if os(macOS)` - uses macOS Keychain for decryption.

**Required changes:**

```swift
// Add Linux support
#if os(Linux)
import Glibc
#elseif os(macOS)
// existing macOS imports
#endif

// In ChromeCookieImporter enum:
#if os(Linux)
private static func getChromeEncryptionKey() -> Data? {
    // On Linux, Chrome uses either:
    // 1. No encryption (older versions)
    // 2. GNOME Keyring
    // 3. KDE Wallet
    // 4. Custom encryption with secret stored in system keyring

    // Path to Chrome's "Local State" JSON
    let localStatePath = chromeProfilePath()
        .appendingPathComponent("Local State")

    guard let localStateData = try? Data(contentsOf: localStatePath),
          let localState = try? JSONSerialization.jsonObject(with: localStateData) as? [String: Any],
          let osCrypt = localState["os_crypt"] as? [String: Any],
          let encryptedKey = osCrypt["encrypted_key"] as? String else {
        return nil
    }

    // The encrypted_key is base64 encoded. Remove the "DPAPI" prefix if present,
    // then decode base64 to get the actual encrypted key.
    let keyData = Data(base64Encoded: encryptedKey)
        .filter { $0.prefix != "DPAPI" }

    // On Linux, this key is encrypted with the system keyring.
    // Need to decrypt using:
    // - GNOME Keylib (libsecret)
    // - Or KDE Wallet
    // - Or plain text (some systems)

    // For now, check if cookies are stored in plaintext
    return keyData
}
#endif

// Modify loadCookies to handle Linux
#if os(Linux)
static func loadCookies(matchingDomains domains: [String]) throws -> [CookieSource] {
    let home = FileManager.default.homeDirectoryForCurrentUser
    let configPath = home
        .appendingPathComponent(".config")
        .appendingPathComponent("google-chrome")

    let profilePath = configPath.appendingPathComponent("Default")
    let cookieDBPath = profilePath.appendingPathComponent("Network").appendingPathComponent("Cookies")

    // Check if cookies are in newer "Cookies" file (SQLite) or fallback to "Cookies" in profile root
    let actualCookieDB = FileManager.default.fileExists(atPath: cookieDBPath.path)
        ? cookieDBPath
        : profilePath.appendingPathComponent("Cookies")

    guard FileManager.default.fileExists(atPath: actualCookieDB.path) else {
        throw ImportError.cookieDBNotFound(path: actualCookieDB.path)
    }

    // Copy the DB to avoid locking issues
    let tempDB = FileManager.default.temporaryDirectory
        .appendingPathComponent(UUID().uuidString + ".db")
    try? FileManager.default.removeItem(at: tempDB)
    try FileManager.default.copyItem(at: actualCookieDB, to: tempDB)

    defer {
        try? FileManager.default.removeItem(at: tempDB)
    }

    // Query SQLite for cookies
    let cookies = try queryCookiesFromDB(
        path: tempDB,
        domains: domains
    )

    return [CookieSource(
        label: "Chrome (Linux)",
        records: cookies
    )]
}
#endif
```

#### 1.2 Add SQLite Helper for Linux

Create new file: `Sources/CodexBarCore/Host/Cookies/SQLiteCookieReader.swift`

```swift
#if os(Linux)
import Foundation
import SQLite3

struct SQLiteCookieReader {
    static func queryCookies(
        from dbPath: URL,
        matchingDomains domains: [String]
    ) throws -> [ChromeCookieImporter.CookieRecord] {
        var db: OpaquePointer?

        guard sqlite3_open_v2(
            dbPath.path,
            &db,
            SQLITE_OPEN_READONLY,
            nil
        ) == SQLITE_OK else {
            throw ChromeCookieImporter.ImportError.sqliteFailed(
                message: "Failed to open database"
            )
        }

        defer {
            sqlite3_close(db)
        }

        // Build query - Chrome stores cookies in 'cookies' table
        let query = """
            SELECT host_key, name, path, expires_utc, is_secure, is_httponly, encrypted_value
            FROM cookies
            WHERE host_key LIKE ?
        """

        var statement: OpaquePointer?
        var cookies: [ChromeCookieImporter.CookieRecord] = []

        for domain in domains {
            guard sqlite3_prepare_v2(
                db, query, -1, &statement, nil
            ) == SQLITE_OK else {
                continue
            }

            let domainPattern = "%\(domain)%"
            sqlite3_bind_text(statement, 1, (domainPattern as NSString).utf8String, -1, nil)

            while sqlite3_step(statement) == SQLITE_ROW {
                if let cookie = parseCookieRow(statement: statement) {
                    cookies.append(cookie)
                }
            }

            sqlite3_finalize(statement)
        }

        return cookies
    }

    private static func parseCookieRow(
        statement: OpaquePointer?
    ) -> ChromeCookieImporter.CookieRecord? {
        guard let statement = statement else { return nil }

        let hostKey = String(cString: sqlite3_column_text(statement, 0))
        let name = String(cString: sqlite3_column_text(statement, 1))
        let path = String(cString: sqlite3_column_text(statement, 2))
        let expiresUTC = sqlite3_column_int64(statement, 3)
        let isSecure = sqlite3_column_int(statement, 4) != 0
        let isHTTPOnly = sqlite3_column_int(statement, 5) != 0

        // Get encrypted value blob
        let encryptedValueLength = sqlite3_column_bytes(statement, 6)
        guard let encryptedValueBlob = sqlite3_column_blob(statement, 6) else {
            return nil
        }

        let encryptedValue = Data(
            bytes: encryptedValueBlob,
            count: Int(encryptedValueLength)
        )

        // Decrypt the value
        let value: String
        if encryptedValue.starts(with: Data([0x76, 0x31, 0x30])) {
            // v10 format - encrypted with AES
            // This requires the encryption key from Local State
            // For now, try plaintext
            value = String(data: encryptedValue, encoding: .utf8) ?? ""
        } else {
            // Plaintext
            value = String(data: encryptedValue, encoding: .utf8) ?? ""
        }

        return ChromeCookieImporter.CookieRecord(
            hostKey: hostKey,
            name: name,
            path: path,
            expiresUTC: expiresUTC,
            isSecure: isSecure,
            isHTTPOnly: isHTTPOnly,
            value: value
        )
    }
}
#endif
```

#### 1.3 Remove macOS-only Restrictions

**File:** `Sources/CodexBarCore/Providers/Cursor/CursorStatusProbe.swift`

Find the `#else` block around line 615-625 and remove it or add Linux support:

```swift
// Remove this macOS-only guard
#if os(macOS)
// ... existing code ...
#else
// DELETE THIS SECTION - replace with Linux cookie support
public enum CursorStatusProbeError: LocalizedError, Sendable {
    case notSupported
    public var errorDescription: String? {
        "Cursor is only supported on macOS."
    }
}
#endif

// Replace with unified implementation
```

Same for **Factory**: `Sources/CodexBarCore/Providers/Factory/FactoryStatusProbe.swift` around line 1065-1072.

---

## Task 2: Antigravity Language Server Detection

**Priority:** MEDIUM - Would be nice to have

### Current Issue

Antigravity is running but not exposing the required `--extension_server_port` argument that the probe looks for.

### Investigation Needed

1. Check Antigravity Linux binary for alternative port detection:
   ```bash
   ps aux | grep antigravity | head -1 | awk '{print /proc/$1/cmdline}'
   ```

2. Look for WebSocket or HTTP ports being used:
   ```bash
   lsof -iTCP -sTCP:LISTEN -p <antigravity_pid>
   ```

3. Check Antigravity config for API settings:
   ```bash
   ~/.config/antigravity/
   ~/.antigravity/
   ```

### Possible Solutions

**Option A:** Find the correct port and update probe
**Option B:** Antigravity Linux may not support the API → mark as unsupported
**Option C:** Use Antigravity CLI if available (like `antigravity --status`)

---

## Task 3: Testing and Verification

### Test Cookie Decryption

```bash
# After implementing Chrome cookie support:
usagebar usage --provider cursor --source web
usagebar usage --provider factory --source web
```

### Test Antigravity

```bash
# After fixing detection:
usagebar usage --provider antigravity
```

---

## Implementation Order for Opus

1. **Create branch:** `feature/linux-chrome-cookies`
2. **Implement SQLiteCookieReader.swift** for Linux
3. **Add Linux getChromeEncryptionKey()** to ChromeCookieImporter.swift
4. **Test with Cursor provider**
5. **Remove macOS-only guards** from Cursor and Factory
6. **Test with Factory provider**
7. **Investigate and fix Antigravity** (or document as unsupported)
8. **Update Package.swift** to add SQLite dependency if needed
9. **Full test suite:** `usagebar usage --provider all`
10. **Update README.md** with Chrome cookie setup instructions

---

## Files to Modify

1. `Sources/CodexBarCore/Host/Cookies/ChromeCookieImporter.swift` - Add Linux support
2. `Sources/CodexBarCore/Host/Cookies/FirefoxCookieImporter.swift` - Add Linux support (similar approach)
3. `Sources/CodexBarCore/Providers/Cursor/CursorStatusProbe.swift` - Remove macOS guard
4. `Sources/CodexBarCore/Providers/Factory/FactoryStatusProbe.swift` - Remove macOS guard
5. `Package.swift` - Add SQLite dependency
6. `README.md` - Document Chrome cookie requirements

---

## Dependencies to Add

**Package.swift:**

```swift
.dependencies: [
    // ... existing ...
    .package(url: "https://github.com/stephencelis/SQLite.swift", from: "0.15.3"),
],
targets: [
    .target(
        name: "CodexBarCore",
        dependencies: [
            // ... existing ...
            .product(name: "SQLite", package: "SQLite.swift"),
        ]
    ),
]
```

---

## Notes

- Chrome on Linux may store cookies **in plaintext** on some systems (much easier!)
- On systems with GNOME Keyring, use `libsecret` via C interop
- Consider supporting Firefox too (SQLite, no encryption usually)
- Antigravity may require a different approach entirely (CLI, config file, or mark unsupported)

---

## Estimated Complexity

- Chrome Cookie Decryption: **4-6 hours** (SQLite + encryption + testing)
- Cursor Provider: **1 hour** (mostly removing guards, using cookies)
- Factory Provider: **1 hour** (same as Cursor)
- Antigravity: **2-4 hours** (investigation + implementation) OR **30 mins** to document as unsupported

**Total:** ~8-12 hours for full implementation

---

## Quick Win Alternative

If full Chrome cookie decryption is too complex:

**Alternative:** Use API tokens instead (like we did for z.ai)

- Cursor may have an API
- Factory may have an API
- Much simpler than cookie decryption
- More reliable across different Linux setups

Consider checking:
- Cursor Settings → Developer → API Token
- Factory Settings → API Key
