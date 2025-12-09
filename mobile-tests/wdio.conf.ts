import type { Options } from '@wdio/types';

// App configuration - set these or use CLI to configure
// These can be set via environment variables or CLI will update this file
const APP_PATH = process.env.APP_PATH || 'C:/Users/LENOVO/Desktop/upwork/QA-AI-agent/mobile-tests/app/Android-NativeDemoApp-0.4.0.apk'; // Full path to .apk file
const APP_PACKAGE = process.env.APP_PACKAGE || 'com.wdiodemoapp'; // Package name for Android-NativeDemoApp-0.4.0.apk
const APP_ACTIVITY = process.env.APP_ACTIVITY || '.MainActivity'; // e.g., '.MainActivity'

export const config = {
    runner: 'local',

    hostname: '127.0.0.1',
    port: 4723,
    path: '/',

    specs: ['./src/tests/**/*.ts'],

    maxInstances: 1,

    capabilities: [{
        platformName: 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'sdk_gphone64_x86_64',
        'appium:platformVersion': '13.0',
        
        // Native app configuration (if APP_PATH is set)
        ...(APP_PATH ? {
            'appium:app': APP_PATH,
            'appium:appPackage': APP_PACKAGE,
            'appium:appActivity': APP_ACTIVITY,
            'appium:noReset': false, // Set to true to keep app data between sessions
            'appium:fullReset': false, // Set to true to uninstall app after session
        } : {
            // Browser configuration (fallback if no app)
            browserName: 'Chrome',
            'appium:chromedriverAutodownload': true
        }),
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
        //         allowInsecure: '*:chromedriver_autodownload'
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
