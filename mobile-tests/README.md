# Mobile Tests - WebDriverIO + Appium

WebDriverIO test framework for iOS and Android mobile applications with AI-powered test generation.

## 📋 Quick Reference

### Run Tests

```bash
# Android (default)
npm test

# iOS
npm run test:ios

# BrowserStack iOS
npm run test:browserstack:ios

# Specific test file
npm test -- --spec src/tests/home.e2e.ts
npm run test:ios -- --spec src/tests/login.e2e.ts

# Crawl page elements
CRAWL_PAGE_NAME=login npm test -- --spec src/tests/crawl-page.e2e.ts
CRAWL_PAGE_NAME=home npm run test:ios -- --spec src/tests/crawl-page.e2e.ts
```

### View Reports

```bash
# Generate Allure report
npm run allure:generate

# Open Allure report
npm run allure:open

# Combined (generate and open)
npx allure open ./allure-report
```

---

## 📁 Project Structure

```
mobile-tests/
├── src/
│   ├── pageobjects/           # Page Object Models
│   │   ├── HomePage.ts        # Home page objects
│   │   ├── LoginPage.ts       # Login page objects
│   │   └── ...
│   └── tests/                 # Test specifications
│       ├── home.e2e.ts        # Home page tests
│       ├── login.e2e.ts       # Login page tests
│       └── crawl-page.e2e.ts  # Page crawling test
│
├── crawls/                    # Crawled page XMLs
│   ├── home.xml              # Home screen elements
│   ├── login.xml             # Login screen elements
│   └── ...
│
├── acceptance-criteria/       # Test requirements
│   ├── home.json             # Home page criteria
│   ├── login.json            # Login page criteria
│   └── ...
│
├── manual-tests/              # Generated manual test cases
│   ├── home_manual.json
│   ├── login_manual.json
│   └── ...
│
├── app/                       # Test applications
│   ├── Android-NativeDemoApp-0.4.0.apk
│   └── iOS-Simulator-NativeDemoApp.app/
│
├── allure-results/            # Test execution results
├── allure-report/             # HTML test reports
├── logs/                      # Test logs
│
├── wdio.conf.ts              # Android configuration
├── wdio.ios.conf.ts          # iOS configuration
├── wdio.browserstack.ios.conf.ts  # BrowserStack config
├── package.json              # Dependencies & scripts
└── tsconfig.json             # TypeScript config
```

---

## ⚙️ Configuration Files

### wdio.conf.ts (Android)

Main configuration for Android testing:

```typescript
{
  runner: 'local',
  hostname: '127.0.0.1',
  port: 4723,
  path: '/',
  
  specs: ['./src/tests/**/*.ts'],
  
  capabilities: [{
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'emulator-5554',
    'appium:platformVersion': '13.0',
    'appium:app': 'path/to/app.apk',
    'appium:appPackage': 'com.wdiodemoapp',
    'appium:appActivity': '.MainActivity',
  }]
}
```

### wdio.ios.conf.ts (iOS)

Configuration for iOS testing:

```typescript
{
  capabilities: [{
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'iPhone 14',
    'appium:platformVersion': '16.0',
    'appium:app': 'path/to/app.app',
    'appium:bundleId': 'org.reactjs.native.example.wdiodemoapp',
  }]
}
```

---

## 🎯 Writing Tests

### Page Object Model Pattern

**Example: HomePage.ts**

```typescript
class HomePage {
    // Element getters
    public get loginButton() {
        return $('~Login');
    }

    public get welcomeText() {
        return $('~welcome-text');
    }

    // Actions
    public async clickLogin() {
        const btn = await this.loginButton;
        await btn.waitForDisplayed({ timeout: 10000 });
        await btn.click();
    }

    public async getWelcomeMessage(): Promise<string> {
        const text = await this.welcomeText;
        await text.waitForDisplayed({ timeout: 10000 });
        return await text.getText();
    }
}

export default new HomePage();
```

