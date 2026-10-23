import Foundation
import ImageIO
import UniformTypeIdentifiers
import Vision

struct LocalPhotoAnalysis: Sendable {
    let clue: PhotoClue
    let preview: Data
}

// No network client, OCR, face recognition, library enumeration or persistence.
// The system picker may itself download a selected iCloud photo from Apple.
actor LocalPhotoAnalyzer {
    func analyze(_ data: Data) throws -> LocalPhotoAnalysis {
        guard data.count <= 20_000_000,
              let source = CGImageSourceCreateWithData(data as CFData, [kCGImageSourceShouldCache: false] as CFDictionary),
              let image = CGImageSourceCreateThumbnailAtIndex(source, 0, [
                kCGImageSourceCreateThumbnailFromImageAlways: true,
                kCGImageSourceCreateThumbnailWithTransform: true,
                kCGImageSourceThumbnailMaxPixelSize: 1024
              ] as CFDictionary) else { throw PhoneExportError.invalidSelection }
        try Task.checkCancellation()
        let request = VNClassifyImageRequest()
        // If Vision is unavailable, keep the photo usable with a neutral question.
        // Never substitute a remote classifier or invent a scene.
        let classified = (try? VNImageRequestHandler(cgImage: image, options: [:]).perform([request])) != nil
        try Task.checkCancellation()
        let labels = (classified ? request.results ?? [] : []).prefix(20).map { ($0.identifier, $0.confidence) }
        // Encode pixels only for an in-memory preview; do not copy source metadata.
        let preview = NSMutableData()
        guard let output = CGImageDestinationCreateWithData(preview, UTType.jpeg.identifier as CFString, 1, nil) else {
            throw PhoneExportError.invalidSelection
        }
        CGImageDestinationAddImage(output, image, [kCGImageDestinationLossyCompressionQuality: 0.7] as CFDictionary)
        guard CGImageDestinationFinalize(output) else { throw PhoneExportError.invalidSelection }
        return LocalPhotoAnalysis(clue: PhotoClue.suggested(by: labels), preview: preview as Data)
    }
}
