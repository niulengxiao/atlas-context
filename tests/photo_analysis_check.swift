import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

// Procedural pixels and invented metadata only; never opens a user's library.
@main
struct PhotoAnalysisCheck {
    static func main() async throws {
        let canvas = CGContext(data: nil, width: 160, height: 160, bitsPerComponent: 8,
                               bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(),
                               bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
        canvas.setFillColor(CGColor(red: 0.2, green: 0.6, blue: 0.4, alpha: 1))
        canvas.fill(CGRect(x: 0, y: 0, width: 160, height: 160))
        let encoded = NSMutableData()
        let destination = CGImageDestinationCreateWithData(encoded, UTType.jpeg.identifier as CFString, 1, nil)!
        CGImageDestinationAddImage(destination, canvas.makeImage()!, [
            kCGImagePropertyGPSDictionary: [kCGImagePropertyGPSLatitude: 12.0, kCGImagePropertyGPSLatitudeRef: "N"],
            kCGImagePropertyExifDictionary: [kCGImagePropertyExifUserComment: "FICTIONAL_METADATA_SENTINEL"]
        ] as CFDictionary)
        precondition(CGImageDestinationFinalize(destination))
        let original = CGImageSourceCreateWithData(encoded, nil)!
        let originalProperties = CGImageSourceCopyPropertiesAtIndex(original, 0, nil)! as NSDictionary
        precondition(originalProperties[kCGImagePropertyGPSDictionary] != nil)
        let analyzer = LocalPhotoAnalyzer()
        let result = try await analyzer.analyze(encoded as Data)
        let source = CGImageSourceCreateWithData(result.preview as CFData, nil)!
        let properties = CGImageSourceCopyPropertiesAtIndex(source, 0, nil)! as NSDictionary
        precondition(properties[kCGImagePropertyGPSDictionary] == nil)
        precondition(!String(describing: properties).contains("FICTIONAL_METADATA_SENTINEL"))
        precondition(!result.preview.isEmpty && !result.clue.question.isEmpty)
        for invalid in [Data("not an image".utf8), Data(repeating: 0, count: 20_000_001)] {
            do { _ = try await analyzer.analyze(invalid); fatalError("Invalid image accepted") }
            catch PhoneExportError.invalidSelection { }
        }
        if CommandLine.arguments.count > 1 {
            try (encoded as Data).write(to: URL(fileURLWithPath: CommandLine.arguments[1]), options: .withoutOverwriting)
        }
        print("Local Vision ran on procedural pixels; preview metadata and invalid-input checks passed.")
    }
}
