import Foundation

public struct ZaiSettingsReader: Sendable {
    private static let log = CodexBarLog.logger("zai-settings")

    public static let apiTokenKey = "Z_AI_API_KEY"
    private static let configPath = ".config/codexbar/config.toml"

    public static func apiToken(
        environment: [String: String] = ProcessInfo.processInfo.environment) -> String?
    {
        // Priority: 1. Environment variable, 2. Config file
        if let token = self.cleaned(environment[apiTokenKey]) { return token }

        // Try config file
        if let token = self.readTokenFromConfigFile() { return token }

        return nil
    }

    private static func readTokenFromConfigFile() -> String? {
        let home = FileManager.default.homeDirectoryForCurrentUser
        let configURL = home.appendingPathComponent(configPath)

        guard let content = try? String(contentsOf: configURL) else {
            return nil
        }

        // Simple parsing: look for zai_token = "..." or zai_api_key = "..."
        for line in content.components(separatedBy: .newlines) {
            let trimmed = line.trimmingCharacters(in: .whitespacesAndNewlines)
            if trimmed.isEmpty || trimmed.hasPrefix("[") || trimmed.hasPrefix("#") {
                continue
            }
            let parts = trimmed.components(separatedBy: "=").map { $0.trimmingCharacters(in: .whitespaces) }
            if parts.count >= 2 {
                let key = parts[0].lowercased()
                if key == "zai_token" || key == "zai_api_key" {
                    var value = parts[1...].joined(separator: "=")
                    // Remove quotes if present
                    value = value.trimmingCharacters(in: CharacterSet(charactersIn: "\"'"))
                    return value.isEmpty ? nil : value
                }
            }
        }
        return nil
    }

    static func cleaned(_ raw: String?) -> String? {
        guard var value = raw?.trimmingCharacters(in: .whitespacesAndNewlines), !value.isEmpty else {
            return nil
        }

        if (value.hasPrefix("\"") && value.hasSuffix("\"")) ||
            (value.hasPrefix("'") && value.hasSuffix("'"))
        {
            value.removeFirst()
            value.removeLast()
        }

        value = value.trimmingCharacters(in: .whitespacesAndNewlines)
        return value.isEmpty ? nil : value
    }
}

public enum ZaiSettingsError: LocalizedError, Sendable {
    case missingToken

    public var errorDescription: String? {
        switch self {
        case .missingToken:
            "z.ai API token not found. Set Z_AI_API_KEY environment variable or add to ~/.config/codexbar/config.toml"
        }
    }
}
