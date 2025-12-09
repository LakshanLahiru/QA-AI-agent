# Project Handover Document

**Project:** QA AI Agent - Mobile Test Automation Framework  
**Date:** December 2025  
**Version:** 1.0

---

## 📋 Project Overview

This is an AI-powered mobile test automation framework that automatically generates and executes tests for iOS and Android applications. It uses OpenAI's GPT models to create test cases from acceptance criteria and WebDriverIO + Appium for test execution.

---

## 🎯 Key Features

✅ **AI Test Generation** - Converts acceptance criteria into working test code  
✅ **Cross-Platform** - Supports both iOS and Android  
✅ **Page Object Model** - Generates maintainable, structured code  
✅ **Auto-Healing** - Fixes broken tests automatically  
✅ **Visual Reports** - Allure reports with screenshots  
✅ **Cloud Testing** - BrowserStack integration included  
✅ **CLI Interface** - User-friendly command-line workflow  

---

## 📁 Project Structure

```
QA-AI-agent/
├── agent-backend/              # Python AI engine
│   ├── agent.py               # Core AI logic
│   ├── cli.py                 # Command-line interface
│   ├── device_manager.py      # Device/simulator management
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # API keys (not in git)
│   └── README.md
│
├── mobile-tests/              # WebDriverIO test framework
│   ├── src/
│   │   ├── pageobjects/      # Page Object Models (generated)
│   │   └── tests/            # Test specs (generated)
│   ├── crawls/               # Crawled UI elements (XML)
│   ├── acceptance-criteria/  # Test requirements (JSON)
│   ├── manual-tests/         # Manual test cases (generated)
│   ├── allure-results/       # Test execution results
│   ├── allure-report/        # HTML reports
│   ├── app/                  # Test applications
│   ├── wdio.conf.ts          # Android configuration
│   ├── wdio.ios.conf.ts      # iOS configuration
│   ├── package.json
|   ├── .env  
│   └── README.md
│
├── README.md                  # Main documentation
├── QUICK_START.md            # 5-minute setup guide
└── HANDOVER.md               # This file
```

---

## 🚀 Getting Started

### 1. Prerequisites

