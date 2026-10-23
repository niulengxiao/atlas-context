import XCTest

@MainActor
final class PhoneReviewUITests: XCTestCase {
    override func setUp() { continueAfterFailure = false }
    func testDefaultExportIsDisabled() {
        let app = XCUIApplication()
        app.launchArguments = ["--export-fixture"]
        app.launch()
        let review = app.buttons["review-export"]
        for _ in 0..<8 where !review.isHittable { app.swipeUp() }
        XCTAssertFalse(review.isEnabled)
        XCTAssertEqual(app.switches["allow-cloud"].value as? String, "0")
    }

    func testSelectionAndExactReviewRequiredBeforeExport() {
        let app = XCUIApplication()
        app.launchArguments = ["--export-fixture"]
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
        XCTAssertTrue(app.buttons["DOCPicker.actionButton"].waitForExistence(timeout: 10)
                      || app.buttons["Save"].waitForExistence(timeout: 5)
                      || app.buttons["Export"].exists || app.navigationBars["Move"].exists,
                      app.debugDescription)
    }

    func testReflectionRequiresConfirmationThenSeparateDisclosure() {
        let app = XCUIApplication()
        app.launch()
        app.buttons["try-fictional"].tap()
        let share = app.buttons["share-reflections"]
        for _ in 0..<6 where !share.isHittable { app.swipeUp() }
        XCTAssertFalse(share.isEnabled)
        for _ in 0..<6 where !app.buttons["confirm-reflection"].firstMatch.isHittable { app.swipeDown() }
        app.buttons["confirm-reflection"].firstMatch.tap()
        for _ in 0..<6 where !share.isHittable { app.swipeUp() }
        XCTAssertTrue(share.isEnabled)
        share.tap()
        let selected = app.switches["include-record"].firstMatch
        XCTAssertTrue(selected.waitForExistence(timeout: 5))
        XCTAssertEqual(selected.value as? String, "0")
        selected.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap()
        let review = app.buttons["review-export"]
        for _ in 0..<8 where !review.isHittable { app.swipeUp() }
        XCTAssertEqual(app.switches["allow-cloud"].value as? String, "0")
        review.tap()
        let payload = app.staticTexts.containing(NSPredicate(format: "label CONTAINS %@", "atlas-context.phone")).firstMatch
        XCTAssertTrue(payload.waitForExistence(timeout: 5))
        XCTAssertTrue(payload.label.contains("personal_assistance"))
        XCTAssertTrue(payload.label.contains("quiet outdoor walks"))
        XCTAssertFalse(payload.label.contains("café")) // The second explanation was not confirmed.
        XCTAssertFalse(payload.label.contains("clue"))
        let save = app.buttons["save-export"]
        for _ in 0..<5 where !save.isHittable { app.swipeUp() }
        XCTAssertTrue(save.exists)
        XCTAssertFalse(save.isEnabled)
    }

    func testClearSessionRemovesConfirmedContext() {
        let app = XCUIApplication()
        app.launch()
        app.buttons["try-fictional"].tap()
        let confirm = app.buttons["confirm-reflection"].firstMatch
        for _ in 0..<6 where !confirm.isHittable { app.swipeUp() }
        confirm.tap()
        let clear = app.buttons["clear-reflections"]
        for _ in 0..<6 where !clear.isHittable { app.swipeUp() }
        clear.tap()
        XCTAssertFalse(app.buttons["share-reflections"].isEnabled)
        XCTAssertFalse(app.textViews["reflection-text"].exists)
        XCTAssertFalse(app.staticTexts["fictional-banner"].exists)
    }
}
