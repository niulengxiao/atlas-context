import Foundation

// A projection of reviewed text, never a photo-library or backup model.
struct PhoneRecord: Codable, Equatable, Sendable {
    var text: String
    let attribution: String
    var period: String? = nil
    var city: String? = nil
    var evidence_label: String? = nil
}

struct PhoneBundle: Encodable, Sendable {
    let format = "atlas-context.phone"
    let schema_version = 1
    let bundle_id: String
    let created_at: String
    let expires_at: String
    let purpose: String
    let disclosure: String
    let records: [PhoneRecord]

    init(records: [PhoneRecord], purpose: String, allowCloud: Bool, lifetime: TimeInterval = 3600, now: Date = .now) throws {
        guard (1...50).contains(records.count), (60...86400).contains(lifetime),
              ["life_reflection", "short_bio", "year_review"].contains(purpose),
              records.reduce(0, { $0 + $1.text.unicodeScalars.count }) <= 20_000 else {
            throw PhoneExportError.invalidSelection
        }
        for record in records {
            guard !record.text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty,
                  record.text.unicodeScalars.count <= 2000,
                  ["recorded", "user_statement", "inferred"].contains(record.attribution),
                  (record.city?.unicodeScalars.count ?? 0) <= 100,
                  (record.evidence_label?.unicodeScalars.count ?? 0) <= 100 else {
                throw PhoneExportError.invalidSelection
            }
            if let period = record.period {
                let parts = period.split(separator: "-", omittingEmptySubsequences: false)
                guard period.range(of: #"^[0-9]{4}(-[0-9]{2})?$"#, options: .regularExpression) != nil,
                      let year = Int(parts[0]), year > 0,
                      parts.count == 1 || (1...12).contains(Int(parts[1]) ?? 0) else {
                    throw PhoneExportError.invalidSelection
                }
            }
        }
        let dates = ISO8601DateFormatter()
        bundle_id = UUID().uuidString.lowercased()
        created_at = dates.string(from: now)
        expires_at = dates.string(from: now.addingTimeInterval(lifetime))
        self.purpose = purpose
        disclosure = allowCloud ? "cloud_allowed" : "local_only"
        self.records = records
    }

    func encoded() throws -> Data {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes]
        let data = try encoder.encode(self)
        guard data.count <= 256_000 else { throw PhoneExportError.invalidSelection }
        return data
    }
}

enum PhoneExportError: Error {
    case invalidSelection
}
