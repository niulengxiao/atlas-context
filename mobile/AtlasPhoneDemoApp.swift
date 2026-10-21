import SwiftUI

@main
struct AtlasPhoneDemoApp: App {
    var body: some Scene {
        WindowGroup {
            NavigationStack {
                VStack(spacing: 0) {
                    Text("SYNTHETIC DEMO · FICTIONAL RECORDS")
                        .font(.caption.bold()).padding(10).frame(maxWidth: .infinity)
                        .background(.yellow.opacity(0.2))
                    AtlasContextExportView(candidates: [
                        PhoneCandidate(record: PhoneRecord(text: "In 2023, I began learning photography in Harbor City.", attribution: "user_statement", period: "2023", city: "Harbor City")),
                        PhoneCandidate(record: PhoneRecord(text: "In 2024, I helped at a fictional community garden.", attribution: "user_statement", period: "2024")),
                        PhoneCandidate(record: PhoneRecord(text: "In 2025, I put together a small photography portfolio.", attribution: "user_statement", period: "2025")),
                        PhoneCandidate(record: PhoneRecord(text: "A short trip may have happened in 2024.", attribution: "inferred", period: "2024"))
                    ])
                }
            }
        }
    }
}
