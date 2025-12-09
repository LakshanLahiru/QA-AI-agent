# QA AI Agent - Mobile Test Automation

An AI-powered mobile test automation framework that generates and executes tests for iOS and Android applications using WebDriverIO and Appium.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Android Setup](#android-setup)
- [iOS Setup](#ios-setup)
- [Project Setup](#project-setup)
- [Running Tests](#running-tests)
- [CLI Workflow](#cli-workflow)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- 🤖 AI-powered test generation from acceptance criteria
- 📱 Cross-platform support (iOS & Android)
- 🔄 Automatic page crawling and element detection
- 🧪 Manual test case generation
- 📝 Automated test script generation (Page Object Model)
- 🔧 Auto-healing for failed tests
- 📊 Allure reporting
- 🎯 BrowserStack integration for cloud testing

---

## 🔧 Prerequisites

### Required Software

1. **Node.js** (v18 or higher)
   - Download: https://nodejs.org/
   - Verify: `node --version`

2. **Python** (v3.8 or higher)
   - Download: https://www.python.org/
   - Verify: `python --version` or `python3 --version`

3. **Java JDK** (v11 or higher)
   - Download: https://www.oracle.com/java/technologies/downloads/
   - Set `JAVA_HOME` environment variable
   - Verify: `java -version`

4. **Appium** (v2.0 or higher)
   ```bash
   npm install -g appium
   appium --version
   ```

5. **Appium Drivers**
   ```bash
   # For Android
   appium driver install uiautomator2
   
   # For iOS
   appium driver install xcuitest
   ```

### Platform-Specific Requirements

#### For Android Testing:
- Android Studio or Android SDK Command-line tools
- Android SDK Platform Tools
- Android Emulator or Physical Device

#### For iOS Testing:
- macOS (required)
- Xcode (latest version)
- Xcode Command Line Tools
- iOS Simulator or Physical Device

---

## 📱 Android Setup

### Step 1: Install Android Studio

1. Download Android Studio: https://developer.android.com/studio
2. Install Android Studio
3. Open Android Studio → SDK Manager

### Step 2: Install Android SDK Components

In SDK Manager, install:
- ✅ Android SDK Platform (API 33 or higher)
- ✅ Android SDK Build-Tools
- ✅ Android SDK Platform-Tools
- ✅ Android Emulator
- ✅ System Images (for emulator)

### Step 3: Set Environment Variables

**Windows:**
```powershell
# Add to System Environment Variables
ANDROID_HOME = C:\Users\YOUR_USERNAME\AppData\Local\Android\Sdk

# Add to Path:
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\tools
%ANDROID_HOME%\emulator
```

**macOS/Linux:**
```bash
# Add to ~/.bash_profile or ~/.zshrc
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/emulator
```

Verify:
```bash
adb --version
emulator -list-avds
```

### Step 4: Create Android Emulator

**Using Android Studio:**
1. Open Android Studio
2. Tools → Device Manager
3. Create Device → Choose device (e.g., Pixel 6)
4. Select System Image (e.g., Android 13 - API 33)
5. Finish and launch emulator

**Using Command Line:**
```bash
# List available system images
sdkmanager --list | grep system-images

# Create AVD
avdmanager create avd -n test_device -k "system-images;android-33;google_apis;x86_64"

# Start emulator
emulator -avd test_device
```

### Step 5: Verify Android Setup

```bash
# Start emulator
emulator -avd test_device

# In another terminal, check if device is connected
adb devices
# Should show: List of devices attached
#              emulator-5554   device
```

### Step 6: Download Test App

Download the Android demo app:
```bash
cd mobile-tests/app
# Download from: https://github.com/webdriverio/native-demo-app/releases
# Or use the included: Android-NativeDemoApp-0.4.0.apk
```

---

## 🍎 iOS Setup

### Step 1: Install Xcode

1. Install Xcode from App Store
2. Open Xcode and accept license
3. Install Command Line Tools:
   ```bash
   xcode-select --install
   ```

### Step 2: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 3: Install Additional Tools

```bash
# Install Carthage
brew install carthage

# Install libimobiledevice (for real iOS devices)
brew install libimobiledevice

# Install ios-deploy (for real iOS devices)
npm install -g ios-deploy
```

### Step 4: Install Appium XCUITest Driver

```bash
appium driver install xcuitest

# Verify installation
appium driver list
```

### Step 5: Setup iOS Simulator

**List available simulators:**
```bash
xcrun simctl list devices
```

**Create a new simulator (if needed):**
```bash
# Create iPhone 14 with iOS 16
xcrun simctl create "iPhone 14" "iPhone 14" "iOS16.0"
```

**Boot simulator:**
```bash
# Get device ID from list
xcrun simctl boot <DEVICE_ID>

# Or open Simulator app
open -a Simulator
```

### Step 6: Download iOS Test App

Download the iOS demo app:
```bash
cd mobile-tests/app
# Download from: https://github.com/webdriverio/native-demo-app/releases
# Or use the included: iOS-Simulator-NativeDemoApp.app.zip
# Extract the .app file
```

### Step 7: Install App on Simulator

```bash
xcrun simctl install booted /path/to/iOS-Simulator-NativeDemoApp.app
```

---

## 🚀 Project Setup

### Step 1: Clone/Extract Project

```bash
cd /path/to/QA-AI-agent
```

### Step 2: Install Python Dependencies

```bash
cd agent-backend
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### Step 3: Install Node.js Dependencies

```bash
cd ../mobile-tests
npm install
```

### Step 4: Configure Environment Variables

Create `.env` file in `agent-backend` directory:

```bash
# agent-backend/.env
OPENAI_API_KEY=your_openai_api_key_here

# Optional: BrowserStack credentials
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

### Step 5: Configure App Paths

**For Android:**
Edit `mobile-tests/wdio.conf.ts`:
```typescript
const APP_PATH = 'C:/path/to/Android-NativeDemoApp-0.4.0.apk';
const APP_PACKAGE = 'com.wdiodemoapp';
const APP_ACTIVITY = '.MainActivity';
```

**For iOS:**
Edit `mobile-tests/wdio.ios.conf.ts`:
```typescript
const APP_PATH = '/path/to/iOS-Simulator-NativeDemoApp.app';
const BUNDLE_ID = 'org.reactjs.native.example.wdiodemoapp';
```

---

## ▶️ Running Tests

### Method 1: Using CLI (Recommended)

The CLI provides a complete workflow for test generation and execution.

```bash
cd agent-backend
python cli.py
```

**CLI Menu:**
1. Select Platform and Device
2. Configure App (Native App Path)
3. Add Acceptance Criteria
4. Crawl Page Elements
5. Generate Manual Test Cases
6. Generate Test Scripts (POM + Tests)
7. Execute Tests
8. Generate Allure Report
9. Run Complete Workflow (All Steps)
10. Exit

**Complete Workflow Example:**

1. **Select Platform:** Choose iOS or Android
2. **Configure App:** Set app path, package, activity
3. **Add Acceptance Criteria:** Define test scenarios
4. **Crawl Page:** Extract UI elements
5. **Generate Tests:** AI creates test scripts
6. **Execute Tests:** Run automated tests
7. **View Report:** Generate Allure report

### Method 2: Manual Test Execution

#### Start Appium Server

```bash
appium
# Server will start on http://127.0.0.1:4723
```

#### Run Android Tests

```bash
cd mobile-tests

# Start Android emulator first
emulator -avd test_device

# Run all tests
npm test

# Run specific test
npm test -- --spec src/tests/home.e2e.ts

# Run with specific page
CRAWL_PAGE_NAME=login npm test -- --spec src/tests/crawl-page.e2e.ts
```

#### Run iOS Tests

```bash
cd mobile-tests

# Boot iOS simulator first
open -a Simulator

# Run all iOS tests
npm run test:ios

# Run specific test
npm run test:ios -- --spec src/tests/home.e2e.ts
```

#### Run Tests on BrowserStack

```bash
# iOS on BrowserStack
npm run test:browserstack:ios

# Android on BrowserStack (configure first)
npm run test:browserstack:android
```

### Method 3: Using Python Script

```bash
cd agent-backend
python run_cli.py
```

---

## 🔄 CLI Workflow

### Complete Workflow (Step-by-Step)

#### 1. Select Platform and Device

```
Choose option: 1
Select Platform:
1. Android
2. iOS
Enter choice: 2

Available iOS Simulators:
1. iPhone 14 (iOS 16.0)
2. iPhone 15 Pro (iOS 17.0)
Enter choice: 1
```

#### 2. Configure App Path

```
Choose option: 2
Enter full path to app: /Users/me/apps/iOS-Simulator-NativeDemoApp.app
Enter bundle ID: org.reactjs.native.example.wdiodemoapp
```

#### 3. Add Acceptance Criteria

```
Choose option: 3
Enter page name: login
Enter feature name: login
Enter description: user should be able to login

Add more criteria? (y/n): n
```

This creates: `mobile-tests/acceptance-criteria/login.json`

#### 4. Crawl Page Elements

```
Choose option: 4
Enter page name: login
```

This:
- Launches app
- Navigates to login page
- Extracts all UI elements
- Saves to: `mobile-tests/crawls/login.xml`

#### 5. Generate Manual Test Cases

```
Choose option: 5
```

This:
- Uses AI to analyze acceptance criteria
- Generates human-readable test cases
- Saves to: `mobile-tests/manual-tests/login_manual.json`

#### 6. Generate Test Scripts

```
Choose option: 6
```

This:
- Uses AI to generate Page Object Model
- Creates automated test scripts
- Saves to:
  - `mobile-tests/src/pageobjects/LoginPage.ts`
  - `mobile-tests/src/tests/login.e2e.ts`

#### 7. Execute Tests

```
Choose option: 7
Enter page name: login
```

This:
- Starts Appium (if not running)
- Launches device/simulator
- Runs generated tests
- Displays results

#### 8. Generate Allure Report

```
Choose option: 8
```

This:
- Generates HTML report from test results
- Opens report in browser
- Available at: `mobile-tests/allure-report/index.html`

#### 9. Run Complete Workflow

```
Choose option: 9
```

This runs steps 3-8 automatically in sequence.

---

## ⚙️ Configuration

### Android Configuration

**File:** `mobile-tests/wdio.conf.ts`

```typescript
capabilities: [{
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'emulator-5554',
    'appium:platformVersion': '13.0',
    'appium:app': '/path/to/app.apk',
    'appium:appPackage': 'com.wdiodemoapp',
    'appium:appActivity': '.MainActivity',
}]
```

### iOS Configuration

**File:** `mobile-tests/wdio.ios.conf.ts`

```typescript
capabilities: [{
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'iPhone 14',
    'appium:platformVersion': '16.0',
    'appium:app': '/path/to/app.app',
    'appium:bundleId': 'org.reactjs.native.example.wdiodemoapp',
}]
```

### BrowserStack Configuration

**File:** `mobile-tests/wdio.browserstack.ios.conf.ts`

```typescript
user: process.env.BROWSERSTACK_USERNAME
key: process.env.BROWSERSTACK_ACCESS_KEY

capabilities: [{
    'bstack:options': {
        deviceName: 'iPhone 14',
        osVersion: '16',
    },
    'appium:app': 'bs://your-app-id',
}]
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Appium Server Not Starting

**Error:** `EADDRINUSE: address already in use`

**Solution:**
```bash
# Kill existing Appium process
# Windows:
taskkill /F /IM node.exe

# macOS/Linux:
killall node
# or
lsof -ti:4723 | xargs kill -9
```

#### 2. Android Emulator Not Detected

**Error:** `No devices connected`

**Solution:**
```bash
# Check ADB connection
adb devices

# Restart ADB server
adb kill-server
adb start-server

# Reconnect emulator
adb connect emulator-5554
```

#### 3. iOS Simulator Not Booting

**Error:** `Unable to boot device`

**Solution:**
```bash
# Reset simulator
xcrun simctl shutdown all
xcrun simctl erase all

# Restart simulator
xcrun simctl boot <device-id>
```

#### 4. App Installation Fails

**Android:**
```bash
# Uninstall existing app
adb uninstall com.wdiodemoapp

# Install manually
adb install /path/to/app.apk
```

**iOS:**
```bash
# Uninstall from simulator
xcrun simctl uninstall booted org.reactjs.native.example.wdiodemoapp

# Reinstall
xcrun simctl install booted /path/to/app.app
```

#### 5. Tests Cannot Find Elements

**Solution:**
```bash
# Re-crawl the page
cd agent-backend
python cli.py
# Choose: 4. Crawl Page Elements

# Check crawled XML file
cat mobile-tests/crawls/page_name.xml
```

#### 6. Python Module Not Found

**Error:** `ModuleNotFoundError: No module named 'openai'`

**Solution:**
```bash
cd agent-backend
pip install -r requirements.txt
```

#### 7. Node Module Errors

**Error:** `Cannot find module '@wdio/...'`

**Solution:**
```bash
cd mobile-tests
rm -rf node_modules package-lock.json
npm install
```

#### 8. Permission Denied (macOS)

**Error:** `Permission denied: 'app.app'`

**Solution:**
```bash
# Grant permissions
chmod -R 755 /path/to/app.app

# For iOS real device, trust certificate
# Settings → General → Device Management → Trust
```

#### 9. WebDriverIO Config Not Found

**Error:** `No config found`

**Solution:**
```bash
# Verify config file exists
ls -la mobile-tests/wdio.conf.ts
ls -la mobile-tests/wdio.ios.conf.ts

# Run with explicit config
npx wdio run wdio.conf.ts
npx wdio run wdio.ios.conf.ts
```

---

## 📊 Viewing Reports

### Allure Report

After running tests:

```bash
cd mobile-tests

# Generate and open report
npm run allure:generate
npm run allure:open

# Or combined
npx allure open ./allure-report
```

The report includes:
- ✅ Test execution results
- 📸 Screenshots on failure
- 📝 Step-by-step logs
- 📊 Statistics and trends
- ⏱️ Execution timeline

---

## 📁 Project Structure

```
QA-AI-agent/
├── agent-backend/           # Python AI agent
│   ├── agent.py            # Test generation agent
│   ├── cli.py              # CLI interface
│   ├── device_manager.py   # Device management
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
│
├── mobile-tests/           # WebDriverIO tests
│   ├── src/
│   │   ├── pageobjects/   # Page Object Models
│   │   └── tests/         # Test specs
│   ├── crawls/            # Crawled page XMLs
│   ├── acceptance-criteria/ # Test criteria
│   ├── manual-tests/      # Generated manual tests
│   ├── allure-results/    # Test results
│   ├── allure-report/     # HTML reports
│   ├── app/               # Test applications
│   ├── wdio.conf.ts       # Android config
│   ├── wdio.ios.conf.ts   # iOS config
│   └── package.json       # Node dependencies
│
└── README.md              # This file
```

---

## 🎯 Quick Start Guide

### For New Users (Complete Setup)

```bash
# 1. Setup project
cd QA-AI-agent
cd agent-backend && pip install -r requirements.txt
cd ../mobile-tests && npm install

# 2. Start Appium
appium

# 3. Start emulator/simulator (in another terminal)
# Android:
emulator -avd test_device

# iOS:
open -a Simulator

# 4. Run CLI
cd agent-backend
python cli.py

# 5. Follow CLI workflow (options 1-8)
```

### For Existing Setup (Quick Test)

```bash
# 1. Start Appium
appium

# 2. Start device
emulator -avd test_device  # Android
# or
open -a Simulator          # iOS

# 3. Run tests
cd mobile-tests
npm test           # Android
npm run test:ios   # iOS
```

---

## 🤝 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review test logs in `mobile-tests/logs/`
3. Check Appium logs
4. Verify device/simulator status

---

## 📝 Notes

- **iOS testing requires macOS** (Xcode limitation)
- **Real device testing** requires additional setup (certificates, provisioning)
- **BrowserStack** provides cloud-based device testing (no local setup needed)
- **AI features** require valid OpenAI API key
- **Test generation** quality depends on clear acceptance criteria

---

## 🔗 Useful Links

- [Appium Documentation](https://appium.io/docs/en/)
- [WebDriverIO Documentation](https://webdriver.io/)
- [Android Studio](https://developer.android.com/studio)
- [Xcode](https://developer.apple.com/xcode/)
- [BrowserStack](https://www.browserstack.com/)

---

**Last Updated:** December 2025

