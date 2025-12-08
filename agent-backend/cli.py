#!/usr/bin/env python3
"""
CLI interface for AI Agent for Mobile Webdriver
Handles the complete workflow: acceptance criteria → crawl → manual tests → review → generate → execute → report
"""

import json
import os
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from agent import TestGenerationAgent
from device_manager import DeviceManager
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
MOBILE_TESTS_DIR = ROOT_DIR / "mobile-tests"
ACCEPTANCE_CRITERIA_DIR = MOBILE_TESTS_DIR / "acceptance-criteria"
APP_CONFIG_FILE = MOBILE_TESTS_DIR / ".app_config.env"

IS_WINDOWS = platform.system() == "Windows"


class CLI:
    def __init__(self):
        self.agent: Optional[TestGenerationAgent] = None
        self.device_manager = DeviceManager()
        self.current_page: Optional[str] = None
        self.current_platform: Optional[str] = None
        self.current_device: Optional[Dict[str, str]] = None
        self.app_path: Optional[str] = None
        self.app_package: Optional[str] = None
        self.app_activity: Optional[str] = None

    def print_header(self, text: str):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60 + "\n")

    def print_success(self, text: str):
        """Print success message"""
        print(f"✓ {text}")

    def print_error(self, text: str):
        """Print error message"""
        print(f"✗ {text}")

    def print_info(self, text: str):
        """Print info message"""
        print(f"ℹ {text}")

    def _check_node_available(self) -> Tuple[bool, str]:
        """Check if Node.js/npm is available"""
        try:
            if IS_WINDOWS:
                result = subprocess.run(
                    ["node", "--version"],
                    capture_output=True,
                    text=True,
                    check=False,
                    shell=True,
                )
            else:
                result = subprocess.run(
                    ["node", "--version"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            return False, "Node.js not found"
        except FileNotFoundError:
            return False, "Node.js not installed or not in PATH"

    def _get_npx_cmd(self) -> List[str]:
        """Get the correct npx command for the current OS"""
        if IS_WINDOWS:
            # Try npx.cmd first, fallback to npx
            return ["npx.cmd"] if self._check_node_available()[0] else ["npx"]
        return ["npx"]

    def initialize_agent(self):
        """Initialize the AI agent with API keys"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.print_error("OPENAI_API_KEY not found in environment variables.")
            self.print_info("Please set OPENAI_API_KEY in .env file or environment.")
            return False

        try:
            self.agent = TestGenerationAgent(openai_api_key=api_key)
            self.print_success("AI Agent initialized successfully")
            return True
        except Exception as e:
            self.print_error(f"Failed to initialize agent: {e}")
            return False

    def get_acceptance_criteria(self) -> Optional[Dict[str, Any]]:
        """Interactive CLI to get acceptance criteria from user"""
        self.print_header("Enter Acceptance Criteria")

        page = input("Enter page name (e.g., login, signup, home): ").strip().lower()
        if not page:
            self.print_error("Page name cannot be empty")
            return None

        feature = input("Enter feature name (e.g., User Login) or press Enter to use default: ").strip()
        if not feature:
            feature = f"{page.capitalize()} Feature"

        # Create acceptance criteria file name
        criteria_filename = f"acceptance_criteria_{page}.txt"
        criteria_file_path = ACCEPTANCE_CRITERIA_DIR / criteria_filename
        
        ACCEPTANCE_CRITERIA_DIR.mkdir(parents=True, exist_ok=True)

        print(f"\n✓ Acceptance criteria file will be saved as: {criteria_filename}")
        print("\nEnter acceptance criteria (one per line, press Enter on empty line to finish):")
        print("Example:")
        print("  - User should be able to see the title on login screen")
        print("  - User should be able to see the username field")
        print("  - User should be able to login after entering valid details\n")
        
        criteria_list = []
        criterion_num = 1

        while True:
            description = input(f"{criterion_num}. ").strip()
            if not description:
                if criterion_num == 1:
                    self.print_error("At least one criterion is required")
                    continue
                else:
                    break

            # Create simple criterion with auto-generated ID
            criterion = {
                "id": f"{page.upper()}_{criterion_num:03d}",
                "description": description,
            }
            criteria_list.append(criterion)
            criterion_num += 1

        if not criteria_list:
            self.print_error("No acceptance criteria provided")
            return None

        return {
            "page": page,
            "feature": feature,
            "acceptanceCriteria": criteria_list,
        }

    def save_acceptance_criteria(self, criteria: Dict[str, Any]) -> Path:
        """Save acceptance criteria to text file"""
        ACCEPTANCE_CRITERIA_DIR.mkdir(parents=True, exist_ok=True)
        page = criteria["page"]
        
        # Create filename: acceptance_criteria_<pagename>.txt
        file_path = ACCEPTANCE_CRITERIA_DIR / f"acceptance_criteria_{page}.txt"
        
        # Create content
        content_lines = [
            f"PAGE: {page}",
            f"FEATURE: {criteria['feature']}",
            f"DATE: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "ACCEPTANCE CRITERIA:",
            "=" * 60,
        ]
        
        for idx, criterion in enumerate(criteria["acceptanceCriteria"], 1):
            content_lines.append(f"{idx}. {criterion['description']}")
        
        content_lines.append("")
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))

        # Also save as JSON for agent to process
        json_path = ACCEPTANCE_CRITERIA_DIR / f"{page}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(criteria, f, indent=2, ensure_ascii=False)

        self.print_success(f"Acceptance criteria saved to {file_path}")
        self.print_info(f"JSON format also saved to {json_path} (for processing)")
        return file_path

    def select_platform_and_device(self) -> bool:
        """Select platform (Android/iOS) and device/emulator"""
        self.print_header("Select Platform and Device")

        print("Select platform:")
        print("1. Android")
        print("2. iOS")
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            self.current_platform = "Android"
        elif choice == "2":
            self.current_platform = "iOS"
        else:
            self.print_error("Invalid choice")
            return False

        # Detect available devices
        devices = self.device_manager.detect_devices(self.current_platform)
        
        if not devices:
            self.print_error(f"No {self.current_platform} devices/emulators detected")
            self.print_info("Please ensure:")
            if self.current_platform == "Android":
                print("  - Android emulator is running, OR")
                print("  - Android device is connected via USB with USB debugging enabled")
            else:
                print("  - iOS Simulator is running, OR")
                print("  - iOS device is connected with proper provisioning")
            return False

        print(f"\nAvailable {self.current_platform} devices/emulators:")
        for idx, device in enumerate(devices, 1):
            device_type = "Emulator" if device.get("is_emulator") else "Device"
            print(f"{idx}. {device['name']} ({device_type}) - {device.get('version', 'Unknown version')}")

        device_choice = input(f"\nSelect device (1-{len(devices)}): ").strip()
        try:
            device_idx = int(device_choice) - 1
            if 0 <= device_idx < len(devices):
                self.current_device = devices[device_idx]
                self.print_success(f"Selected: {self.current_device['name']}")
                return True
            else:
                self.print_error("Invalid device selection")
                return False
        except ValueError:
            self.print_error("Invalid input")
            return False

    def crawl_page(self, page_name: str) -> bool:
        """Crawl elements from the current page"""
        self.print_header(f"Crawling Elements for {page_name}")

        if not self.current_device:
            self.print_error("No device selected. Please select a device first.")
            return False

        self.print_info(f"Connecting to {self.current_device['name']}...")
        
        # Update wdio config with selected device
        if not self.device_manager.update_wdio_config(self.current_device, self.current_platform):
            self.print_error("Failed to update WebdriverIO configuration")
            return False

        self.print_info("Starting page crawl...")
        self.print_info("Please ensure:")
        print("  - Appium server is running (port 4723)")
        print("  - The app is launched on the device/emulator")
        print("  - You are on the correct page/screen")

        input("\nPress Enter when ready to crawl...")

        # Check if Node.js is available
        node_available, node_info = self._check_node_available()
        if not node_available:
            self.print_error("Node.js is not installed or not in PATH")
            self.print_info("Please install Node.js from https://nodejs.org/")
            self.print_info("After installation, restart the CLI")
            return False

        env = os.environ.copy()
        env["CRAWL_PAGE_NAME"] = page_name

        # Get the correct npx command
        npx_cmd = self._get_npx_cmd()
        cmd = npx_cmd + ["wdio", "run", "wdio.conf.ts", "--spec", "./src/tests/crawl-page.e2e.ts"]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(MOBILE_TESTS_DIR),
                capture_output=True,
                text=True,
                check=False,
                env=env,
                shell=IS_WINDOWS,
            )

            if result.returncode == 0:
                crawl_file = MOBILE_TESTS_DIR / "crawls" / f"{page_name}.xml"
                if crawl_file.exists():
                    self.print_success(f"Page elements crawled and saved to {crawl_file}")
                    return True
                else:
                    self.print_error("Crawl completed but file not found")
                    print(f"Expected file: {crawl_file}")
                    return False
            else:
                self.print_error("Crawl failed")
                print("\n--- Error Output ---")
                if result.stderr:
                    print(result.stderr[-2000:])
                if result.stdout:
                    print("\n--- Standard Output ---")
                    print(result.stdout[-2000:])
                return False
        except Exception as e:
            self.print_error(f"Failed to run crawl: {e}")
            return False

    def generate_manual_tests(self, criteria: Dict[str, Any]) -> Optional[Path]:
        """Generate manual test cases"""
        self.print_header("Generating Manual Test Cases")

        if not self.agent:
            self.print_error("Agent not initialized")
            return None

        try:
            manual_path = self.agent.generate_manual_tests(
                page_name=criteria["page"],
                feature=criteria["feature"],
                criteria=criteria["acceptanceCriteria"],
            )
            self.print_success(f"Manual test cases generated: {manual_path}")
            return Path(manual_path)
        except Exception as e:
            self.print_error(f"Failed to generate manual tests: {e}")
            return None

    def review_manual_tests(self, manual_file: Path) -> bool:
        """Allow user to review and modify manual tests"""
        self.print_header("Review Manual Test Cases")

        if not manual_file.exists():
            self.print_error(f"Manual test file not found: {manual_file}")
            return False

        try:
            with open(manual_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            print(json.dumps(content, indent=2, ensure_ascii=False))
            
            print("\nOptions:")
            print("1. Accept and continue")
            print("2. Edit manually (file will be opened)")
            choice = input("Enter choice (1 or 2): ").strip()

            if choice == "2":
                self.print_info(f"Please edit the file: {manual_file}")
                input("Press Enter after editing...")
            
            return True
        except Exception as e:
            self.print_error(f"Failed to review manual tests: {e}")
            return False

    def generate_test_scripts(self, criteria: Dict[str, Any]) -> bool:
        """Generate POM and test scripts"""
        self.print_header("Generating Test Scripts (POM + Tests)")

        if not self.agent:
            self.print_error("Agent not initialized")
            return False

        try:
            # Generate POM
            self.print_info("Generating Page Object Model...")
            pom_path = self.agent.generate_pom(
                page_name=criteria["page"],
                criteria=criteria["acceptanceCriteria"],
            )
            self.print_success(f"POM generated: {pom_path}")

            # Generate test scripts
            self.print_info("Generating test scripts...")
            test_path = self.agent.generate_tests(
                page_name=criteria["page"],
                criteria=criteria["acceptanceCriteria"],
            )
            self.print_success(f"Test scripts generated: {test_path}")

            return True
        except Exception as e:
            self.print_error(f"Failed to generate test scripts: {e}")
            return False

    def review_test_scripts(self, page_name: str) -> bool:
        """Allow user to review generated test scripts"""
        self.print_header("Review Test Scripts")

        pom_file = MOBILE_TESTS_DIR / "src" / "pageobjects" / f"{page_name.capitalize()}Page.ts"
        test_file = MOBILE_TESTS_DIR / "src" / "tests" / f"{page_name.lower()}.e2e.ts"

        if pom_file.exists():
            print(f"\n--- Page Object Model: {pom_file.name} ---")
            print(pom_file.read_text(encoding='utf-8')[:1000] + "...\n")

        if test_file.exists():
            print(f"\n--- Test Script: {test_file.name} ---")
            print(test_file.read_text(encoding='utf-8')[:1000] + "...\n")

        print("Options:")
        print("1. Accept and continue to execution")
        print("2. Edit manually (files will be opened)")
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "2":
            self.print_info(f"Please edit the files:")
            print(f"  - {pom_file}")
            print(f"  - {test_file}")
            input("Press Enter after editing...")

        return True

    def execute_tests(self, page_name: Optional[str] = None) -> bool:
        """Execute test cases"""
        self.print_header("Executing Test Cases")

        if not self.current_device:
            self.print_error("No device selected")
            return False

        self.print_info("Starting test execution...")
        self.print_info("Please ensure Appium server is running (port 4723)")

        input("\nPress Enter to start execution...")

        # Check if Node.js is available
        node_available, node_info = self._check_node_available()
        if not node_available:
            self.print_error("Node.js is not installed or not in PATH")
            self.print_info("Please install Node.js from https://nodejs.org/")
            return False

        try:
            # Get the correct npx command
            npx_cmd = self._get_npx_cmd()
            
            # Run specific test file if page_name provided, otherwise run all
            if page_name:
                spec_file = f"./src/tests/{page_name.lower()}.e2e.ts"
                cmd = npx_cmd + ["wdio", "run", "wdio.conf.ts", "--spec", spec_file]
            else:
                cmd = npx_cmd + ["wdio", "run", "wdio.conf.ts"]

            result = subprocess.run(
                cmd,
                cwd=str(MOBILE_TESTS_DIR),
                capture_output=True,
                text=True,
                check=False,
                shell=IS_WINDOWS,
            )

            success = result.returncode == 0

            if success:
                self.print_success("Test execution completed successfully")
            else:
                self.print_error("Test execution completed with failures")
                print("\nLast 500 characters of output:")
                print(result.stdout[-500:])
                print(result.stderr[-500:])

            # Generate Allure report
            self.generate_allure_report()

            return success
        except Exception as e:
            self.print_error(f"Failed to execute tests: {e}")
            return False

    def generate_allure_report(self):
        """Generate Allure HTML report"""
        self.print_header("Generating Allure Report")

        # Check if Node.js is available
        node_available, node_info = self._check_node_available()
        if not node_available:
            self.print_error("Node.js is not installed or not in PATH")
            self.print_info("Cannot generate Allure report without Node.js")
            return False

        # Check if allure-results directory exists
        allure_results_dir = MOBILE_TESTS_DIR / "allure-results"
        if not allure_results_dir.exists():
            self.print_error("No test results found")
            self.print_info(f"Expected directory: {allure_results_dir}")
            self.print_info("Please run tests first (Option 8) to generate test results")
            return False

        # Check if Java is available (required by Allure)
        try:
            java_result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True,
                check=False,
                shell=IS_WINDOWS,
            )
            if java_result.returncode != 0:
                raise FileNotFoundError
        except (FileNotFoundError, Exception):
            self.print_error("Java is not installed or not in PATH")
            self.print_info("Allure requires Java to generate reports")
            self.print_info("Please install Java JDK 17+ and set JAVA_HOME environment variable")
            self.print_info("See: FIX_JAVA_ERROR.md for installation instructions")
            return False

        try:
            npx_cmd = self._get_npx_cmd()
            cmd = npx_cmd + ["allure", "generate", "./allure-results", "--clean", "-o", "./allure-report"]
            
            self.print_info("Generating Allure report...")
            result = subprocess.run(
                cmd,
                cwd=str(MOBILE_TESTS_DIR),
                capture_output=True,
                text=True,
                check=False,
                shell=IS_WINDOWS,
            )

            if result.returncode == 0:
                report_dir = MOBILE_TESTS_DIR / "allure-report"
                self.print_success(f"Allure report generated: {report_dir}")
                self.print_info(f"Open report: npx allure open ./allure-report")
                self.print_info(f"Or open: {report_dir / 'index.html'}")
                return True
            else:
                self.print_error("Failed to generate Allure report")
                if result.stderr:
                    print(result.stderr)
                if result.stdout:
                    print(result.stdout)
                return False
        except Exception as e:
            self.print_error(f"Error generating report: {e}")
            return False

    def configure_app(self) -> bool:
        """Configure native app for testing"""
        self.print_header("Configure Native App")

        print("Options:")
        print("1. Use native app (APK file)")
        print("2. Use WebdriverIO Demo App (Quick Setup)")
        print("3. Use browser (Chrome) - default")
        print("4. Clear app configuration")
        
        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            # Get app path
            app_path = input("\nEnter full path to APK file: ").strip()
            if not app_path:
                self.print_error("App path cannot be empty")
                return False

            app_path_obj = Path(app_path)
            if not app_path_obj.exists():
                self.print_error(f"APK file not found: {app_path}")
                return False

            if not app_path.endswith('.apk'):
                self.print_error("File must be an APK file (.apk extension)")
                return False

            # Get app package (optional, can extract from APK)
            app_package = input("Enter app package name (e.g., com.example.app) or press Enter to auto-detect: ").strip()
            
            # Get app activity (optional)
            app_activity = input("Enter main activity (e.g., .MainActivity) or press Enter to use default: ").strip()

            # Try to extract package name from APK if not provided
            if not app_package:
                self.print_info("Attempting to extract package name from APK...")
                try:
                    import subprocess
                    result = subprocess.run(
                        ["aapt", "dump", "badging", app_path],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if line.startswith('package: name='):
                                app_package = line.split("'")[1]
                                self.print_success(f"Detected package: {app_package}")
                                break
                except FileNotFoundError:
                    self.print_info("aapt not found. Please install Android SDK Build Tools or enter package manually.")
                    app_package = input("Enter app package name: ").strip()
                    if not app_package:
                        self.print_error("Package name is required")
                        return False

            if not app_activity:
                app_activity = ".MainActivity"

            # Save configuration
            self.app_path = app_path
            self.app_package = app_package
            self.app_activity = app_activity

            # Update wdio config
            if self.device_manager.update_app_config(app_path, app_package, app_activity):
                self.print_success("App configuration saved!")
                self.print_info(f"App Path: {app_path}")
                self.print_info(f"Package: {app_package}")
                self.print_info(f"Activity: {app_activity}")
                return True
            else:
                self.print_error("Failed to update configuration")
                return False

        elif choice == "2":
            # WebdriverIO Demo App Quick Setup
            self.print_header("WebdriverIO Demo App Quick Setup")
            
            # Try to find the app in common locations
            possible_paths = [
                MOBILE_TESTS_DIR / "app" / "Android-NativeDemoApp-0.4.0.apk",
                ROOT_DIR / "app" / "android.wdio.native.app.v1.0.8.apk",
                ROOT_DIR / "app" / "wdio-demo-app.apk",
                ROOT_DIR / "app" / "Android-NativeDemoApp-0.4.0.apk",
                MOBILE_TESTS_DIR / "app" / "android.wdio.native.app.v1.0.8.apk",
            ]
            
            found_path = None
            for path in possible_paths:
                if path.exists():
                    found_path = str(path)
                    break
            
            if found_path:
                self.print_success(f"Found WebdriverIO demo app: {found_path}")
                use_found = input("Use this app? (y/n): ").strip().lower()
                if use_found != 'y':
                    found_path = None
            
            if not found_path:
                app_path = input("Enter path to WebdriverIO demo app APK: ").strip()
                if not app_path or not Path(app_path).exists():
                    self.print_error("APK file not found")
                    return False
                found_path = app_path
            
            # WebdriverIO demo app details
            # Try to detect package name from APK, fallback to common packages
            app_package = None
            app_activity = ".MainActivity"
            
            # Try to extract package name
            try:
                import subprocess
                result = subprocess.run(
                    ["aapt", "dump", "badging", found_path],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.startswith('package: name='):
                            app_package = line.split("'")[1]
                            self.print_success(f"Detected package: {app_package}")
                            break
            except FileNotFoundError:
                pass
            
            # Fallback to common package names
            if not app_package:
                # Check which package is installed
                try:
                    result = subprocess.run(
                        ["adb", "shell", "pm", "list", "packages"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if "io.cloudgrey.the_app" in result.stdout:
                        app_package = "io.cloudgrey.the_app"
                    elif "com.wdiodemoapp" in result.stdout:
                        app_package = "com.wdiodemoapp"
                    else:
                        app_package = "io.cloudgrey.the_app"  # Default for Android-NativeDemoApp
                except:
                    app_package = "io.cloudgrey.the_app"  # Default
            
            self.app_path = found_path
            self.app_package = app_package
            self.app_activity = app_activity
            
            if self.device_manager.update_app_config(found_path, app_package, app_activity):
                self.print_success("WebdriverIO Demo App configured!")
                self.print_info(f"App Path: {found_path}")
                self.print_info(f"Package: {app_package}")
                self.print_info(f"Activity: {app_activity}")
                self.print_info("\nYou can now test common screens:")
                self.print_info("  - login (Login screen)")
                self.print_info("  - forms (Forms screen)")
                self.print_info("  - swipe (Swipe screen)")
                return True
            else:
                self.print_error("Failed to update configuration")
                return False

        elif choice == "3":
            # Clear app config to use browser
            if self.device_manager.update_app_config("", "", ""):
                self.app_path = None
                self.app_package = None
                self.app_activity = None
                self.print_success("Switched to browser mode (Chrome)")
                return True
            return False

        elif choice == "4":
            # Clear configuration
            if self.device_manager.update_app_config("", "", ""):
                self.app_path = None
                self.app_package = None
                self.app_activity = None
                self.print_success("App configuration cleared")
                return True
            return False

        else:
            self.print_error("Invalid choice")
            return False

    def auto_heal(self, page_name: str) -> bool:
        """Auto-heal failed tests"""
        self.print_header("Auto-Healing Failed Tests")

        if not self.agent:
            self.print_error("Agent not initialized")
            return False

        # Read allure results to find failures
        allure_results_dir = MOBILE_TESTS_DIR / "allure-results"
        if not allure_results_dir.exists():
            self.print_error("No test results found for auto-healing")
            return False

        self.print_info("Analyzing test failures...")
        
        # Re-crawl the page to get fresh elements
        if not self.crawl_page(page_name):
            self.print_error("Failed to crawl page for auto-healing")
            return False

        # Regenerate POM with fresh crawl data
        try:
            # Load existing acceptance criteria
            criteria_file = ACCEPTANCE_CRITERIA_DIR / f"{page_name}.json"
            if criteria_file.exists():
                with open(criteria_file, 'r', encoding='utf-8') as f:
                    criteria = json.load(f)
                
                self.print_info("Regenerating POM with updated selectors...")
                pom_path = self.agent.generate_pom(
                    page_name=page_name,
                    criteria=criteria["acceptanceCriteria"],
                )
                self.print_success(f"POM regenerated: {pom_path}")
                
                # Re-run tests
                self.print_info("Re-running tests after auto-healing...")
                return self.execute_tests(page_name)
            else:
                self.print_error(f"Acceptance criteria file not found: {criteria_file}")
                return False
        except Exception as e:
            self.print_error(f"Auto-healing failed: {e}")
            return False

    def run_full_workflow(self):
        """Run the complete workflow"""
        self.print_header("AI Agent for Mobile Webdriver - CLI")

        # Initialize agent
        if not self.initialize_agent():
            return

        while True:
            print("\n" + "=" * 60)
            print("Main Menu")
            print("=" * 60)
            print("1. Add Acceptance Criteria")
            print("2. Select Platform and Device")
            print("3. Crawl Page Elements")
            print("4. Generate Manual Test Cases")
            print("5. Review Manual Test Cases")
            print("6. Generate Test Scripts (POM + Tests)")
            print("7. Review Test Scripts")
            print("8. Execute Tests")
            print("9. Generate Allure Report")
            print("10. Auto-Heal Failed Tests")
            print("11. Configure App (Native App Path)")
            print("12. Run Complete Workflow (All Steps)")
            print("13. Exit")
            print("=" * 60)

            choice = input("\nEnter your choice (1-13): ").strip()

            if choice == "1":
                criteria = self.get_acceptance_criteria()
                if criteria:
                    self.save_acceptance_criteria(criteria)
                    self.current_page = criteria["page"]

            elif choice == "2":
                self.select_platform_and_device()

            elif choice == "3":
                if not self.current_page:
                    self.current_page = input("Enter page name to crawl: ").strip().lower()
                if self.current_page:
                    self.crawl_page(self.current_page)

            elif choice == "4":
                if not self.current_page:
                    criteria_file = input("Enter acceptance criteria file name (without .json): ").strip()
                    criteria_path = ACCEPTANCE_CRITERIA_DIR / f"{criteria_file}.json"
                else:
                    criteria_path = ACCEPTANCE_CRITERIA_DIR / f"{self.current_page}.json"

                if criteria_path.exists():
                    with open(criteria_path, 'r', encoding='utf-8') as f:
                        criteria = json.load(f)
                    self.generate_manual_tests(criteria)
                else:
                    self.print_error(f"Acceptance criteria file not found: {criteria_path}")

            elif choice == "5":
                if not self.current_page:
                    page = input("Enter page name: ").strip().lower()
                else:
                    page = self.current_page
                manual_file = MOBILE_TESTS_DIR / "manual-tests" / f"{page}_manual.json"
                self.review_manual_tests(manual_file)

            elif choice == "6":
                if not self.current_page:
                    criteria_file = input("Enter acceptance criteria file name (without .json): ").strip()
                    criteria_path = ACCEPTANCE_CRITERIA_DIR / f"{criteria_file}.json"
                else:
                    criteria_path = ACCEPTANCE_CRITERIA_DIR / f"{self.current_page}.json"

                if criteria_path.exists():
                    with open(criteria_path, 'r', encoding='utf-8') as f:
                        criteria = json.load(f)
                    self.generate_test_scripts(criteria)
                else:
                    self.print_error(f"Acceptance criteria file not found: {criteria_path}")

            elif choice == "7":
                if not self.current_page:
                    page = input("Enter page name: ").strip().lower()
                else:
                    page = self.current_page
                self.review_test_scripts(page)

            elif choice == "8":
                page = input("Enter page name to test (or press Enter for all tests): ").strip().lower() or None
                self.execute_tests(page)

            elif choice == "9":
                self.generate_allure_report()

            elif choice == "10":
                if not self.current_page:
                    page = input("Enter page name: ").strip().lower()
                else:
                    page = self.current_page
                self.auto_heal(page)

            elif choice == "11":
                self.configure_app()

            elif choice == "12":
                # Run complete workflow
                criteria = self.get_acceptance_criteria()
                if not criteria:
                    continue
                
                self.current_page = criteria["page"]
                self.save_acceptance_criteria(criteria)

                if not self.select_platform_and_device():
                    continue

                if not self.crawl_page(self.current_page):
                    continue

                manual_file = self.generate_manual_tests(criteria)
                if manual_file:
                    if not self.review_manual_tests(manual_file):
                        continue

                if not self.generate_test_scripts(criteria):
                    continue

                if not self.review_test_scripts(self.current_page):
                    continue

                if not self.execute_tests(self.current_page):
                    # If tests failed, offer auto-healing
                    heal = input("\nTests failed. Attempt auto-healing? (y/n): ").strip().lower()
                    if heal == 'y':
                        self.auto_heal(self.current_page)

                self.generate_allure_report()

            elif choice == "13":
                self.print_info("Exiting...")
                break

            else:
                self.print_error("Invalid choice")


def main():
    cli = CLI()
    cli.run_full_workflow()


if __name__ == "__main__":
    main()