**Example: Test Spec**

```typescript
import { expect } from 'chai';
import HomePage from '../pageobjects/HomePage';

describe('Home Page Tests', () => {
    beforeEach(async () => {
        await driver.pause(2000);
    });

    it('should display welcome message', async () => {
        const message = await HomePage.getWelcomeMessage();
        expect(message).to.include('Welcome');
    });

    it('should navigate to login', async () => {
        await HomePage.clickLogin();
        await driver.pause(1000);
        // Verify navigation
    });
});
```

---

## 🔍 Element Selectors

### Accessibility ID (Recommended)

```typescript
// Best for cross-platform
$('~element-id')              // iOS & Android
```

### iOS Specific

```typescript
$('~Text Button')                    // Accessibility ID
$('label=Button Text')               // By label
$('name=Button Name')                // By name
$('type=XCUIElementTypeButton')      // By type
```

### Android Specific

```typescript
$('~button-id')                                      // Accessibility ID
$('android=new UiSelector().text("Button")')         // By text
$('android=new UiSelector().resourceId("id")')       // By resource ID
$('android=new UiSelector().className("Button")')    // By class
```

### Platform Detection

```typescript
const platform = driver.capabilities.platformName?.toLowerCase();

public get myButton() {
    if (platform === 'ios') {
        return $('~iOS Button');
    } else {
        return $('~Android Button');
    }
}
```

---

## 📝 Acceptance Criteria Format

**File:** `acceptance-criteria/feature.json`

```json
{
  "page": "login",
  "feature": "User Authentication",
  "acceptanceCriteria": [
    {
      "id": "LOGIN_001",
      "description": "User should see login form"
    },
    {
      "id": "LOGIN_002",
      "description": "User can enter email and password"
    },
    {
      "id": "LOGIN_003",
      "description": "User can submit login form"
    },
    {
      "id": "LOGIN_004",
      "description": "User sees error message for invalid credentials"
    }
  ]
}
```

---

## 🤖 AI Test Generation

The AI agent generates tests in 3 steps:

### 1. Manual Test Cases

AI analyzes acceptance criteria and crawled elements to generate human-readable test cases.

**Output:** `manual-tests/{page}_manual.json`

```json
{
  "page": "login",
  "manualTests": [
    {
      "id": "LOGIN_001",
      "title": "Verify login form display",
      "steps": [
        "Launch the app",
        "Navigate to Login screen",
        "Verify email input field is visible",
        "Verify password input field is visible",
        "Verify login button is visible"
      ],
      "expectedResult": "All login form elements are displayed"
    }
  ]
}
```

### 2. Page Objects

AI generates Page Object Model classes with element selectors and methods.

**Output:** `src/pageobjects/{Page}Page.ts`

### 3. Test Scripts

AI generates executable test specifications using the page objects.

**Output:** `src/tests/{page}.e2e.ts`

---

## 🐛 Debugging

### Enable Debug Logs

```bash
# Set log level in wdio config
logLevel: 'debug'

# Or via command line
npm test -- --logLevel=debug
```

### Take Screenshots

```typescript
await driver.saveScreenshot('./screenshot.png');
```

### Get Page Source

```typescript
const pageSource = await driver.getPageSource();
console.log(pageSource);
```

### Pause Execution

```typescript
await driver.pause(5000); // Pause for 5 seconds
await driver.debug();     // Interactive debugging
```

### Check Element Details

```typescript
const element = await $('~button');
console.log('Is Displayed:', await element.isDisplayed());
console.log('Is Enabled:', await element.isEnabled());
console.log('Text:', await element.getText());
console.log('Location:', await element.getLocation());
console.log('Size:', await element.getSize());
```

---

## 🔧 Common Tasks

### Update App Path

**Android:**
```typescript
// wdio.conf.ts
const APP_PATH = 'C:/path/to/your-app.apk';
const APP_PACKAGE = 'com.yourapp';
const APP_ACTIVITY = '.MainActivity';
```

