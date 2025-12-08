import type { Options } from '@wdio/types';

/**
 * iOS-specific WebdriverIO configuration
 * 
 * Usage:
 *   npx wdio run wdio.ios.conf.ts
 * 
 * Or set environment variables:
 *   PLATFORM_NAME=iOS npx wdio run wdio.conf.ts
 */

// iOS App configuration
const IOS_APP_PATH = process.env.IOS_APP_PATH || process.env.APP_PATH || '/path/to/your/app.app';
const IOS_DEVICE_NAME = process.env.IOS_DEVICE_NAME || 'iPhone 14';
const IOS_PLATFORM_VERSION = process.env.IOS_PLATFORM_VERSION || '17.0';
const IOS_BUNDLE_ID = process.env.IOS_BUNDLE_ID || 'com.example.app'; // Your app's bundle ID

export const config = {
    runner: 'local',

    hostname: '127.0.0.1',
    port: 4723,
    path: '/',

    specs: ['./src/tests/**/*.ts'],

    maxInstances: 1,

    capabilities: [{
        platformName: 'iOS',
        'appium:automationName': 'XCUITest',
        'appium:deviceName': IOS_DEVICE_NAME,
        'appium:platformVersion': IOS_PLATFORM_VERSION,
        
        // App configuration
        'appium:app': IOS_APP_PATH,
        'appium:bundleId': IOS_BUNDLE_ID,
        
        // Reset options
        'appium:noReset': false,      // Set to true to keep app data between sessions
        'appium:fullReset': false,    // Set to true to uninstall app after session
        
        // Additional iOS options (uncomment if needed)
        // 'appium:udid': '<DEVICE_UDID>',  // Use UDID for physical devices
        // 'appium:xcodeOrgId': '<TEAM_ID>',  // For physical device testing
        // 'appium:xcodeSigningId': 'iPhone Developer',  // For physical device testing
        // 'appium:autoAcceptAlerts': true,  // Auto-accept iOS alerts
        // 'appium:autoDismissAlerts': true,  // Auto-dismiss iOS alerts
    }],

    logLevel: 'info',
    framework: 'mocha',

    reporters: [
        'spec',
        ['allure', {
            outputDir: 'allure-results',
            disableWebdriverStepsReporting: false,
            disableWebdriverScreenshotsReporting: false
        }]
    ],

    services: [
        // Appium service - comment out if Appium is running separately
        // Uncomment if you want WebdriverIO to start Appium automatically
        // ['appium', {
        //     command: 'appium',
        //     args: {
        //         port: 4723,
        //         address: '127.0.0.1',
        //     }
        // }]
    ],

    mochaOpts: {
        ui: 'bdd',
        timeout: 120000
    },

    autoCompileOpts: {
        autoCompile: true,
        tsNodeOpts: {
            transpileOnly: true,
            project: './tsconfig.json'
        }
    }
};

export default config;

