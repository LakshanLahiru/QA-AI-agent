# Configuration Guide

Complete guide to configuring the QA AI Agent framework.

---

## 🔑 API Keys and Credentials

### OpenAI API Key (Required)

**Step 1: Get API Key**
1. Sign up at https://platform.openai.com/
2. Go to API Keys: https://platform.openai.com/api-keys
3. Click "Create new secret key"
4. Copy the key (it will only be shown once!)

**Step 2: Configure**

Create `agent-backend/.env` file:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Example:**
```bash
OPENAI_API_KEY=sk-proj-abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx1234yz
```

**Test Configuration:**
```bash
cd agent-backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', os.getenv('OPENAI_API_KEY')[:20] + '...')"
```

### BrowserStack Credentials (Optional)

For cloud device testing.

**Step 1: Get Credentials**
1. Sign up at https://www.browserstack.com/
2. Go to Settings: https://www.browserstack.com/accounts/settings
3. Copy Username and Access Key

**Step 2: Configure**

Add to `agent-backend/.env`:

```bash
BROWSERSTACK_USERNAME=your_username_here
BROWSERSTACK_ACCESS_KEY=your_access_key_here
```

**Example:**
```bash
BROWSERSTACK_USERNAME=johnsmith_abc123
BROWSERSTACK_ACCESS_KEY=xyz789def456ghi123
```

---

## 📱 Device Configuration

### Android Configuration

**File:** `mobile-tests/wdio.conf.ts`

#### 1. App Path

```typescript
const APP_PATH = 'C:/Users/LENOVO/Desktop/upwork/QA-AI-agent/mobile-tests/app/Android-NativeDemoApp-0.4.0.apk';
```

**Change to your app:**
```typescript
const APP_PATH = 'C:/path/to/your/app.apk';
```

**Get absolute path:**
```bash
# Windows
cd mobile-tests\app
echo %cd%\your-app.apk

# Mac/Linux
cd mobile-tests/app
realpath your-app.apk
```

#### 2. App Package

```typescript
const APP_PACKAGE = 'com.wdiodemoapp';
```

**Find your app's package:**
```bash
# Method 1: aapt (from Android SDK)
aapt dump badging your-app.apk | grep package

# Method 2: From app.apk
unzip -p your-app.apk AndroidManifest.xml | grep package

# Method 3: If app is installed
adb shell pm list packages | grep yourapp
```

**Change to your package:**
```typescript
const APP_PACKAGE = 'com.yourcompany.yourapp';
```

#### 3. Main Activity

```typescript
const APP_ACTIVITY = '.MainActivity';
```

**Find your main activity:**
```bash
# Method 1: aapt
aapt dump badging your-app.apk | grep activity

# Method 2: From installed app
adb shell dumpsys package com.yourpackage | grep -A 1 MAIN
```

**Common patterns:**
```typescript
const APP_ACTIVITY = '.MainActivity';           // Standard
const APP_ACTIVITY = '.SplashActivity';         // If has splash screen
const APP_ACTIVITY = '.ui.MainActivity';        // If in subfolder
const APP_ACTIVITY = 'com.company.app.MainActivity';  // Full path
```

#### 4. Device Name

```typescript
'appium:deviceName': 'emulator-5554',
```

**Find your device:**
```bash
adb devices
# Output: emulator-5554    device
```

**Change to your device:**
```typescript
'appium:deviceName': 'emulator-5554',  // For emulator
'appium:deviceName': '1234567890',     // For real device
```

#### 5. Platform Version

```typescript
'appium:platformVersion': '13.0',
```

**Find your device version:**
```bash
adb shell getprop ro.build.version.release
# Output: 13
```

**Change to match your device:**
```typescript
'appium:platformVersion': '13.0',  // Android 13
'appium:platformVersion': '12.0',  // Android 12
'appium:platformVersion': '11.0',  // Android 11
```

#### Complete Android Example

```typescript
const APP_PATH = 'C:/Projects/MyApp/app-release.apk';
const APP_PACKAGE = 'com.mycompany.myapp';
const APP_ACTIVITY = '.ui.MainActivity';

export const config = {
    capabilities: [{
        platformName: 'Android',
        'appium:automationName': 'UiAutomator2',
        'appium:deviceName': 'emulator-5554',
        'appium:platformVersion': '13.0',
        'appium:app': APP_PATH,
        'appium:appPackage': APP_PACKAGE,
        'appium:appActivity': APP_ACTIVITY,
        'appium:noReset': false,
        'appium:fullReset': false,
    }]
}
```

---

### iOS Configuration

