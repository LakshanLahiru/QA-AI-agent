# Agent Backend - AI Test Generation Engine

Python backend that uses OpenAI to generate mobile test cases and automation scripts.

---

## 📋 Overview

The agent backend is the AI brain of the testing framework. It:

1. 🤖 Analyzes acceptance criteria
2. 🔍 Crawls mobile app UI elements
3. 📝 Generates human-readable manual test cases
4. 💻 Creates automated test scripts (Page Objects + Tests)
5. 🔧 Auto-heals failed tests by updating selectors
6. 📊 Orchestrates test execution and reporting

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Run CLI
python cli.py
```

---

## 📁 File Structure

```
agent-backend/
├── agent.py              # Core AI agent (TestGenerationAgent)
├── cli.py                # Command-line interface
├── device_manager.py     # Device/simulator management
├── run_cli.py           # Simple CLI launcher
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

---

## 🔑 Configuration

### Environment Variables

Create `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Optional - BrowserStack
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

### OpenAI API Key

1. Sign up: https://platform.openai.com/
2. Go to API Keys: https://platform.openai.com/api-keys
3. Create new secret key
4. Copy and add to `.env` file

---

## 🛠️ Components

### 1. TestGenerationAgent (`agent.py`)

The core AI engine that generates tests.

**Key Methods:**

```python
# Generate manual test cases from criteria
manual_tests = agent.generate_manual_tests(
    acceptance_criteria={...},
    page_elements=[...]
)

# Generate Page Object Model
page_object = agent.generate_page_object(
    page_name="login",
    page_elements=[...],
    acceptance_criteria={...}
)

# Generate test scripts
test_script = agent.generate_test_script(
    page_name="login",
    page_object_code="...",
    manual_tests={...}
)

# Auto-heal failed tests
healed_code = agent.auto_heal_test(
    test_code="...",
    error_message="element not found",
    page_elements=[...]
)
```

**Configuration:**

```python
agent = TestGenerationAgent(
    openai_api_key="sk-...",
    model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo"
    temperature=0.7,
    max_tokens=4000
)
```

### 2. DeviceManager (`device_manager.py`)

Manages Android emulators and iOS simulators.

**Key Methods:**

```python
device_manager = DeviceManager()

# List available devices
android_devices = device_manager.list_android_emulators()
ios_devices = device_manager.list_ios_simulators()

# Check device status
is_booted = device_manager.is_ios_simulator_booted(device_id)
is_online = device_manager.is_android_emulator_online(device_name)

# Control devices
device_manager.boot_ios_simulator(device_id)
device_manager.start_android_emulator(avd_name)
```

### 3. CLI (`cli.py`)

Interactive command-line interface for the complete workflow.

**Features:**
- Platform and device selection
- App configuration
- Acceptance criteria input
- Page crawling
- Test generation
- Test execution
- Report generation
- Auto-healing

**Usage:**

```bash
python cli.py
```

---

## 🔄 Workflow

### 1. Select Platform and Device

```python
# Lists available Android emulators or iOS simulators
# User selects platform and device
# Stores selection for subsequent steps
```

### 2. Configure App

```python
# Prompts for:
# - App path (.apk for Android, .app for iOS)
# - Package name / Bundle ID
# - Main activity (Android only)
# Saves to mobile-tests/.app_config.env
```

### 3. Add Acceptance Criteria

```python
# User inputs:
# - Page name (e.g., "login", "home")
# - Feature name
# - Test descriptions

# Saves to: mobile-tests/acceptance-criteria/{page}.json
```

**Example Output:**

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
      "description": "User can enter credentials"
    }
  ]
}
```

### 4. Crawl Page Elements

```python
# Launches app on selected device
# Navigates to specified page (if auto-nav available)
# Extracts UI element tree using driver.getPageSource()
# Saves XML to: mobile-tests/crawls/{page}.xml
```

**Auto-Navigation Support:**
- `login` - Clicks Login tab
- `signup` - Navigates to sign up screen
- `forms` - Clicks Forms tab
- `swipe` - Clicks Swipe tab
- `text` - Clicks Text Button
- Other pages - Manual navigation

### 5. Generate Manual Test Cases

```python
# AI analyzes:
# - Acceptance criteria
# - Crawled UI elements
# - Best testing practices

# Generates:
# - Human-readable test steps
# - Expected results
# - Test data requirements

# Saves to: mobile-tests/manual-tests/{page}_manual.json
```

