import Foundation

// Run alongside mobile/PhoneBundle.swift. The resulting file is fictional.
@main
struct PhoneContractCheck {
    static func main() throws {
        let records = [
            PhoneRecord(text: "In 2023, I began learning photography in Harbor City.", attribution: "user_statement", period: "2023"),
            PhoneRecord(text: "A short trip may have happened in 2024.", attribution: "inferred", period: "2024")
        ]
        let bundle = try PhoneBundle(records: records, purpose: "life_reflection", allowCloud: false)
        let data = try bundle.encoded()
        let object = try JSONSerialization.jsonObject(with: data) as! [String: Any]
        precondition(object["disclosure"] as? String == "local_only")
        precondition((object["records"] as? [[String: Any]])?.count == 2)
        precondition(!String(decoding: data, as: UTF8.self).contains("source_ref"))
        for invalid in [PhoneRecord(text: "", attribution: "recorded"),
                        PhoneRecord(text: "Text", attribution: "verified_truth"),
                        PhoneRecord(text: "Text", attribution: "recorded", period: "2024-13"),
                        PhoneRecord(text: String(repeating: "a", count: 2001), attribution: "recorded")] {
            do {
                _ = try PhoneBundle(records: [invalid], purpose: "life_reflection", allowCloud: false)
                fatalError("Invalid export accepted")
            } catch PhoneExportError.invalidSelection { }
        }
        if CommandLine.arguments.count > 1 {
            try data.write(to: URL(fileURLWithPath: CommandLine.arguments[1]), options: [.withoutOverwriting, .completeFileProtection])
        }
        print("Swift phone contract checks passed; fictional export only.")
    }
}
