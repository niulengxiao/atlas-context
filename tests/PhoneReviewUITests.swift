import XCTest

@MainActor
final class PhoneReviewUITests: XCTestCase {
    override func setUp() { continueAfterFailure = false }

    private func reveal(_ element: XCUIElement, in app: XCUIApplication, towardTop: Bool = false,
                        file: StaticString = #filePath, line: UInt = #line) {
        // isHittable alone can be true beneath a navigation bar or sheet edge.
        // Keep the complete target inside a safe visible band before tapping.
        for _ in 0..<12 {
            if element.exists {
                let frame = element.frame
                if element.isHittable && frame.minY >= 150 && frame.maxY <= app.frame.maxY - 35 { return }
                scroll(in: app, towardTop: frame.minY < 150)
            } else { scroll(in: app, towardTop: towardTop) }
        }
        XCTFail("Target did not enter the visible interaction area: \(element), frame: \(element.frame)", file: file, line: line)
    }

    private func scroll(in app: XCUIApplication, towardTop: Bool) {
        // Drag the form gutter so a TextEditor cannot consume the scroll.
        let upper = app.coordinate(withNormalizedOffset: CGVector(dx: 0.97, dy: 0.35))
        let lower = app.coordinate(withNormalizedOffset: CGVector(dx: 0.97, dy: 0.75))
        (towardTop ? upper : lower).press(forDuration: 0.01, thenDragTo: towardTop ? lower : upper)
    }

    func testDefaultExportIsDisabled() {
        let app = XCUIApplication()
        app.launchArguments = ["--export-fixture"]
        app.launch()
        let review = app.buttons["review-export"]
        reveal(review, in: app)
        XCTAssertFalse(review.isEnabled)
        reveal(app.switches["allow-cloud"], in: app, towardTop: true)
        XCTAssertEqual(app.switches["allow-cloud"].value as? String, "0")
    }

    func testSelectionAndExactReviewRequiredBeforeExport() {
        let app = XCUIApplication()
        app.launchArguments = ["--export-fixture"]
        app.launch()
        let selection = app.switches["include-record"].firstMatch
        XCTAssertTrue(selection.waitForExistence(timeout: 10))
        reveal(selection, in: app)
        XCTAssertEqual(selection.value as? String, "0")
        selection.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap()
        XCTAssertEqual(selection.value as? String, "1")

        let review = app.buttons["review-export"]
        reveal(review, in: app)
        reveal(app.switches["allow-cloud"], in: app, towardTop: true)
        XCTAssertEqual(app.switches["allow-cloud"].value as? String, "0")
        reveal(review, in: app)
        XCTAssertTrue(review.isEnabled)
        review.tap()
        XCTAssertTrue(app.navigationBars["Review before export"].waitForExistence(timeout: 5))

        let outgoing = app.staticTexts.containing(NSPredicate(format: "label CONTAINS %@", "atlas-context.phone")).firstMatch
        XCTAssertTrue(outgoing.waitForExistence(timeout: 5))
        let payload = outgoing.label
        XCTAssertTrue(payload.contains("local_only"))
        XCTAssertTrue(payload.contains("learning photography"))
        XCTAssertFalse(payload.contains("community garden"))
        XCTAssertFalse(payload.contains("short trip"))
        let save = app.buttons["save-export"]
        reveal(save, in: app)
        XCTAssertFalse(save.isEnabled)
        let acknowledgment = app.switches["acknowledge-export"]
        reveal(acknowledgment, in: app, towardTop: true)
        acknowledgment.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap()
        XCTAssertEqual(acknowledgment.value as? String, "1")
        reveal(save, in: app)
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
        reveal(share, in: app)
        XCTAssertFalse(share.isEnabled)
        let confirm = app.buttons["confirm-reflection-0"]
        reveal(confirm, in: app, towardTop: true)
        confirm.tap()
        let confirmed = XCTNSPredicateExpectation(predicate: NSPredicate(format: "label == %@", "Wording confirmed"), object: confirm)
        XCTAssertEqual(XCTWaiter.wait(for: [confirmed], timeout: 5), .completed)
        reveal(share, in: app)
        XCTAssertTrue(share.isEnabled)
        share.tap()
        let selected = app.switches["include-record"].firstMatch
        XCTAssertTrue(selected.waitForExistence(timeout: 5))
        reveal(selected, in: app)
        XCTAssertEqual(selected.value as? String, "0")
        selected.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap()
        let review = app.buttons["review-export"]
        reveal(review, in: app)
        reveal(app.switches["allow-cloud"], in: app, towardTop: true)
        XCTAssertEqual(app.switches["allow-cloud"].value as? String, "0")
        reveal(review, in: app)
        review.tap()
        let payload = app.staticTexts.containing(NSPredicate(format: "label CONTAINS %@", "atlas-context.phone")).firstMatch
        XCTAssertTrue(payload.waitForExistence(timeout: 5))
        XCTAssertTrue(payload.label.contains("personal_assistance"))
        XCTAssertTrue(payload.label.contains("quiet outdoor walks"))
        XCTAssertFalse(payload.label.contains("café")) // The second explanation was not confirmed.
        XCTAssertFalse(payload.label.contains("clue"))
        let save = app.buttons["save-export"]
        reveal(save, in: app)
        XCTAssertTrue(save.exists)
        XCTAssertFalse(save.isEnabled)
    }

    func testClearSessionRemovesConfirmedContext() {
        let app = XCUIApplication()
        app.launch()
        app.buttons["try-fictional"].tap()
        let confirm = app.buttons["confirm-reflection-0"]
        reveal(confirm, in: app)
        confirm.tap()
        let clear = app.buttons["clear-reflections"]
        reveal(clear, in: app)
        clear.tap()
        XCTAssertFalse(app.buttons["share-reflections"].isEnabled)
        XCTAssertFalse(app.textViews["reflection-text"].exists)
        XCTAssertFalse(app.staticTexts["fictional-banner"].exists)
    }
}
