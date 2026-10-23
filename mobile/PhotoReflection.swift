import Foundation

// Local, tentative prompts. Neither labels nor photo handles enter PhoneRecord.
enum PhotoClue: String, Sendable {
    case outdoors, food, creative, unknown

    static func suggested(by labels: [(String, Float)]) -> PhotoClue {
        let allowed: [String: PhotoClue] = [
            "park": .outdoors, "forest": .outdoors, "garden": .outdoors,
            "mountain": .outdoors, "beach": .outdoors, "outdoor": .outdoors,
            "food": .food, "coffee": .food, "cafe": .food, "restaurant": .food,
            "art": .creative, "painting": .creative, "drawing": .creative
        ]
        for (label, confidence) in labels.sorted(by: { $0.1 > $1.1 }) where confidence >= 0.3 {
            if let clue = allowed[label.lowercased()] { return clue }
        }
        return .unknown
    }

    var question: String {
        switch self {
        case .outdoors: "Possibly an outdoor scene. Was this leisure, work, or something else? What would you want an agent to remember?"
        case .food: "Possibly food or a café. Was this something you enjoyed, work, or someone else's choice? What matters to you here?"
        case .creative: "Possibly a creative activity. Were you making, learning, visiting, or working? What does this mean to you?"
        case .unknown: "What was happening here? What, if anything, would you want an agent to remember about this experience?"
        }
    }
}

struct PhotoReflection: Identifiable, Sendable {
    let id = UUID() // Temporary UI identity, never exported.
    let clue: PhotoClue
    var statement: String = "" {
        didSet { if statement != oldValue { confirmedText = nil } }
    }
    private(set) var confirmedText: String?

    var canConfirm: Bool {
        !statement.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && statement.unicodeScalars.count <= 2000
    }
    var isConfirmed: Bool { confirmedText != nil && confirmedText == statement && canConfirm }

    mutating func confirm() throws {
        guard canConfirm else { throw PhoneExportError.invalidSelection }
        confirmedText = statement
    }

    var reviewedRecord: PhoneRecord? {
        guard isConfirmed, let confirmedText else { return nil }
        return PhoneRecord(text: confirmedText, attribution: "user_statement")
    }

    static var fictional: [PhotoReflection] { [
        PhotoReflection(clue: .outdoors, statement: "On days off, I enjoy quiet outdoor walks and taking photographs. I prefer a flexible plan to a crowded schedule."),
        PhotoReflection(clue: .food, statement: "These café photographs were for a work assignment. They do not mean I enjoy visiting busy cafés.")
    ] }
}
