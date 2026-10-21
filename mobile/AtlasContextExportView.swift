import SwiftUI
import UniformTypeIdentifiers

struct PhoneCandidate: Identifiable {
    let id = UUID() // Local UI identity only; not serialized.
    var record: PhoneRecord
    var selected = false
    var includePeriod = false
    var includeCity = false
}

struct AtlasContextExportView: View {
    @State var candidates: [PhoneCandidate]
    @State private var purpose = "life_reflection"
    @State private var allowCloud = false
    @State private var review: ExportReview?
    @State private var showingError = false

    private var selectedCount: Int { candidates.filter(\.selected).count }

    var body: some View {
        Form {
            Section {
                Label("You decide what leaves your phone", systemImage: "lock.shield")
                    .font(.headline)
                Text("Only selected, reviewed text is exported. No original photos, videos, GPS coordinates, photo IDs or full backup are included.")
                Text("Sentences can still identify you. Remove names, addresses and other details you do not want to share.")
                    .foregroundStyle(.secondary)
            }
            Section("Choose records · nothing selected by default") {
                ForEach($candidates) { $candidate in
                    VStack(alignment: .leading, spacing: 10) {
                        Toggle("Include this record", isOn: $candidate.selected)
                            .accessibilityIdentifier("include-record")
                        Text(candidate.record.attribution == "inferred" ? "System inference · excluded from default Agent retrieval" : "Source: \(candidate.record.attribution)")
                            .font(.caption).foregroundStyle(.secondary)
                        TextEditor(text: $candidate.record.text)
                            .frame(minHeight: 85)
                            .accessibilityLabel("Exact outgoing wording")
                        Text("\(candidate.record.text.unicodeScalars.count)/2000 characters")
                            .font(.caption).foregroundStyle(.secondary)
                        if let period = candidate.record.period {
                            Toggle("Include period: \(period)", isOn: $candidate.includePeriod)
                        }
                        if let city = candidate.record.city {
                            Toggle("Include city: \(city)", isOn: $candidate.includeCity)
                        }
                    }.padding(.vertical, 6)
                }
            }
            Section("Task and disclosure") {
                Picker("Purpose", selection: $purpose) {
                    Text("Life reflection").tag("life_reflection")
                    Text("Short biography").tag("short_bio")
                    Text("Year review").tag("year_review")
                }
                Text("Export expires one hour after you open the review. A copied file remains readable after expiry; expiry limits future access through Atlas Context.")
                Toggle("Allow a cloud Agent to receive this text", isOn: $allowCloud)
                    .accessibilityIdentifier("allow-cloud")
                Text(allowCloud ? "Cloud use sends the approved text to your model provider. Review its retention policy. Desktop opt-in is also required." : "Local use only. Use a local model and a host that respects this setting. The file format cannot block another app from uploading a copied file.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            Section {
                Button("Review exact export · \(selectedCount) records") { prepareReview() }
                    .disabled(!(1...50).contains(selectedCount))
                    .accessibilityIdentifier("review-export")
                Text("Choose On My iPhone to save locally, then AirDrop the JSON to your computer. Choosing iCloud or another file provider sends it to that provider. Connecting USB alone grants no Agent access.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
        }
        .navigationTitle("Agent context")
        .sheet(item: $review) { item in
            PhoneExportReview(bundle: item.bundle, data: item.data)
        }
        .alert("Cannot prepare export", isPresented: $showingError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text("Select 1–50 records, keep each text within 2,000 characters and the total within 20,000. Review period and label lengths.")
        }
    }

    private func prepareReview() {
        do {
            let records = candidates.filter(\.selected).map { candidate in
                PhoneRecord(text: candidate.record.text, attribution: candidate.record.attribution,
                            period: candidate.includePeriod ? candidate.record.period : nil,
                            city: candidate.includeCity ? candidate.record.city : nil,
                            evidence_label: nil)
            }
            let bundle = try PhoneBundle(records: records, purpose: purpose, allowCloud: allowCloud)
            review = ExportReview(bundle: bundle, data: try bundle.encoded())
        } catch { showingError = true }
    }
}

private struct ExportReview: Identifiable {
    let id = UUID()
    let bundle: PhoneBundle
    let data: Data
}

private struct ContextDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.json] }
    var data: Data
    init(data: Data) { self.data = data }
    init(configuration: ReadConfiguration) throws {
        data = configuration.file.regularFileContents ?? Data()
    }
    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        FileWrapper(regularFileWithContents: data)
    }
}

private struct PhoneExportReview: View {
    let bundle: PhoneBundle
    let data: Data
    @State private var acknowledged = false
    @State private var exporting = false
    @State private var resultMessage: String?
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section("Everything in the outgoing file") {
                    Text(String(decoding: data, as: UTF8.self))
                        .font(.caption.monospaced()).textSelection(.enabled)
                }
                Section("Privacy before export") {
                    Text("Mode: \(bundle.disclosure). Expires: \(bundle.expires_at).")
                    Text("This JSON is not encrypted. Anyone with a copy can read it. Deleting it or revoking desktop access cannot recall earlier copies or model responses.")
                    Toggle("I reviewed every outgoing sentence and field", isOn: $acknowledged)
                        .accessibilityIdentifier("acknowledge-export")
                    Button("Save reviewed JSON") { exporting = true }
                        .disabled(!acknowledged)
                        .accessibilityIdentifier("save-export")
                    if let resultMessage { Text(resultMessage).font(.footnote) }
                }
            }
            .navigationTitle("Review before export")
            .toolbar { Button("Close") { dismiss() } }
            .fileExporter(isPresented: $exporting, document: ContextDocument(data: data), contentType: .json,
                          defaultFilename: "atlas-context-export") { result in
                switch result {
                case .success: resultMessage = "Saved to your selected file provider. Transfer this file to your trusted computer."
                case .failure: resultMessage = "Export did not complete. No Agent connection was created."
                }
            }
        }
    }
}