- **Node.js** v18+ (https://nodejs.org/)
- **Python** 3.8+ (https://python.org/)
- **Java JDK** 11+ (https://www.oracle.com/java/)
- **Appium** 2.0+ (`npm install -g appium`)
- **Android Studio** (for Android) or **Xcode** (for iOS, Mac only)

### 2. Installation

```bash
# Install Python dependencies
cd agent-backend
pip install -r requirements.txt

# Install Node dependencies
cd ../mobile-tests
npm install

# Install Appium drivers
appium driver install uiautomator2  # Android
appium driver install xcuitest      # iOS
```

### 3. Configuration

```bash
# Create .env file in agent-backend/
echo "OPENAI_API_KEY=your-key-here" > agent-backend/.env
```

Get OpenAI API key: https://platform.openai.com/api-keys

### 4. Quick Test

```bash
# Terminal 1: Start Appium
appium

# Terminal 2: Start Android emulator
emulator -avd YOUR_AVD_NAME

# Terminal 3: Run tests
cd mobile-tests
npm test
```

**See `QUICK_START.md` for detailed setup!**

---

## 🔄 Complete Workflow

### Using the CLI (Recommended)

```bash
cd agent-backend
python cli.py
```

**Menu Options:**
1. **Select Platform and Device** - Choose iOS or Android
2. **Configure App** - Set app path and package details
3. **Add Acceptance Criteria** - Define what to test
4. **Crawl Page Elements** - Extract UI elements
5. **Generate Manual Test Cases** - AI creates test steps
6. **Generate Test Scripts** - AI creates automation code
7. **Execute Tests** - Run the generated tests
8. **Generate Allure Report** - View results
9. **Run Complete Workflow** - Do all steps automatically
10. **Exit**

### Example Flow

```
1. Select iOS, choose iPhone 14 simulator
2. Configure app path: /path/to/app.app
3. Add criteria:
   - Page: login
   - Feature: authentication
   - Description: user can login with valid credentials
4. Crawl login page (extracts all UI elements)
5. Generate manual tests (AI creates test cases)
6. Generate test scripts (AI creates code)
7. Execute tests (runs automatically)
8. View Allure report (opens in browser)
```

**Time: ~5 minutes**  
**Output:** Fully working automated tests

---

## 🔑 Important Files

### Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| `.env` | API keys | `agent-backend/.env` |
| `wdio.conf.ts` | Android config | `mobile-tests/wdio.conf.ts` |
| `wdio.ios.conf.ts` | iOS config | `mobile-tests/wdio.ios.conf.ts` |
| `.app_config.env` | App config (generated) | `mobile-tests/.app_config.env` |

### Generated Files

| File | Content | Created By |
|------|---------|------------|
| `{page}.json` | Acceptance criteria | User input (CLI) |
| `{page}.xml` | Crawled UI elements | Crawl step |
| `{page}_manual.json` | Manual test cases | AI generation |
| `{Page}Page.ts` | Page Object Model | AI generation |
| `{page}.e2e.ts` | Test specification | AI generation |

---

## 🎯 Use Cases

### Use Case 1: Test Existing App

1. Launch CLI: `python cli.py`
2. Option 2: Configure your app path
3. Option 3: Define test scenarios
4. Option 9: Run complete workflow
5. Done! Tests are generated and executed

### Use Case 2: Add New Test to Existing Page

1. Edit `acceptance-criteria/{page}.json` - add new criteria
2. Option 6: Re-generate test scripts
3. Option 7: Execute tests

### Use Case 3: Fix Broken Tests

**Manual Fix:**
1. Edit `src/pageobjects/{Page}Page.ts`
2. Update selectors
3. Re-run tests

**Auto-Heal (Future):**
1. Option 10: Auto-heal failed tests
2. AI automatically fixes selectors

### Use Case 4: Test on BrowserStack

```bash
# Configure .env
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_key

# Run on cloud
cd mobile-tests
npm run test:browserstack:ios
```

---

## 🧪 Testing Different Devices

### Android Devices

```bash
# List emulators
emulator -list-avds

# Start emulator
emulator -avd Pixel_6_API_33

# Or use CLI option 1 to select device
```

### iOS Devices

```bash
# List simulators
xcrun simctl list devices

# Boot simulator
xcrun simctl boot <DEVICE_ID>

# Or use CLI option 1 to select device
```

---

## 📊 Reports and Logs

### Allure Reports

**Location:** `mobile-tests/allure-report/index.html`

**Generate & Open:**
```bash
cd mobile-tests
npm run allure:open
```

**Contains:**
- Test execution status (pass/fail)
- Screenshots on failure
- Step-by-step logs
- Execution timeline
- Test statistics

### Test Logs

**Location:** `mobile-tests/logs/wdio.log`

### Appium Logs

Visible in terminal where Appium is running

---

## 🐛 Common Issues & Solutions

### Issue 1: Tests Can't Find Elements

**Symptom:** `element not found after 5000ms`

**Solution:**
```bash
# Re-crawl the page to get current selectors
cd agent-backend
python cli.py
# Option 4: Crawl Page Elements
```

### Issue 2: Appium Won't Start

**Symptom:** `EADDRINUSE: address already in use`

**Solution:**
```bash
# Windows
taskkill /F /IM node.exe

# Mac/Linux
killall node
```

### Issue 3: Device Not Detected

**Android:**
```bash
adb devices
# Should show: emulator-5554    device

# If not:
adb kill-server
adb start-server
```

**iOS:**
```bash
xcrun simctl list devices | grep Booted
# Should show booted simulator

# If not:
xcrun simctl boot <DEVICE_ID>
```

### Issue 4: App Won't Install

**Android:**
```bash
adb uninstall com.wdiodemoapp
adb install /path/to/app.apk
```

**iOS:**
```bash
xcrun simctl uninstall booted org.reactjs.native.example.wdiodemoapp
xcrun simctl install booted /path/to/app.app
```

### Issue 5: AI Generation Fails

**Check:**
1. Valid OpenAI API key in `.env`
2. Sufficient API credits
3. Internet connection
4. Check `agent-backend/cli.py` logs for errors

**Solution:**
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 💰 Costs

### OpenAI API Usage

**Per page workflow:**
- GPT-4: ~$0.30-0.50
- GPT-3.5: ~$0.05-0.10

**Monthly estimate (20 pages):**
- GPT-4: ~$6-10/month
- GPT-3.5: ~$1-2/month

**To reduce costs:**
1. Use GPT-3.5 instead of GPT-4
2. Don't regenerate unchanged pages
3. Cache generated results

---

## 🔧 Customization

### Change AI Model

Edit `agent-backend/cli.py`:

```python
self.agent = TestGenerationAgent(
    openai_api_key=api_key,
    model="gpt-3.5-turbo",  # Change this
    temperature=0.7,
    max_tokens=4000
)
```

### Add Custom Page Navigation

Edit `mobile-tests/src/tests/crawl-page.e2e.ts`:

```typescript
} else if (pageName.toLowerCase() === 'your-page') {
    try {
        await driver.pause(2000);
        const btn = await $('~Your Button');
        await btn.waitForDisplayed({ timeout: 10000 });
        await btn.click();
        await driver.pause(2000);
    } catch (error) {
        console.log('Navigation failed');
    }
}
```

### Modify Test Templates

The AI generates based on examples in prompts. To change output style:
1. Edit prompts in `agent-backend/agent.py`
2. Update examples to match your preferred format
3. Regenerate tests

---

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| `README.md` | Complete setup & reference | All users |
| `QUICK_START.md` | 5-minute quick start | New users |
| `HANDOVER.md` | Project handover | Developers taking over |
| `mobile-tests/README.md` | Test framework details | Test engineers |
| `agent-backend/README.md` | AI engine details | Backend developers |
| `TEST_FAILURE_FIX.md` | Debugging guide | When tests fail |

---

## 🔐 Security Notes

### Sensitive Files (DO NOT COMMIT)

```
agent-backend/.env              # Contains API keys
mobile-tests/.app_config.env    # May contain paths
*.log                           # May contain sensitive data
allure-results/                 # May contain screenshots
allure-report/                  # May contain screenshots
```

### .gitignore Already Configured

The `.gitignore` file already excludes:
- `.env` files
- `node_modules/`
- `allure-results/`, `allure-report/`
- Log files
- Python cache

### API Key Management

- Store OpenAI key in `.env` only
- Never hardcode in source files
- Rotate keys periodically
- Use separate keys for dev/prod

---

## 🚀 Deployment

### CI/CD Integration

**GitHub Actions Example:**

```yaml
name: Mobile Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: macos-latest  # For iOS
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - name: Install dependencies
        run: |
          cd mobile-tests
          npm install
      - name: Start Appium
        run: appium &
      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          cd mobile-tests
          npm run test:ios
      - name: Generate report
        if: always()
        run: |
          cd mobile-tests
          npm run allure:generate
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: allure-report
          path: mobile-tests/allure-report
```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

**Weekly:**
- Review test results
- Update failing tests
- Check API usage costs

**Monthly:**
- Update dependencies (`npm update`, `pip install -U`)
- Review and update test coverage
- Clean up old reports

**As Needed:**
- Re-crawl pages when UI changes
- Update page objects for new features
- Regenerate tests for updated acceptance criteria

### Dependency Updates

```bash
# Update Node packages
cd mobile-tests
npm update

# Update Python packages
cd agent-backend
pip install --upgrade -r requirements.txt
```

### Troubleshooting Resources

1. **Check logs** - `mobile-tests/logs/wdio.log`
2. **Check Appium logs** - Terminal output
3. **Review README** - `README.md` Troubleshooting section
4. **Verify setup** - Run through `QUICK_START.md`
5. **Test components**:
   - Appium: `curl http://127.0.0.1:4723/status`
   - Device: `adb devices` or `xcrun simctl list`
   - App: Manual launch on device

---

## 🎓 Learning Resources

### For Test Engineers
1. Read `mobile-tests/README.md`
2. Learn WebDriverIO: https://webdriver.io/
3. Learn Appium: https://appium.io/docs/en/
4. Practice with CLI workflow

### For Backend Developers
1. Read `agent-backend/README.md`
2. Review `agent.py` core logic
3. Learn OpenAI API: https://platform.openai.com/docs
4. Experiment with prompt engineering

### For DevOps
1. Review BrowserStack setup
2. Check CI/CD examples
3. Learn Allure reporting: https://docs.qameta.io/allure/

---

## ✅ Handover Checklist

Before handing over, ensure:

- [ ] All documentation is up to date
- [ ] `.env.example` file exists (without actual keys)
- [ ] Sample test runs successfully
- [ ] All dependencies are documented
- [ ] Known issues are documented
- [ ] Contact information provided
- [ ] Access to necessary services (OpenAI, BrowserStack) is transferred
- [ ] Repository access granted
- [ ] Walkthrough session completed

---

## 📝 Next Steps for New Developer

### Day 1: Setup & Familiarization
1. ✅ Install prerequisites
2. ✅ Clone repository
3. ✅ Install dependencies
4. ✅ Configure `.env` file
5. ✅ Run sample test
6. ✅ Review documentation

### Day 2: Understand Workflow
1. ✅ Run complete CLI workflow
2. ✅ Examine generated files
3. ✅ Read through code
4. ✅ Try modifying a test
5. ✅ Generate Allure report

### Week 1: Hands-On
1. ✅ Test with your own app
2. ✅ Create custom acceptance criteria
3. ✅ Generate and run tests
4. ✅ Debug a failing test
5. ✅ Customize configuration

### Week 2: Advanced
1. ✅ Integrate with CI/CD
2. ✅ Set up BrowserStack
3. ✅ Customize AI prompts
4. ✅ Add custom page navigation
5. ✅ Implement new features

---

## 🤝 Contact Information

**Previous Developer:** [Your contact info]  
**Project Repository:** [Git repository URL]  
**OpenAI Account:** [Account owner/admin]  
**BrowserStack Account:** [Account owner/admin]  

---

## 📅 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2025 | Initial handover version |

---

## 🎉 Final Notes

This project is designed to significantly reduce the time and effort required for mobile test automation. The AI-powered approach allows non-technical stakeholders to contribute to test creation through simple acceptance criteria.

**Key Success Factors:**
- Clear, specific acceptance criteria = Better generated tests
- Regular page crawling = Up-to-date selectors
- Consistent workflow usage = Maintainable test suite

**The framework is production-ready and has been tested on:**
- ✅ iOS simulators (Xcode)
- ✅ Android emulators (Android Studio)
- ✅ BrowserStack cloud devices

Good luck with the project! 🚀

---

**Document Last Updated:** December 2025

