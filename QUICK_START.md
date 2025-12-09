# Quick Start Guide - 5 Minutes to First Test

Get your first mobile test running in 5 minutes!

---

## ✅ Prerequisites Check

Before starting, make sure you have:

- [ ] Node.js installed (`node --version`)
- [ ] Python installed (`python --version`)
- [ ] Java JDK installed (`java -version`)
- [ ] Android Studio OR Xcode (depending on platform)

---

## 🚀 Option 1: Android Setup (Windows/Mac/Linux)

### Step 1: Install Tools (5 min)

```bash
# Install Appium globally
npm install -g appium

# Install Android driver
appium driver install uiautomator2
```

### Step 2: Start Android Emulator (2 min)

```bash
# Open Android Studio → Device Manager → Create/Start Emulator
# Or command line:
emulator -list-avds
emulator -avd YOUR_AVD_NAME
```

### Step 3: Setup Project (3 min)

```bash
cd QA-AI-agent

# Install Python dependencies
cd agent-backend
pip install -r requirements.txt

# Install Node dependencies
cd ../mobile-tests
npm install
```

### Step 4: Configure App (1 min)

Edit `mobile-tests/wdio.conf.ts`:

```typescript
// Line 5-7: Update these paths
const APP_PATH = 'C:/Users/LENOVO/Desktop/upwork/QA-AI-agent/mobile-tests/app/Android-NativeDemoApp-0.4.0.apk';
const APP_PACKAGE = 'com.wdiodemoapp';
const APP_ACTIVITY = '.MainActivity';
```

### Step 5: Run Your First Test! (1 min)

```bash
# Terminal 1: Start Appium
appium

# Terminal 2: Run test
cd mobile-tests
npm test
```

🎉 **Done!** Your first test is running!

---

## 🍎 Option 2: iOS Setup (Mac Only)

### Step 1: Install Tools (5 min)

```bash
# Install Appium
npm install -g appium

# Install iOS driver
appium driver install xcuitest

# Install Xcode Command Line Tools
xcode-select --install
```

### Step 2: Start iOS Simulator (1 min)

```bash
# Open Simulator app
open -a Simulator

# Or command line:
xcrun simctl list devices
xcrun simctl boot <DEVICE_ID>
```

### Step 3: Setup Project (3 min)

```bash
cd QA-AI-agent

# Install Python dependencies
cd agent-backend
pip install -r requirements.txt

# Install Node dependencies
cd ../mobile-tests
npm install
```

### Step 4: Configure App (1 min)

Edit `mobile-tests/wdio.ios.conf.ts`:

```typescript
// Line 5-6: Update these
const APP_PATH = '/Users/YOUR_USERNAME/Desktop/upwork/QA-AI-agent/mobile-tests/app/iOS-Simulator-NativeDemoApp.app';
const BUNDLE_ID = 'org.reactjs.native.example.wdiodemoapp';
```

### Step 5: Run Your First Test! (1 min)

```bash
# Terminal 1: Start Appium
appium

# Terminal 2: Run test
cd mobile-tests
npm run test:ios
```

🎉 **Done!** Your first iOS test is running!

---

## 🤖 Use AI to Generate Tests (10 min)

### Step 1: Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key

### Step 2: Configure API Key

Create `.env` file in `agent-backend` folder:

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 3: Run CLI

```bash
cd agent-backend
python cli.py
```

### Step 4: Follow the Workflow

```
Select option: 9  (Run Complete Workflow)

Enter page name: home
Enter feature name: home page
Enter description: user wants to view home screen

Add more criteria? (y/n): n

Select Platform:
1. Android
2. iOS
Enter choice: 1  (or 2 for iOS)

[Select your device from the list]
```

The AI will now:
1. ✅ Crawl your app
2. ✅ Generate manual test cases
3. ✅ Generate test scripts
4. ✅ Run tests
5. ✅ Create Allure report

### Step 5: View Report

```bash
cd mobile-tests
npm run allure:open
```

🎉 **You just used AI to create and run tests!**

---

## 🎯 What Just Happened?

### Without AI:
1. ❌ Manually explore app
2. ❌ Write page objects
3. ❌ Write test cases
4. ❌ Debug selectors
5. ❌ Create assertions

⏱️ **Time: 2-3 hours**

