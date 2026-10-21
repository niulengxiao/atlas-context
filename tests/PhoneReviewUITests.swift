import XCTest

final class PhoneReviewUITests: XCTestCase {
    override func setUp() { continueAfterFailure = false }
    func testDefaultExportIsDisabled() {
        let app = XCUIApplication()
        app.launch()
        let review = app.buttons["review-export"]
        for _ in 0..<8 where !review.isHittable { app.swipeUp() }
        XCTAssertFalse(review.isEnabled)
        XCTAssertEqual(app.switches["allow-cloud"].value as? String, "0")
    }

    func testSelectionAndExactReviewRequiredBeforeExport() {
        let app = XCUIApplication()
        app.launch()
        let selection = app.switches["include-record"].firstMatch
        XCTAssertTrue(selection.waitForExistence(timeout: 10))
        XCTAssertEqual(selection.value as? String, "0")
        selection.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap()
        XCTAssertEqual(selection.value as? String, "1")

        let review = app.buttons["review-export"]
        for _ in 0..<8 where !review.isHittable { app.swipeUp() }
        XCTAssertEqual(app.switches["allow-cloud"].value as? String, "0")
        XCTAssertTrue(review.isEnabled)
        review.tap()

        let save = app.buttons["save-export"]
        XCTAssertTrue(save.waitForExistence(timeout: 5))
        for _ in 0..<5 where !save.isHittable { app.swipeUp() }
        XCTAssertFalse(save.isEnabled)
        XCTAssertTrue(app.staticTexts.containing(NSPredicate(format: "label CONTAINS %@", "local_only")).firstMatch.exists)
        let payload = app.staticTexts.containing(NSPredicate(format: "label CONTAINS %@", "atlas-context.phone")).firstMatch.label
        XCTAssertTrue(payload.contains("learning photography"))
        XCTAssertFalse(payload.contains("community garden"))
        XCTAssertFalse(payload.contains("short trip"))
        let acknowledgment = app.switches["acknowledge-export"]
        acknowledgment.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap()
        XCTAssertEqual(acknowledgment.value as? String, "1")
        XCTAssertTrue(save.isEnabled)
        save.tap()
        // System file picker must open only after both explicit decisions.
        XCTAssertTrue(app.navigationBars["Move"].waitForExistence(timeout: 3)
                      || app.buttons["Save"].exists || app.buttons["Export"].exists)
    }
}