**File:** `mobile-tests/wdio.ios.conf.ts`

#### 1. App Path

```typescript
const APP_PATH = '/Users/username/Desktop/upwork/QA-AI-agent/mobile-tests/app/iOS-Simulator-NativeDemoApp.app';
```

**Change to your app:**
```typescript
const APP_PATH = '/Users/username/path/to/YourApp.app';
```

**Note:** For iOS simulator, use `.app` folder (not .ipa)

**Get absolute path:**
```bash
cd mobile-tests/app
pwd
# Then append: /YourApp.app
```

#### 2. Bundle ID

```typescript
const BUNDLE_ID = 'org.reactjs.native.example.wdiodemoapp';
```

**Find your bundle ID:**
```bash
# Method 1: From .app folder
/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" YourApp.app/Info.plist

# Method 2: If app is installed
xcrun simctl listapps booted | grep -i yourapp
```

**Change to your bundle ID:**
```typescript
const BUNDLE_ID = 'com.yourcompany.yourapp';
```

#### 3. Device Name

```typescript
'appium:deviceName': 'iPhone 14',
```

**List available simulators:**
```bash
xcrun simctl list devices | grep Booted
# Or
xcrun simctl list devices available
```

**Change to your simulator:**
```typescript
'appium:deviceName': 'iPhone 14',      // iPhone 14
'appium:deviceName': 'iPhone 15 Pro',  // iPhone 15 Pro
'appium:deviceName': 'iPad Pro',       // iPad
```

#### 4. Platform Version

```typescript
'appium:platformVersion': '16.0',
```

**Find available versions:**
```bash
xcrun simctl list runtimes
```

**Change to match your simulator:**
```typescript
'appium:platformVersion': '17.0',  // iOS 17
'appium:platformVersion': '16.0',  // iOS 16
'appium:platformVersion': '15.0',  // iOS 15
```

#### Complete iOS Example

```typescript
const APP_PATH = '/Users/john/Projects/MyApp/MyApp.app';
const BUNDLE_ID = 'com.mycompany.myapp';

export const config = {
    capabilities: [{
        platformName: 'iOS',
        'appium:automationName': 'XCUITest',
        'appium:deviceName': 'iPhone 14',
        'appium:platformVersion': '16.0',
        'appium:app': APP_PATH,
        'appium:bundleId': BUNDLE_ID,
        'appium:noReset': false,
        'appium:autoAcceptAlerts': true,
    }]
}
```

---

## ⚙️ Appium Configuration

### Appium Server

**Default settings** (usually no changes needed):

```typescript
hostname: '127.0.0.1',
port: 4723,
path: '/',
```

**Change if Appium runs on different port:**

```typescript
hostname: '127.0.0.1',
port: 4724,  // If Appium started with: appium -p 4724
path: '/',
```

**For remote Appium server:**

```typescript
hostname: '192.168.1.100',  // Remote server IP
port: 4723,
path: '/',
```

---

## 🔧 Test Configuration

### Test Timeouts

**File:** `mobile-tests/wdio.conf.ts` or `wdio.ios.conf.ts`

```typescript
mochaOpts: {
    ui: 'bdd',
    timeout: 120000  // 120 seconds (2 minutes)
}
```

**Increase for slow tests:**
```typescript
timeout: 300000  // 5 minutes
```

### Element Wait Times

**In Page Objects:**

```typescript
await element.waitForDisplayed({ timeout: 5000 });  // 5 seconds
```

**Increase for slow apps:**
```typescript
await element.waitForDisplayed({ timeout: 15000 });  // 15 seconds
```

### Log Level

```typescript
logLevel: 'info',  // Options: trace, debug, info, warn, error, silent
```

**For debugging:**
```typescript
logLevel: 'debug',
```

---

## 📊 Reporting Configuration

### Allure Report

**File:** `mobile-tests/wdio.conf.ts`

```typescript
reporters: [
    'spec',
    ['allure', {
        outputDir: 'allure-results',
        disableWebdriverStepsReporting: false,
        disableWebdriverScreenshotsReporting: false
    }]
],
```

**Disable screenshots (for faster execution):**
```typescript
['allure', {
    outputDir: 'allure-results',
    disableWebdriverStepsReporting: false,
    disableWebdriverScreenshotsReporting: true  // Changed to true
}]
```

---

## 🌐 BrowserStack Configuration

**File:** `mobile-tests/wdio.browserstack.ios.conf.ts`

### 1. Upload App to BrowserStack