### With AI:
1. ✅ Describe what you want to test
2. ✅ AI does everything else

⏱️ **Time: 5 minutes**

---

## 📋 Common First-Time Issues

### Issue: Appium won't start

```bash
# Error: Address already in use
# Solution: Kill existing process

# Windows:
taskkill /F /IM node.exe

# Mac/Linux:
killall node
```

### Issue: Device not detected

```bash
# Android:
adb devices
# Should show: emulator-5554    device

# iOS:
xcrun simctl list devices | grep Booted
# Should show booted device
```

### Issue: App won't install

```bash
# Android:
adb install -r mobile-tests/app/Android-NativeDemoApp-0.4.0.apk

# iOS:
xcrun simctl install booted mobile-tests/app/iOS-Simulator-NativeDemoApp.app
```

### Issue: Python module not found

```bash
cd agent-backend
pip install -r requirements.txt

# If still fails, try:
pip3 install -r requirements.txt
```

### Issue: Node modules not found

```bash
cd mobile-tests
rm -rf node_modules package-lock.json
npm install
```

---

## 🎓 Next Steps

### Learn the CLI Workflow

The CLI has 10 options that form a complete testing workflow:

1. **Select Platform** → Choose Android or iOS
2. **Configure App** → Set app path
3. **Add Acceptance Criteria** → Define what to test
4. **Crawl Page** → Extract UI elements
5. **Generate Manual Tests** → AI creates test cases
6. **Generate Scripts** → AI creates code
7. **Execute Tests** → Run tests
8. **Generate Report** → View results
9. **Run Complete Workflow** → Do all steps at once
10. **Exit** → Quit

### Try Different Pages

Test different screens in your app:

```bash
python cli.py
# Option 4: Crawl Page Elements
# Try: login, home, signup, settings, etc.
```

### Customize Tests

Generated tests are in:
- Page Objects: `mobile-tests/src/pageobjects/`
- Test Specs: `mobile-tests/src/tests/`

You can edit them to add custom logic!

### Run Tests Continuously

```bash
# Watch mode (re-run on changes)
npm test -- --watch

# Run specific test
npm test -- --spec src/tests/login.e2e.ts
```

---

## 💡 Pro Tips

### Tip 1: Keep Appium Running

Start Appium once and keep it running:

```bash
# Terminal 1 (keep open)
appium

# Terminal 2 (run tests here)
cd mobile-tests
npm test
```

### Tip 2: Use BrowserStack for Cloud Testing

No emulator needed! Tests run in the cloud:

```bash
# Add to agent-backend/.env
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_key

# Run on BrowserStack
cd mobile-tests
npm run test:browserstack:ios
```

### Tip 3: View Logs

If tests fail, check logs:

```bash
# Test logs
cat mobile-tests/logs/wdio.log

# Appium logs (from terminal where Appium is running)
```

### Tip 4: Take Screenshots

Add to your tests:

```typescript
await driver.saveScreenshot('./debug.png');
```

### Tip 5: Use Allure for Better Reports

```bash
npm run allure:open
```

Better than terminal output! Shows:
- Screenshots
- Step-by-step execution
- Pass/fail statistics
- Test history

---

## 🎉 Congratulations!

You've successfully:
- ✅ Set up mobile test automation
- ✅ Run your first test
- ✅ Used AI to generate tests
- ✅ Viewed test reports

### Ready for More?

Read the full documentation:
- **Complete Setup**: See `README.md`
- **Test Framework**: See `mobile-tests/README.md`
- **AI Agent**: See `agent-backend/README.md`

### Need Help?

Check the **Troubleshooting** section in `README.md`

---

## 🚀 What's Next?

### Add Your Own App

1. Replace the demo app in `mobile-tests/app/`
2. Update `wdio.conf.ts` with your app's package/bundle ID
3. Run CLI workflow to generate tests

### Test Real Features

1. Navigate to your app's main screens
2. Define acceptance criteria
3. Let AI generate tests
4. Run and iterate

### Integrate with CI/CD

Add to GitHub Actions, Jenkins, etc.:

```yaml
# .github/workflows/mobile-tests.yml
- name: Run tests
  run: |
    appium &
    cd mobile-tests
    npm test
```

---

**Time to build something awesome! 🚀**

