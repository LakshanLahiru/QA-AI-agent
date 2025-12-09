import type { Options } from '@wdio/types';
import * as dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

/**
 * BrowserStack iOS Configuration for WebdriverIO
 * 
 * This configuration allows you to run iOS app tests on BrowserStack cloud devices from Windows
 * 
 * Prerequisites:
 *   1. BrowserStack account (get from https://www.browserstack.com/)
 *   2. Upload your iOS app (.ipa or .app file) to BrowserStack
 *   3. Set environment variables for BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY
 * 
 * Usage:
 *   npx wdio run wdio.browserstack.ios.conf.ts
 * 
 * Or with npm script:
 *   npm run test:browserstack:ios
 */

// BrowserStack credentials
const BROWSERSTACK_USERNAME = process.env.BROWSERSTACK_USERNAME || 'your_username';
const BROWSERSTACK_ACCESS_KEY = process.env.BROWSERSTACK_ACCESS_KEY || 'your_access_key';

// App configuration
// After uploading your app to BrowserStack, you'll get an app URL like: bs://c700ce60cf13ae8ed97705a55b8e022f13c5827c
const BROWSERSTACK_APP_URL = process.env.BROWSERSTACK_APP_URL || 'bs://your_app_id';

// Alternative: You can also provide a publicly accessible app URL
// const APP_URL = 'https://www.browserstack.com/app-automate/sample-apps/ios/BStackSampleApp.ipa';

export const config = {
    // BrowserStack authentication - must be set before hostname
    user: BROWSERSTACK_USERNAME,
    key: BROWSERSTACK_ACCESS_KEY,
    
    // BrowserStack hub URL
    hostname: 'hub.browserstack.com',
    port: 443,
    protocol: 'https',
    path: '/wd/hub',
    
    // Test specs
    specs: ['./src/tests/**/*.e2e.ts'],
    
    // Patterns to exclude
    exclude: [],
    
    maxInstances: 5, // BrowserStack allows parallel tests based on your plan
    
    // BrowserStack capabilities for iOS devices
    capabilities: [
        {
            // Real iPhone 14 Pro
            platformName: 'iOS',
            'appium:platformVersion': '16',
            'appium:deviceName': 'iPhone 14 Pro',
            'appium:app': BROWSERSTACK_APP_URL,
            'appium:automationName': 'XCUITest',
            
            // BrowserStack specific capabilities
            'bstack:options': {
                projectName: 'QA-AI-Agent iOS Tests',
                buildName: `iOS Build - ${new Date().toISOString().split('T')[0]}`,
                sessionName: 'iOS App Test',
                debug: true,               // Enable visual logs
                networkLogs: true,         // Enable network logs
                appiumLogs: true,          // Enable Appium logs
                video: true,               // Record video of test execution
                deviceLogs: true,          // Enable device logs
                
                // Additional options
                // acceptInsecureCerts: true,
                // local: false,           // Set to true if testing local/staging app
                // localIdentifier: 'random_string', // Required if local is true
            }
        },
        
        // You can add more device configurations here
        // Uncomment to test on multiple iOS devices in parallel
        /*
        {
            platformName: 'iOS',
            'appium:platformVersion': '15',
            'appium:deviceName': 'iPhone 13',
            'appium:app': BROWSERSTACK_APP_URL,
            'appium:automationName': 'XCUITest',
            'bstack:options': {
                userName: BROWSERSTACK_USERNAME,
                accessKey: BROWSERSTACK_ACCESS_KEY,
                projectName: 'QA-AI-Agent iOS Tests',
                buildName: `iOS Build - ${new Date().toISOString().split('T')[0]}`,
                sessionName: 'iOS App Test - iPhone 13',
                debug: true,
                networkLogs: true,
                video: true,
            }
        },
        {
            platformName: 'iOS',
            'appium:platformVersion': '14',
            'appium:deviceName': 'iPhone 12',
            'appium:app': BROWSERSTACK_APP_URL,
            'appium:automationName': 'XCUITest',
            'bstack:options': {
                userName: BROWSERSTACK_USERNAME,
                accessKey: BROWSERSTACK_ACCESS_KEY,
                projectName: 'QA-AI-Agent iOS Tests',
                buildName: `iOS Build - ${new Date().toISOString().split('T')[0]}`,
                sessionName: 'iOS App Test - iPhone 12',
                debug: true,
                networkLogs: true,
                video: true,
            }
        }
        */
    ],
    
    // Test configurations
    logLevel: 'info',
    bail: 0,
    baseUrl: '',
    waitforTimeout: 30000,
    connectionRetryTimeout: 120000,
    connectionRetryCount: 3,
    
    // Framework configuration
    framework: 'mocha',
    
    // Reporters
    reporters: [
        'spec',
        ['allure', {
            outputDir: 'allure-results',
            disableWebdriverStepsReporting: false,
            disableWebdriverScreenshotsReporting: false,
            addConsoleLogs: true,
        }]
    ],
    
    // BrowserStack service
    services: [
        ['browserstack', {
            browserstackLocal: false, // Set to true if you need to test local apps
            opts: {
                // BrowserStack Local options (if browserstackLocal is true)
                // forceLocal: true,
                // onlyAutomate: true,
            }
        }]
    ],
    
    // Mocha options
    mochaOpts: {
        ui: 'bdd',
        timeout: 120000, // 2 minutes per test
        retries: 1, // Retry failed tests once
    },
    
    // TypeScript compilation
    autoCompileOpts: {
        autoCompile: true,
        tsNodeOpts: {
            transpileOnly: true,
            project: './tsconfig.json'
        }
    },
    
    // Hooks
    /**
     * Gets executed before test execution begins
     */
    before: function (capabilities, specs) {
        console.log('Starting test on BrowserStack iOS device...');
    },
    
    /**
     * Gets executed after all tests are done
     */
    after: function (result, capabilities, specs) {
        console.log('Test execution completed on BrowserStack');
    },
    
    /**
     * Gets executed after all workers got shut down and the process is about to exit
     */
    onComplete: function(exitCode, config, capabilities, results) {
        console.log('All tests completed!');
        console.log('View your test results at: https://app-automate.browserstack.com/dashboard');
    }
};

export default config;