```bash
curl -u "USERNAME:ACCESS_KEY" \
  -X POST "https://api-cloud.browserstack.com/app-automate/upload" \
  -F "file=@/path/to/app.ipa"  # For iOS
  # or
  -F "file=@/path/to/app.apk"  # For Android
```

**Response:**
```json
{
  "app_url": "bs://abc123def456"
}
```

### 2. Configure App URL

```typescript
capabilities: [{
    'appium:app': 'bs://abc123def456',  // Use app_url from upload
    'bstack:options': {
        deviceName: 'iPhone 14',
        osVersion: '16',
        projectName: 'My App Tests',
        buildName: 'Build 1.0',
    }
}]
```

### 3. Configure Credentials

```typescript
user: process.env.BROWSERSTACK_USERNAME || 'your_username',
key: process.env.BROWSERSTACK_ACCESS_KEY || 'your_key',
```

**Better:** Use environment variables in `.env` file.

---

## 🎛️ AI Configuration

### Model Selection

**File:** `agent-backend/cli.py`

```python
self.agent = TestGenerationAgent(
    openai_api_key=api_key,
    model="gpt-4-turbo-preview",  # Default
    temperature=0.7,
    max_tokens=4000
)
```

**Options:**

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| `gpt-4-turbo-preview` | Slow | Best | High |
| `gpt-4` | Slow | Best | High |
| `gpt-3.5-turbo` | Fast | Good | Low |

**For faster/cheaper:**
```python
model="gpt-3.5-turbo",
```

### Temperature

Controls creativity vs consistency.

```python
temperature=0.7,  # Default
```

- **0.0-0.3**: Very consistent, deterministic
- **0.4-0.7**: Balanced (recommended)
- **0.8-1.0**: More creative, varied

**For consistent tests:**
```python
temperature=0.3,
```

### Max Tokens

Controls response length.

```python
max_tokens=4000,  # Default
```

**For longer responses:**
```python
max_tokens=8000,
```

---

## ✅ Verification

### Check Android Configuration

```bash
# Start emulator
emulator -avd YOUR_AVD_NAME

# Verify device
adb devices

# Check app package
adb shell pm list packages | grep yourpackage

# Test app installation
adb install -r /path/to/your-app.apk
```

### Check iOS Configuration

```bash
# List simulators
xcrun simctl list devices

# Boot simulator
xcrun simctl boot <DEVICE_ID>

# Test app installation
xcrun simctl install booted /path/to/YourApp.app

# Verify bundle ID
xcrun simctl listapps booted | grep yourbundle
```

### Check Appium

```bash
# Start Appium
appium

# Test connection (in another terminal)
curl http://127.0.0.1:4723/status
```

### Check OpenAI API

```bash
cd agent-backend
python -c "
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    models = openai.Model.list()
    print('✓ OpenAI API key is valid')
except Exception as e:
    print('✗ Error:', e)
"
```

---

## 📝 Configuration Files Summary

| File | Purpose | Required Changes |
|------|---------|------------------|
| `agent-backend/.env` | API keys | Add your OpenAI key |
| `mobile-tests/wdio.conf.ts` | Android config | App path, package, activity |
| `mobile-tests/wdio.ios.conf.ts` | iOS config | App path, bundle ID |
| `mobile-tests/wdio.browserstack.ios.conf.ts` | BrowserStack | App URL, credentials |

---

## 🚨 Common Configuration Errors

### Error: "App file not found"

**Cause:** Incorrect APP_PATH

**Fix:**
```typescript
// Use absolute path, not relative
const APP_PATH = 'C:/full/path/to/app.apk';  // ✓ Correct
const APP_PATH = '../app/my-app.apk';        // ✗ Wrong
```

### Error: "Package does not exist"

**Cause:** Wrong APP_PACKAGE or APP_ACTIVITY

**Fix:**
```bash
# Find correct package
aapt dump badging your-app.apk | grep package
```

### Error: "Unable to connect to Appium"

**Cause:** Appium not running or wrong port

**Fix:**
```bash
# Check if Appium is running
curl http://127.0.0.1:4723/status

# Or start Appium
appium
```

### Error: "OpenAI API key not found"

**Cause:** Missing or wrong .env file

**Fix:**
```bash
# Verify .env exists
ls -la agent-backend/.env

# Check content
cat agent-backend/.env
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use environment variables** in CI/CD
3. **Rotate API keys** regularly
4. **Use separate keys** for dev/staging/prod
5. **Limit API key permissions** if possible

---

For questions about configuration, refer to:
- **Main documentation**: `README.md`
- **Troubleshooting**: `README.md` → Troubleshooting section
- **Quick start**: `QUICK_START.md`

---

**Last Updated:** December 2025

