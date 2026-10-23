"""Create an isolated Xcode companion project; Photos are read only after picker selection."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PROJECT = r'''// !$*UTF8*$!
{
 archiveVersion = 1;
 classes = {};
 objectVersion = 56;
 objects = {
  A00000000000000000000001 = {isa = PBXProject; buildConfigurationList = A00000000000000000000009; compatibilityVersion = "Xcode 14.0"; developmentRegion = en; hasScannedForEncodings = 0; knownRegions = (en, Base); mainGroup = A00000000000000000000002; productRefGroup = A00000000000000000000003; projectDirPath = ""; projectRoot = ""; targets = (A00000000000000000000004); };
  A00000000000000000000002 = {isa = PBXGroup; children = (A00000000000000000000011, A00000000000000000000012, A00000000000000000000013, A00000000000000000000003); sourceTree = "<group>"; };
  A00000000000000000000003 = {isa = PBXGroup; children = (A00000000000000000000005); name = Products; sourceTree = "<group>"; };
  A00000000000000000000004 = {isa = PBXNativeTarget; buildConfigurationList = A0000000000000000000000A; buildPhases = (A00000000000000000000006, A00000000000000000000007, A00000000000000000000008); buildRules = (); dependencies = (); name = AtlasPhoneDemo; productName = AtlasPhoneDemo; productReference = A00000000000000000000005; productType = "com.apple.product-type.application"; };
  A00000000000000000000005 = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = AtlasPhoneDemo.app; sourceTree = BUILT_PRODUCTS_DIR; };
  A00000000000000000000006 = {isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = (A00000000000000000000021, A00000000000000000000022, A00000000000000000000023); runOnlyForDeploymentPostprocessing = 0; };
  A00000000000000000000007 = {isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; };
  A00000000000000000000008 = {isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; };
  A00000000000000000000009 = {isa = XCConfigurationList; buildConfigurations = (A00000000000000000000031, A00000000000000000000032); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release; };
  A0000000000000000000000A = {isa = XCConfigurationList; buildConfigurations = (A00000000000000000000033, A00000000000000000000034); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release; };
  A00000000000000000000011 = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = PhoneBundle.swift; sourceTree = "<group>"; };
  A00000000000000000000012 = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AtlasContextExportView.swift; sourceTree = "<group>"; };
  A00000000000000000000013 = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AtlasPhoneDemoApp.swift; sourceTree = "<group>"; };
  A00000000000000000000021 = {isa = PBXBuildFile; fileRef = A00000000000000000000011; };
  A00000000000000000000022 = {isa = PBXBuildFile; fileRef = A00000000000000000000012; };
  A00000000000000000000023 = {isa = PBXBuildFile; fileRef = A00000000000000000000013; };
  A00000000000000000000031 = {isa = XCBuildConfiguration; buildSettings = {SDKROOT = iphoneos; IPHONEOS_DEPLOYMENT_TARGET = 18.0; CLANG_ENABLE_MODULES = YES; }; name = Debug; };
  A00000000000000000000032 = {isa = XCBuildConfiguration; buildSettings = {SDKROOT = iphoneos; IPHONEOS_DEPLOYMENT_TARGET = 18.0; CLANG_ENABLE_MODULES = YES; }; name = Release; };
  A00000000000000000000033 = {isa = XCBuildConfiguration; buildSettings = {GENERATE_INFOPLIST_FILE = YES; INFOPLIST_KEY_CFBundleDisplayName = "Atlas Phone Demo"; INFOPLIST_KEY_UILaunchScreen_Generation = YES; INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES; PRODUCT_BUNDLE_IDENTIFIER = org.atlascontext.phone.demo; PRODUCT_NAME = "$(TARGET_NAME)"; SWIFT_VERSION = 6.0; SWIFT_OPTIMIZATION_LEVEL = "-Onone"; TARGETED_DEVICE_FAMILY = "1,2"; CODE_SIGN_STYLE = Automatic; }; name = Debug; };
  A00000000000000000000034 = {isa = XCBuildConfiguration; buildSettings = {GENERATE_INFOPLIST_FILE = YES; INFOPLIST_KEY_CFBundleDisplayName = "Atlas Phone Demo"; INFOPLIST_KEY_UILaunchScreen_Generation = YES; INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES; PRODUCT_BUNDLE_IDENTIFIER = org.atlascontext.phone.demo; PRODUCT_NAME = "$(TARGET_NAME)"; SWIFT_VERSION = 6.0; TARGETED_DEVICE_FAMILY = "1,2"; CODE_SIGN_STYLE = Automatic; }; name = Release; };
 };
 rootObject = A00000000000000000000001;
}
'''

UI_TEST_OBJECTS = r'''
  A00000000000000000000041 = {isa = PBXNativeTarget; buildConfigurationList = A00000000000000000000048; buildPhases = (A00000000000000000000045, A00000000000000000000046, A00000000000000000000047); buildRules = (); dependencies = (A0000000000000000000004B); name = AtlasPhoneDemoUITests; productName = AtlasPhoneDemoUITests; productReference = A00000000000000000000042; productType = "com.apple.product-type.bundle.ui-testing"; };
  A00000000000000000000042 = {isa = PBXFileReference; explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = AtlasPhoneDemoUITests.xctest; sourceTree = BUILT_PRODUCTS_DIR; };
  A00000000000000000000043 = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = PhoneReviewUITests.swift; sourceTree = "<group>"; };
  A00000000000000000000044 = {isa = PBXBuildFile; fileRef = A00000000000000000000043; };
  A00000000000000000000045 = {isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = (A00000000000000000000044); runOnlyForDeploymentPostprocessing = 0; };
  A00000000000000000000046 = {isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; };
  A00000000000000000000047 = {isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; };
  A00000000000000000000048 = {isa = XCConfigurationList; buildConfigurations = (A00000000000000000000049, A0000000000000000000004A); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release; };
  A00000000000000000000049 = {isa = XCBuildConfiguration; buildSettings = {GENERATE_INFOPLIST_FILE = YES; PRODUCT_BUNDLE_IDENTIFIER = org.atlascontext.phone.demo.uitests; PRODUCT_NAME = "$(TARGET_NAME)"; SWIFT_VERSION = 6.0; TEST_TARGET_NAME = AtlasPhoneDemo; TARGETED_DEVICE_FAMILY = "1,2"; CODE_SIGN_STYLE = Automatic; }; name = Debug; };
  A0000000000000000000004A = {isa = XCBuildConfiguration; buildSettings = {GENERATE_INFOPLIST_FILE = YES; PRODUCT_BUNDLE_IDENTIFIER = org.atlascontext.phone.demo.uitests; PRODUCT_NAME = "$(TARGET_NAME)"; SWIFT_VERSION = 6.0; TEST_TARGET_NAME = AtlasPhoneDemo; TARGETED_DEVICE_FAMILY = "1,2"; CODE_SIGN_STYLE = Automatic; }; name = Release; };
  A0000000000000000000004B = {isa = PBXTargetDependency; target = A00000000000000000000004; };
'''


def scheme():
    app = '<BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="A00000000000000000000004" BuildableName="AtlasPhoneDemo.app" BlueprintName="AtlasPhoneDemo" ReferencedContainer="container:AtlasPhoneDemo.xcodeproj"/>'
    tests = '<BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="A00000000000000000000041" BuildableName="AtlasPhoneDemoUITests.xctest" BlueprintName="AtlasPhoneDemoUITests" ReferencedContainer="container:AtlasPhoneDemo.xcodeproj"/>'
    return ('<?xml version="1.0" encoding="UTF-8"?><Scheme version="1.3">'
            '<BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries>'
            '<BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">' + app + '</BuildActionEntry>'
            '<BuildActionEntry buildForTesting="YES" buildForRunning="NO" buildForProfiling="NO" buildForArchiving="NO" buildForAnalyzing="NO">' + tests + '</BuildActionEntry>'
            '</BuildActionEntries></BuildAction>'
            '<TestAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB"><Testables><TestableReference skipped="NO">' + tests + '</TestableReference></Testables></TestAction>'
            '<LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" debugServiceExtension="internal" allowLocationSimulation="YES"><BuildableProductRunnable runnableDebuggingMode="0">' + app + '</BuildableProductRunnable></LaunchAction>'
            '<AnalyzeAction buildConfiguration="Debug"/><ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/></Scheme>')


def create(destination):
    destination = Path(destination).expanduser().resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Build outside the public checkout")
    destination.mkdir(parents=True, exist_ok=False)
    project = destination / "AtlasPhoneDemo.xcodeproj"
    project.mkdir()
    content = PROJECT.replace('targets = (A00000000000000000000004);',
                              'targets = (A00000000000000000000004, A00000000000000000000041);')
    content = content.replace('A00000000000000000000013, A00000000000000000000003',
                              'A00000000000000000000013, A00000000000000000000043, A00000000000000000000003')
    content = content.replace('children = (A00000000000000000000005);',
                              'children = (A00000000000000000000005, A00000000000000000000042);')
    content = content.replace(' };\n rootObject', UI_TEST_OBJECTS + '\n };\n rootObject')
    extra_sources = ("PhotoReflection.swift", "LocalPhotoAnalyzer.swift", "PhotoReflectionView.swift")
    for index, name in enumerate(extra_sources, start=4):
        reference = f"A0000000000000000000001{index}"
        build = f"A0000000000000000000002{index}"
        content = content.replace('A00000000000000000000011, A00000000000000000000012', f'{reference}, A00000000000000000000011, A00000000000000000000012')
        content = content.replace('A00000000000000000000021, A00000000000000000000022', f'{build}, A00000000000000000000021, A00000000000000000000022')
        objects = (f'  {reference} = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = {name}; sourceTree = "<group>"; }};\n'
                   f'  {build} = {{isa = PBXBuildFile; fileRef = {reference}; }};\n')
        content = content.replace(' };\n rootObject', objects + ' };\n rootObject')
    (project / "project.pbxproj").write_text(content, encoding="utf-8")
    schemes = project / "xcshareddata" / "xcschemes"
    schemes.mkdir(parents=True)
    (schemes / "AtlasPhoneDemo.xcscheme").write_text(scheme(), encoding="utf-8")
    for name in ("PhoneBundle.swift", "AtlasContextExportView.swift", "AtlasPhoneDemoApp.swift", *extra_sources):
        shutil.copyfile(ROOT / "mobile" / name, destination / name)
    shutil.copyfile(ROOT / "tests" / "PhoneReviewUITests.swift", destination / "PhoneReviewUITests.swift")
    print("Created an isolated fictional demo project. Choose a signing team in Xcode for a physical device.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    create(parser.parse_args().output)