**Example Output:**

```json
{
  "page": "login",
  "manualTests": [
    {
      "id": "LOGIN_001",
      "title": "Verify login form display",
      "priority": "high",
      "steps": [
        "1. Launch the app",
        "2. Navigate to Login screen",
        "3. Observe the login form"
      ],
      "expectedResult": "Login form with email and password fields is displayed",
      "testData": "N/A"
    }
  ]
}
```

### 6. Generate Test Scripts

```python
# AI generates:
# 1. Page Object Model class
#    - Element selectors from crawl
#    - Helper methods for interactions
#    - Cross-platform support

# 2. Test specification
#    - Test cases based on manual tests
#    - Proper assertions
#    - Error handling

# Saves to:
# - mobile-tests/src/pageobjects/{Page}Page.ts
# - mobile-tests/src/tests/{page}.e2e.ts
```

**Generated Page Object Example:**

```typescript
class LoginPage {
    public get emailInput() {
        return $('~input-email');
    }

    public get passwordInput() {
        return $('~input-password');
    }

    public get loginButton() {
        return $('~button-LOGIN');
    }

    public async login(email: string, password: string) {
        await this.emailInput.setValue(email);
        await this.passwordInput.setValue(password);
        await this.loginButton.click();
    }
}
```

### 7. Execute Tests

```python
# Checks if Appium is running (starts if needed)
# Verifies device is ready
# Runs WebDriverIO tests
# Collects results for reporting
```

### 8. Generate Allure Report

```python
# Generates HTML report from test results
# Opens report in default browser
# Report includes:
# - Test execution status
# - Screenshots
# - Logs
# - Timeline
# - Statistics
```

### 9. Run Complete Workflow

Executes steps 3-8 automatically in sequence.

---

## 🤖 AI Prompts

The agent uses carefully crafted prompts to generate high-quality tests.

### Manual Test Generation Prompt

```python
"""
You are an expert QA engineer. Given:
- Acceptance criteria
- UI elements from mobile app
Generate detailed manual test cases with:
- Clear steps
- Expected results
- Test data
- Priority
"""
```

### Page Object Generation Prompt

```python
"""
You are an expert mobile automation engineer. Given:
- Page name
- UI elements
- Acceptance criteria
Generate a Page Object Model class with:
- Element selectors (accessibility IDs preferred)
- Helper methods
- Cross-platform support (iOS/Android)
- TypeScript with proper types
"""
```

### Test Script Generation Prompt

```python
"""
Given:
- Manual test cases
- Page Object Model
Generate WebDriverIO test specs with:
- Mocha framework
- Chai assertions
- Proper error handling
- Clear test descriptions
"""
```

### Auto-Heal Prompt

```python
"""
Given:
- Current test code
- Error message
- Available UI elements
Fix the test by:
- Updating incorrect selectors
- Adding missing waits
- Handling new UI flows
"""
```

---

## 📊 Data Flow

```
┌─────────────────────┐
│  User Input (CLI)   │
│  - Criteria         │
│  - Page name        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Crawl Page         │
│  - Launch app       │
│  - Extract elements │
│  - Save XML         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AI Agent           │
│  - Analyze elements │
│  - Generate tests   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Generated Files    │
│  - Manual tests     │
│  - Page objects     │
│  - Test scripts     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Execute Tests      │
│  - WebDriverIO      │
│  - Appium           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Allure Report      │
│  - Results          │
│  - Screenshots      │
└─────────────────────┘
```

---

## 🔧 Customization

### Change AI Model

```python
# In agent.py or CLI initialization
agent = TestGenerationAgent(
    openai_api_key=api_key,
    model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo" for cheaper
    temperature=0.5,  # Lower = more consistent, Higher = more creative
    max_tokens=4000
)
```

### Add Custom Page Navigation

Edit `mobile-tests/src/tests/crawl-page.e2e.ts`:

```typescript
} else if (pageName.toLowerCase() === 'mypage') {
    try {
        await driver.pause(2000);
        const myButton = await $('~My Button');
        await myButton.waitForDisplayed({ timeout: 10000 });
        await myButton.click();
        await driver.pause(2000);
        console.log('Navigated to My Page');
    } catch (error) {
        console.log('Could not navigate to My Page');
    }
}
```

