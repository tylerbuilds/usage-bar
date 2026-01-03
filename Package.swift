// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "CodexBar",
    platforms: [
        .macOS(.v15),
    ],
    dependencies: [
        .package(url: "https://github.com/sparkle-project/Sparkle", from: "2.8.1"),
        .package(url: "https://github.com/steipete/Commander", from: "0.2.0"),
        .package(url: "https://github.com/apple/swift-log", from: "1.8.0"),
    ],
    targets: {
        var targets: [Target] = [
            // System library for SQLite3 on Linux
            .systemLibrary(
                name: "CSQLite3",
                pkgConfig: "sqlite3",
                providers: [
                    .apt(["libsqlite3-dev"]),
                    .brew(["sqlite3"]),
                ]),
            .target(
                name: "CodexBarCore",
                dependencies: [
                    .product(name: "Logging", package: "swift-log"),
                    .target(name: "CSQLite3", condition: .when(platforms: [.linux])),
                ],
                swiftSettings: []),
            .executableTarget(
                name: "CodexBarCLI",
                dependencies: [
                    "CodexBarCore",
                    .product(name: "Commander", package: "Commander"),
                ],
                path: "Sources/CodexBarCLI",
                swiftSettings: []),
        .testTarget(
            name: "CodexBarLinuxTests",
            dependencies: ["CodexBarCore", "CodexBarCLI"],
            path: "TestsLinux",
            swiftSettings: []),
        ]

        #if os(macOS)
        targets.append(contentsOf: [
            .executableTarget(
                name: "CodexBarClaudeWatchdog",
                dependencies: [],
                path: "Sources/CodexBarClaudeWatchdog",
                swiftSettings: []),
            .executableTarget(
                name: "CodexBar",
                dependencies: [
                    .product(name: "Sparkle", package: "Sparkle"),
                    "CodexBarCore",
                ],
                path: "Sources/CodexBar",
                exclude: [
                    "Resources",
                ],
                swiftSettings: [.define("ENABLE_SPARKLE")]),
            .executableTarget(
                name: "CodexBarWidget",
                dependencies: ["CodexBarCore"],
                path: "Sources/CodexBarWidget",
                swiftSettings: []),
            .executableTarget(
                name: "CodexBarClaudeWebProbe",
                dependencies: ["CodexBarCore"],
                path: "Sources/CodexBarClaudeWebProbe",
                swiftSettings: []),
        ])

        targets.append(.testTarget(
            name: "CodexBarTests",
            dependencies: ["CodexBar", "CodexBarCore", "CodexBarCLI"],
            path: "Tests",
            swiftSettings: []))
        #endif

        return targets
    }())
