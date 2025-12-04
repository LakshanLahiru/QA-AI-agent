import type { Options } from '@wdio/types';

export const config: Options.Testrunner = {
    runner: 'local',

    hostname: '127.0.0.1',
    port: 4723,
    path: '/',

    specs: ['./src/tests/**/*.ts'],

    maxInstances: 1,

    capabilities: [{
        platformName: 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'Pixel_5_API_33',   // OR Pixel_5_API_33
        'appium:platformVersion': '13.0',
        browserName: 'Chrome',
        'appium:chromedriverAutodownload': true
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
        ['appium', {
            command: 'appium',
            args: {
                port: 4723,
                address: '127.0.0.1',
                // Enable automatic Chromedriver download for any driver that supports it
                allowInsecure: '*:chromedriver_autodownload'
            }
        }]
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