### Modify Test Templates

The AI generates code based on examples and context. To change the output:

1. Modify prompts in `agent.py`
2. Update examples in prompts
3. Add more context about your app structure

---

## 🐛 Debugging

### Enable Verbose Logging

```python
# In cli.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

```python
# Test agent directly
from agent import TestGenerationAgent

agent = TestGenerationAgent(openai_api_key="sk-...")

# Test manual test generation
manual_tests = agent.generate_manual_tests(
    acceptance_criteria={...},
    page_elements=[...]
)
print(manual_tests)
```

### Check Device Manager

```python
from device_manager import DeviceManager

dm = DeviceManager()

# List devices
print("Android:", dm.list_android_emulators())
print("iOS:", dm.list_ios_simulators())
```

---

## ⚡ Performance

### API Usage

- **Manual test generation**: ~500-1000 tokens
- **Page object generation**: ~1000-2000 tokens
- **Test script generation**: ~1500-3000 tokens
- **Auto-healing**: ~800-1500 tokens

**Cost Estimate (GPT-4):**
- Complete workflow: ~$0.20-0.40 per page
- Manual tests only: ~$0.05-0.10

### Speed

- Manual test generation: 5-10 seconds
- Page object generation: 10-15 seconds
- Test script generation: 15-20 seconds
- Complete workflow: 40-60 seconds

### Optimization Tips

1. **Use GPT-3.5** for faster/cheaper generation (quality trade-off)
2. **Cache results** - Don't regenerate if criteria unchanged
3. **Batch pages** - Generate multiple pages in one session
4. **Prune elements** - Remove irrelevant UI elements before sending to AI

---

## 🚨 Error Handling

### OpenAI API Errors

```python
try:
    tests = agent.generate_manual_tests(...)
except openai.AuthenticationError:
    print("Invalid API key")
except openai.RateLimitError:
    print("Rate limit exceeded, wait and retry")
except openai.APIError as e:
    print(f"OpenAI API error: {e}")
```

### Device Errors

```python
try:
    device_manager.boot_ios_simulator(device_id)
except subprocess.CalledProcessError:
    print("Failed to boot simulator")
```

### File System Errors

All file operations use pathlib and handle missing directories:

```python
ACCEPTANCE_CRITERIA_DIR.mkdir(parents=True, exist_ok=True)
```

---

## 📝 API Reference

### TestGenerationAgent

```python
class TestGenerationAgent:
    def __init__(self, openai_api_key: str, model: str = "gpt-4-turbo-preview", temperature: float = 0.7, max_tokens: int = 4000)
    
    def generate_manual_tests(self, acceptance_criteria: Dict, page_elements: List[Dict]) -> Dict
    
    def generate_page_object(self, page_name: str, page_elements: List[Dict], acceptance_criteria: Dict) -> str
    
    def generate_test_script(self, page_name: str, page_object_code: str, manual_tests: Dict) -> str
    
    def auto_heal_test(self, test_code: str, error_message: str, page_elements: List[Dict]) -> str
```

### DeviceManager

```python
class DeviceManager:
    def list_android_emulators(self) -> List[Dict[str, str]]
    
    def list_ios_simulators(self) -> List[Dict[str, str]]
    
    def is_android_emulator_online(self, device_name: str) -> bool
    
    def is_ios_simulator_booted(self, device_id: str) -> bool
    
    def boot_ios_simulator(self, device_id: str) -> bool
    
    def start_android_emulator(self, avd_name: str) -> subprocess.Popen
```

---

## 🧪 Testing

### Run Unit Tests

```bash
# TODO: Add unit tests
pytest tests/
```

### Manual Testing

```bash
# Test CLI
python cli.py

# Test agent directly
python
>>> from agent import TestGenerationAgent
>>> agent = TestGenerationAgent(openai_api_key="sk-...")
>>> # ... test methods
```

---

## 🔗 Dependencies

```
openai>=1.0.0          # OpenAI API client
python-dotenv>=1.0.0   # Environment variables
requests>=2.31.0       # HTTP requests
```

Install all:

```bash
pip install -r requirements.txt
```

---

## 📚 Further Reading

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [WebDriverIO Documentation](https://webdriver.io/)
- [Appium Documentation](https://appium.io/docs/en/)

---

**For complete project documentation, see:** `../README.md`