**iOS:**
```typescript
// wdio.ios.conf.ts
const APP_PATH = '/path/to/your-app.app';
const BUNDLE_ID = 'com.yourapp.bundleid';
```

### Add New Test

1. Create acceptance criteria: `acceptance-criteria/newpage.json`
2. Crawl page: `CRAWL_PAGE_NAME=newpage npm test -- --spec src/tests/crawl-page.e2e.ts`
3. Generate tests using CLI: `python ../agent-backend/cli.py`
4. Run tests: `npm test -- --spec src/tests/newpage.e2e.ts`

### Update Selectors

If elements change:
1. Re-crawl page to get new selectors
2. Update Page Object Model in `src/pageobjects/`
3. Re-run tests

### Handle Waits

```typescript
// Wait for element
await element.waitForDisplayed({ timeout: 10000 });
await element.waitForEnabled({ timeout: 5000 });
await element.waitForExist({ timeout: 5000 });

// Wait for condition
await driver.waitUntil(
    async () => (await element.getText()) === 'Expected',
    { timeout: 10000, timeoutMsg: 'Text did not match' }
);
```

### Handle Alerts

```typescript
// Accept alert
await driver.acceptAlert();

// Dismiss alert
await driver.dismissAlert();

// Get alert text
const alertText = await driver.getAlertText();
```

---

## 📊 Allure Reports

### Report Features

- ✅ Pass/Fail status for each test
- 📸 Screenshots on failure
- 📝 Detailed test steps
- ⏱️ Execution time
- 📊 Statistics and trends
- 🔄 Test history

### Custom Allure Annotations

```typescript
import allure from '@wdio/allure-reporter';

// Add description
allure.addDescription('This test verifies login functionality');

// Add step
allure.addStep('Enter email address');

// Add attachment
allure.addAttachment('Screenshot', screenshot, 'image/png');

// Add severity
allure.addSeverity('critical');

// Add feature
allure.addFeature('Authentication');

// Add story
allure.addStory('User Login');
```

---

## 🚨 Troubleshooting

### Tests Fail to Start

```bash
# Check Appium is running
curl http://127.0.0.1:4723/status

# Restart Appium
killall node
appium
```

### Element Not Found

```bash
# Re-crawl page to verify selectors
CRAWL_PAGE_NAME=page npm test -- --spec src/tests/crawl-page.e2e.ts

# Check crawled XML
cat crawls/page.xml
```

### App Not Installing

```bash
# Android: Uninstall first
adb uninstall com.wdiodemoapp
adb install app/Android-NativeDemoApp-0.4.0.apk

# iOS: Reinstall
xcrun simctl uninstall booted org.reactjs.native.example.wdiodemoapp
xcrun simctl install booted app/iOS-Simulator-NativeDemoApp.app
```

### Timeout Issues

Increase timeouts in tests:

```typescript
// Before
await element.waitForDisplayed({ timeout: 5000 });

// After
await element.waitForDisplayed({ timeout: 15000 });
```

---

## 📚 Useful Commands

```bash
# Install dependencies
npm install

# Run tests
npm test                    # Android
npm run test:ios           # iOS

# Crawl pages
CRAWL_PAGE_NAME=login npm test -- --spec src/tests/crawl-page.e2e.ts

# Generate reports
npm run allure:generate
npm run allure:open

# Clean artifacts
rm -rf allure-results allure-report

# TypeScript compilation
npx tsc --noEmit

# Lint code
npm run lint (if configured)
```

---

## 🔗 Resources

- [WebDriverIO Docs](https://webdriver.io/)
- [Appium Docs](https://appium.io/docs/en/)
- [Allure Report](https://docs.qameta.io/allure/)
- [Mocha Framework](https://mochajs.org/)
- [Chai Assertions](https://www.chaijs.com/)

---

**For complete setup instructions, see:** `../README.md`

