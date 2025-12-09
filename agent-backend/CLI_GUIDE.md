# CLI Guide for AI Agent

## Overview

The CLI (Command Line Interface) provides an interactive way to use the AI Agent for Mobile Webdriver. It replaces the previous FastAPI/Swagger interface with a user-friendly command-line workflow.

## Setup

1. **Install dependencies:**
   ```bash
   cd agent-backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the `agent-backend` directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here  # Optional
   ```

## Running the CLI

**Windows:**
```powershell
cd agent-backend
python run_cli.py
```

**Linux/Mac:**
```bash
cd agent-backend
python3 run_cli.py
```

Or directly:
```bash
python cli.py
```

## Workflow

### Main Menu Options

1. **Add Acceptance Criteria** - Enter acceptance criteria for a page/feature
2. **Select Platform and Device** - Choose Android/iOS and specific device/emulator
3. **Crawl Page Elements** - Extract UI elements from the app
4. **Generate Manual Test Cases** - Create manual test cases from acceptance criteria
5. **Review Manual Test Cases** - Review and modify manual test cases
6. **Generate Test Scripts** - Generate POM and automated test scripts
7. **Review Test Scripts** - Review and modify generated scripts
8. **Execute Tests** - Run automated tests on connected device/emulator
9. **Generate Allure Report** - Create HTML test report
10. **Auto-Heal Failed Tests** - Automatically fix failing tests
11. **Run Complete Workflow** - Execute all steps in sequence
12. **Exit** - Exit the CLI

### Complete Workflow Example

1. **Start the CLI:**
   ```bash
   python run_cli.py
   ```

2. **Add Acceptance Criteria (Option 1):**
   - Enter page name (e.g., `login`)
   - Enter feature name (e.g., `User Login`)
   - Enter acceptance criteria:
     - Criterion ID (e.g., `LOGIN_001`)
     - Description
     - Preconditions (optional)
     - Steps (optional)
     - Expected Result
   - Add more criteria or finish

3. **Select Platform and Device (Option 2):**
   - Choose Android or iOS
   - Select from detected devices/emulators
   - The system will automatically update WebdriverIO configuration

4. **Crawl Page Elements (Option 3):**
   - Ensure Appium server is running (port 4723)
   - Launch your app on the selected device/emulator
   - Navigate to the page you want to crawl
   - Press Enter to start crawling
   - Elements will be saved to `mobile-tests/crawls/{page}.xml`

5. **Generate Manual Test Cases (Option 4):**
   - The AI agent generates manual test cases
   - Saved to `mobile-tests/manual-tests/{page}_manual.json`

6. **Review Manual Test Cases (Option 5):**
   - Review the generated manual test cases
   - Option to edit manually if needed

7. **Generate Test Scripts (Option 6):**
   - Generates Page Object Model (POM) class
   - Generates automated test scripts
   - Uses crawled elements and acceptance criteria

8. **Review Test Scripts (Option 7):**
   - Review generated POM and test files
   - Option to edit manually if needed

9. **Execute Tests (Option 8):**
   - Run tests on the connected device/emulator
   - Ensure Appium server is running
   - Tests execute and results are saved

10. **Generate Allure Report (Option 9):**
    - Creates HTML report from test results
    - Report saved to `mobile-tests/allure-report/`

11. **Auto-Heal (Option 10):**
    - If tests fail, use this option to:
      - Re-crawl page elements
      - Regenerate POM with updated selectors
      - Re-run tests

### Quick Start: Complete Workflow (Option 11)

Select option 11 to run the complete workflow automatically:
- Prompts for acceptance criteria
- Device selection
- Crawling
- Manual test generation
- Review steps
- Script generation
- Review steps
- Test execution
- Report generation
- Auto-healing if tests fail

## Features

### Multiple Acceptance Criteria Support
- Add multiple acceptance criteria for the same page
- New criteria are appended, not replaced
- Existing test scripts are preserved

### Device Detection
- **Android:** Automatically detects connected devices and running emulators via `adb`
- **iOS:** Detects iOS simulators and connected devices (macOS only)

### Smart Code Generation
- Uses crawled XML to extract real selectors
- Merges new code with existing code (doesn't overwrite)
- Follows Page Object Model best practices

### Manual Execution
After scripts are generated, you can run them manually:
```bash
cd mobile-tests
npm test
# or
npx wdio run wdio.conf.ts
```

## Troubleshooting

### Device Not Detected
- **Android:** 
  - Ensure USB debugging is enabled
  - Run `adb devices` to verify connection
  - For emulator, ensure it's running
- **iOS:**
  - Ensure Xcode is installed (macOS only)
  - For simulator, ensure it's booted
  - For device, ensure proper provisioning

### Appium Connection Issues
- Ensure Appium server is running: `appium`
- Check port 4723 is available
- Verify device is connected and authorized

### Test Execution Fails
- Check WebdriverIO configuration in `wdio.conf.ts`
- Verify app path is correct
- Ensure device/emulator is still connected
- Check Appium logs for errors

## File Structure

```
mobile-ai-agent/
├── agent-backend/
│   ├── cli.py              # Main CLI interface
│   ├── agent.py            # AI agent logic
│   ├── device_manager.py   # Device detection
│   ├── run_cli.py          # Entry point
│   └── requirements.txt
└── mobile-tests/
    ├── acceptance-criteria/  # Saved acceptance criteria
    ├── crawls/              # Crawled page XML files
    ├── manual-tests/        # Generated manual test cases
    ├── src/
    │   ├── pageobjects/     # Generated POM classes
    │   └── tests/           # Generated test scripts
    └── allure-results/      # Test execution results
```

## Notes

- The CLI maintains state during a session (current page, device, etc.)
- All generated files follow naming conventions based on page names
- Multiple acceptance criteria for the same page are merged intelligently
- Test scripts can be run manually anytime after generation

