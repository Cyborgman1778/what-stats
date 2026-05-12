import UIKit
import Capacitor

private enum ZipImportHandler {
    private static let importDirectoryName = "zip-imports"

    static func prepareImport(from sourceURL: URL) -> URL? {
        guard sourceURL.isFileURL, sourceURL.pathExtension.lowercased() == "zip" else {
            return nil
        }

        let didAccessSecurityScopedResource = sourceURL.startAccessingSecurityScopedResource()

        defer {
            if didAccessSecurityScopedResource {
                sourceURL.stopAccessingSecurityScopedResource()
            }
        }

        do {
            let fileManager = FileManager.default
            let importRoot = try importRootURL(fileManager: fileManager)
            try recreateDirectory(importRoot, fileManager: fileManager)

            let importDirectory = importRoot.appendingPathComponent(String(Int(Date().timeIntervalSince1970 * 1000)), isDirectory: true)
            try fileManager.createDirectory(at: importDirectory, withIntermediateDirectories: true)

            let targetURL = importDirectory.appendingPathComponent(sanitizeFileName(sourceURL.lastPathComponent))
            try fileManager.copyItem(at: sourceURL, to: targetURL)

            return targetURL
        } catch {
            return nil
        }
    }

    private static func importRootURL(fileManager: FileManager) throws -> URL {
        let cacheDirectory = try fileManager.url(for: .cachesDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
        return cacheDirectory.appendingPathComponent(importDirectoryName, isDirectory: true)
    }

    private static func recreateDirectory(_ directory: URL, fileManager: FileManager) throws {
        if fileManager.fileExists(atPath: directory.path) {
            try fileManager.removeItem(at: directory)
        }

        try fileManager.createDirectory(at: directory, withIntermediateDirectories: true)
    }

    private static func sanitizeFileName(_ fileName: String) -> String {
        let invalidCharacters = CharacterSet(charactersIn: "/\\:*?\"<>|")
        let sanitized = fileName.components(separatedBy: invalidCharacters).joined(separator: "-").trimmingCharacters(in: .whitespacesAndNewlines)

        if sanitized.isEmpty || sanitized == "." || sanitized == ".." {
            return "whatsapp-chat.zip"
        }

        return sanitized.lowercased().hasSuffix(".zip") ? sanitized : "\(sanitized).zip"
    }
}

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }

    func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey: Any] = [:]) -> Bool {
        // Called when the app was launched with a url. Feel free to add additional processing here,
        // but if you want the App API to support tracking app url opens, make sure to keep this call
        let importedURL = ZipImportHandler.prepareImport(from: url) ?? url
        return ApplicationDelegateProxy.shared.application(app, open: importedURL, options: options)
    }

    func application(_ application: UIApplication, continue userActivity: NSUserActivity, restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {
        // Called when the app was launched with an activity, including Universal Links.
        // Feel free to add additional processing here, but if you want the App API to support
        // tracking app url opens, make sure to keep this call
        return ApplicationDelegateProxy.shared.application(application, continue: userActivity, restorationHandler: restorationHandler)
    }

}
