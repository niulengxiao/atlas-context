"""Run the fictional companion's UI checks on a newly created simulator only."""
import argparse
import json
from pathlib import Path
import subprocess


def run(project, results, derived):
    for path in (results, derived):
        if Path(path).exists():
            raise FileExistsError("Use new test output paths")
    runtimes = json.loads(subprocess.check_output(["xcrun", "simctl", "list", "runtimes", "-j"]))["runtimes"]
    supported = [r for r in runtimes if r.get("isAvailable") and r["identifier"].startswith("com.apple.CoreSimulator.SimRuntime.iOS-")
                 and tuple(int(part) for part in r["version"].split(".")) >= (18,)]
    # Exercise the oldest installed supported iOS, avoiding an unrelated preview
    # runtime when a stable baseline is also installed on a developer machine.
    runtime = min(supported, key=lambda r: tuple(int(part) for part in r["version"].split(".")))
    device = subprocess.check_output(["xcrun", "simctl", "create", "Atlas Context Fictional UI",
                                      "com.apple.CoreSimulator.SimDeviceType.iPhone-16", runtime["identifier"]], text=True).strip()
    try:
        print("Running fictional UI checks on iOS " + runtime["version"], flush=True)
        subprocess.run(["xcodebuild", "-quiet", "-project", str(Path(project).resolve()), "-scheme", "AtlasPhoneDemo",
                        "-destination", "platform=iOS Simulator,id=" + device, "-derivedDataPath", str(Path(derived).resolve()),
                        "-resultBundlePath", str(Path(results).resolve()), "-parallel-testing-enabled", "NO",
                        "-collect-test-diagnostics", "never",
                        "-test-timeouts-enabled", "YES", "-maximum-test-execution-time-allowance", "120",
                        "CODE_SIGNING_ALLOWED=NO", "test"], check=True, timeout=1200)
    finally:
        if (Path(results) / "Info.plist").exists():
            # Only fixed fictional app content is exercised. Print precise
            # failures without uploading a simulator archive or account logs.
            subprocess.run(["xcrun", "xcresulttool", "get", "test-results", "summary", "--path", str(results), "--format", "json"])
        # This script owns this new simulator; never shut down a user's device.
        subprocess.run(["xcrun", "simctl", "shutdown", device], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["xcrun", "simctl", "delete", device], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--results", required=True)
    parser.add_argument("--derived-data", required=True)
    args = parser.parse_args()
    run(args.project, args.results, args.derived_data)
