import Foundation

// Run alongside PhoneBundle.swift and PhotoReflection.swift. All records are fictional.
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
        precondition(PhotoClue.suggested(by: [("face", 0.99), ("coffee", 0.1)]) == .unknown)
        precondition(PhotoClue.suggested(by: [("coffee", 0.8)]) == .food)
        var reflection = PhotoReflection(clue: .food)
        precondition(reflection.reviewedRecord == nil)
        do { try reflection.confirm(); fatalError("Blank explanation accepted") }
        catch PhoneExportError.invalidSelection { }
        reflection.statement = "These café photographs were for work, not a leisure preference."
        precondition(reflection.reviewedRecord == nil)
        try reflection.confirm()
        precondition(reflection.reviewedRecord?.attribution == "user_statement")
        reflection.statement = "These café photographs were for a work assignment. They do not mean I enjoy visiting busy cafés."
        precondition(!reflection.isConfirmed && reflection.reviewedRecord == nil)
        try reflection.confirm()
        var walk = PhotoReflection.fictional[0]
        precondition(walk.reviewedRecord == nil)
        try walk.confirm()
        let assistance = try PhoneBundle(records: [walk.reviewedRecord!, reflection.reviewedRecord!],
                                         purpose: "personal_assistance", allowCloud: false)
        let assistanceData = try assistance.encoded()
        let assistanceObject = try JSONSerialization.jsonObject(with: assistanceData) as! [String: Any]
        for item in assistanceObject["records"] as! [[String: Any]] {
            precondition(Set(item.keys) == Set(["text", "attribution"]))
        }
        // Oversized edits must invalidate a previous confirmation, too.
        reflection.statement = String(repeating: "x", count: 2001)
        precondition(!reflection.canConfirm && reflection.reviewedRecord == nil)
        if CommandLine.arguments.count > 1 {
            try data.write(to: URL(fileURLWithPath: CommandLine.arguments[1]), options: [.withoutOverwriting, .completeFileProtection])
        }
        if CommandLine.arguments.count > 2 {
            try assistanceData.write(to: URL(fileURLWithPath: CommandLine.arguments[2]), options: [.withoutOverwriting, .completeFileProtection])
        }
        print("Swift phone contract checks passed; fictional export only.")
    }
}
