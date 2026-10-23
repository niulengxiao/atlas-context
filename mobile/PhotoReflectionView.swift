import SwiftUI
import PhotosUI

struct PhotoReflectionView: View {
    @State private var selection: [PhotosPickerItem] = []
    @State private var reflections: [PhotoReflection] = []
    @State private var previews: [UUID: Data] = [:]
    @State private var fictional = false
    @State private var loading = false
    @State private var loadGeneration = UUID()
    @State private var status: String?
    @State private var export: ReflectionExport?
    private let analyzer = LocalPhotoAnalyzer()

    private var confirmed: [PhoneRecord] { reflections.compactMap(\.reviewedRecord) }

    var body: some View {
        Form {
            Section {
                Text("Help your agent understand what matters to you").font(.headline)
                Text("A photo is a clue. Your explanation gives it meaning. Confirm your own words before choosing what to share.")
                Text("This app classifies a few scenes on device. It cannot reconstruct your life or determine your personality.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            Section("1 · Choose a starting point") {
                PhotosPicker(selection: $selection, maxSelectionCount: 5, matching: .images) {
                    Label("Choose up to 5 photos", systemImage: "photo.on.rectangle")
                }
                .accessibilityIdentifier("choose-photos")
                .disabled(loading)
                Button("Try fictional walk-through") {
                    selection = []
                    previews = [:]
                    reflections = PhotoReflection.fictional
                    fictional = true
                    status = nil
                }
                .accessibilityIdentifier("try-fictional")
                .disabled(loading)
                Text("Only your selection is read. No full-library permission, background scan or model upload. Apple's picker may download a selected iCloud photo. Images stay in memory; only text you approve can be exported.")
                    .font(.footnote).foregroundStyle(.secondary)
                if loading { ProgressView("Reading selected photos locally…") }
                if let status { Text(status).font(.footnote) }
            }
            if fictional {
                Section { Text("FICTIONAL EXAMPLE · edit the sample explanations before confirming")
                    .font(.caption.bold()).accessibilityIdentifier("fictional-banner") }
            }
            ForEach($reflections) { $reflection in
                Section("2 · Explain photo \((reflections.firstIndex(where: { $0.id == reflection.id }) ?? 0) + 1)") {
                    if let data = previews[reflection.id], let image = UIImage(data: data) {
                        Image(uiImage: image).resizable().scaledToFit().frame(maxHeight: 180)
                            .accessibilityLabel("Selected photo preview · stays on this device")
                    }
                    Text(reflection.clue.question).font(.callout)
                    Text("This question is tentative. Correct it, skip it, or describe what the scene actually meant.")
                        .font(.caption).foregroundStyle(.secondary)
                    TextEditor(text: $reflection.statement).frame(minHeight: 100)
                        .accessibilityLabel("Your explanation")
                        .accessibilityIdentifier("reflection-text")
                    Text("\(reflection.statement.unicodeScalars.count)/2000 characters · include only details you want to share")
                        .font(.caption).foregroundStyle(.secondary)
                    Button(reflection.isConfirmed ? "Wording confirmed" : "Confirm my wording") {
                        try? reflection.confirm()
                    }
                    .disabled(!reflection.canConfirm || reflection.isConfirmed)
                    .accessibilityIdentifier("confirm-reflection")
                    if reflection.isConfirmed {
                        Text("Confirmed as your statement, not an independently verified fact. Editing clears confirmation.")
                            .font(.caption).foregroundStyle(.secondary)
                    }
                }
            }
            Section("3 · Review what your agent may receive") {
                Button("Choose text to share · \(confirmed.count) confirmed") {
                    export = ReflectionExport(records: confirmed)
                }
                .disabled(confirmed.isEmpty || loading)
                .accessibilityIdentifier("share-reflections")
                Text("Confirmation does not share anything. The next screen starts with nothing selected and cloud use off. It shows the exact outgoing JSON before saving.")
                    .font(.footnote).foregroundStyle(.secondary)
                Button("Clear this session", role: .destructive) {
                    loadGeneration = UUID()
                    selection = []; reflections = []; previews = [:]; fictional = false; status = nil; loading = false
                }.accessibilityIdentifier("clear-reflections")
            }
        }
        .navigationTitle(fictional ? "Fictional walk-through" : "Photos to understanding")
        .task(id: selection) {
            guard !selection.isEmpty else { return }
            let generation = UUID()
            loadGeneration = generation
            // Replacing a selection also removes every prior explanation/confirmation.
            reflections = []; previews = [:]; fictional = false; status = nil; loading = true
            defer { if loadGeneration == generation { loading = false } }
            var failures = 0
            for item in selection {
                do {
                    try Task.checkCancellation()
                    guard let data = try await item.loadTransferable(type: Data.self) else { throw PhoneExportError.invalidSelection }
                    guard loadGeneration == generation && !Task.isCancelled else { return }
                    let result = try await analyzer.analyze(data)
                    try Task.checkCancellation()
                    guard loadGeneration == generation else { return }
                    let reflection = PhotoReflection(clue: result.clue)
                    previews[reflection.id] = result.preview
                    reflections.append(reflection)
                } catch is CancellationError { return }
                catch { failures += 1 }
            }
            if loadGeneration == generation && !Task.isCancelled && failures > 0 { status = "\(failures) selected image(s) could not be read (20 MB per image limit). Nothing was uploaded. Try another image or the fictional example." }
        }
        .sheet(item: $export) { item in
            NavigationStack {
                AtlasContextExportView(candidates: item.records.map { PhoneCandidate(record: $0) }, purpose: "personal_assistance")
                    .toolbar { ToolbarItem(placement: .cancellationAction) { Button("Back") { export = nil } } }
            }
        }
    }
}

private struct ReflectionExport: Identifiable {
    let id = UUID()
    let records: [PhoneRecord]
}
