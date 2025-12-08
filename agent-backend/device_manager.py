"""
Device Manager for detecting and managing Android and iOS devices/emulators
"""

import json
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Optional

ROOT_DIR = Path(__file__).resolve().parents[1]
MOBILE_TESTS_DIR = ROOT_DIR / "mobile-tests"
WDIO_CONFIG_FILE = MOBILE_TESTS_DIR / "wdio.conf.ts"


class DeviceManager:
    """Manages device detection and WebdriverIO configuration"""

    def __init__(self):
        self.system = platform.system()

    def detect_android_devices(self) -> List[Dict[str, str]]:
        """Detect Android devices and emulators using adb"""
        devices = []

        try:
            # Check if adb is available
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                return devices

            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if not line.strip() or 'offline' in line:
                    continue

                parts = line.split('\t')
                if len(parts) >= 2:
                    device_id = parts[0]
                    status = parts[1]

                    if status == 'device':
                        # Get device properties
                        device_info = self._get_android_device_info(device_id)
                        if device_info:
                            devices.append(device_info)

        except FileNotFoundError:
            # adb not found
            pass
        except Exception as e:
            print(f"Error detecting Android devices: {e}")

        return devices

    def _get_android_device_info(self, device_id: str) -> Optional[Dict[str, str]]:
        """Get detailed information about an Android device"""
        try:
            # Get device model
            model_result = subprocess.run(
                ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
                capture_output=True,
                text=True,
                check=False,
            )
            model = model_result.stdout.strip() if model_result.returncode == 0 else "Unknown"

            # Get Android version
            version_result = subprocess.run(
                ["adb", "-s", device_id, "shell", "getprop", "ro.build.version.release"],
                capture_output=True,
                text=True,
                check=False,
            )
            version = version_result.stdout.strip() if version_result.returncode == 0 else "Unknown"

            # Check if it's an emulator
            is_emulator = device_id.startswith("emulator-") or "emulator" in model.lower()

            return {
                "id": device_id,
                "name": model or device_id,
                "version": f"Android {version}",
                "platform": "Android",
                "is_emulator": is_emulator,
            }
        except Exception:
            return None

    def detect_ios_devices(self) -> List[Dict[str, str]]:
        """Detect iOS devices and simulators"""
        devices = []

        if self.system != "Darwin":  # macOS only
            return devices

        try:
            # List iOS simulators
            result = subprocess.run(
                ["xcrun", "simctl", "list", "devices", "available", "--json"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                for runtime, simulators in data.get("devices", {}).items():
                    for sim in simulators:
                        if sim.get("isAvailable", False):
                            devices.append({
                                "id": sim["udid"],
                                "name": sim["name"],
                                "version": runtime.replace("com.apple.CoreSimulator.SimRuntime.", "").replace("-", " "),
                                "platform": "iOS",
                                "is_emulator": True,
                                "state": sim.get("state", "unknown"),
                            })

            # List physical iOS devices (requires Xcode)
            try:
                devices_result = subprocess.run(
                    ["xcrun", "xctrace", "list", "devices"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                # Parse physical devices if needed
            except Exception:
                pass

        except FileNotFoundError:
            # xcrun not found (not on macOS or Xcode not installed)
            pass
        except Exception as e:
            print(f"Error detecting iOS devices: {e}")

        return devices

    def detect_devices(self, platform_name: str) -> List[Dict[str, str]]:
        """Detect devices for the specified platform"""
        if platform_name.lower() == "android":
            return self.detect_android_devices()
        elif platform_name.lower() == "ios":
            return self.detect_ios_devices()
        else:
            return []

    def update_wdio_config(self, device: Dict[str, str], platform_name: str) -> bool:
        """Update WebdriverIO configuration with selected device"""
        if not WDIO_CONFIG_FILE.exists():
            return False

        try:
            config_content = WDIO_CONFIG_FILE.read_text(encoding='utf-8')

            # Update platform name
            if 'platformName:' in config_content:
                config_content = self._replace_config_value(
                    config_content, 'platformName', f"'{platform_name}'"
                )

            # Update device name
            if 'appium:deviceName' in config_content:
                device_name = device.get('name', device.get('id', 'Unknown'))
                config_content = self._replace_config_value(
                    config_content, 'appium:deviceName', f"'{device_name}'"
                )

            # Update platform version
            if 'appium:platformVersion' in config_content:
                version = device.get('version', '').replace('Android ', '').replace('iOS ', '').split('.')[0]
                if version:
                    config_content = self._replace_config_value(
                        config_content, 'appium:platformVersion', f"'{version}.0'"
                    )

            # Update UDID for iOS or device ID for Android
            if platform_name == "iOS":
                if 'appium:udid' in config_content:
                    config_content = self._replace_config_value(
                        config_content, 'appium:udid', f"'{device.get('id', '')}'"
                    )
                else:
                    # Add UDID if not present
                    config_content = self._add_config_property(
                        config_content, 'appium:udid', f"'{device.get('id', '')}'"
                    )
            else:  # Android
                if 'appium:udid' in config_content:
                    config_content = self._replace_config_value(
                        config_content, 'appium:udid', f"'{device.get('id', '')}'"
                    )

            # Update automation name
            if platform_name == "Android":
                if 'appium:automationName' in config_content:
                    config_content = self._replace_config_value(
                        config_content, 'appium:automationName', "'UiAutomator2'"
                    )
            elif platform_name == "iOS":
                if 'appium:automationName' in config_content:
                    config_content = self._replace_config_value(
                        config_content, 'appium:automationName', "'XCUITest'"
                    )

            WDIO_CONFIG_FILE.write_text(config_content, encoding='utf-8')
            return True

        except Exception as e:
            print(f"Error updating WebdriverIO config: {e}")
            return False

    def _replace_config_value(self, content: str, key: str, value: str) -> str:
        """Replace a configuration value in TypeScript config"""
        import re
        # Match key with optional quotes, colon, and value (handles both single and double quotes)
        pattern = rf"(['\"]?{re.escape(key)}['\"]?\s*:\s*)([^,\n}}]+)"
        replacement = rf"\1{value}"
        result = re.sub(pattern, replacement, content)
        return result

    def _add_config_property(self, content: str, key: str, value: str) -> str:
        """Add a configuration property to capabilities"""
        # Find the capabilities object and add the property
        import re
        # Look for the closing brace of capabilities object (not array)
        # Capabilities is an array with one object: [{...}]
        pattern = r"(capabilities:\s*\[\s*{)([^}]+)(}\s*\])"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            before = match.group(1) + match.group(2)
            after = match.group(3)
            # Add new property before the closing brace
            new_prop = f"        '{key}': {value},\n"
            return content.replace(match.group(0), before + new_prop + "    " + after)
        return content

    def update_app_config(self, app_path: str, app_package: str, app_activity: str) -> bool:
        """Update WebdriverIO configuration with app settings"""
        if not WDIO_CONFIG_FILE.exists():
            return False

        try:
            config_content = WDIO_CONFIG_FILE.read_text(encoding='utf-8')

            # Convert Windows path to forward slashes for consistency
            if app_path:
                app_path = app_path.replace('\\', '/')

            # Update APP_PATH, APP_PACKAGE, APP_ACTIVITY constants
            import re
            
            # Update or add APP_PATH
            if re.search(r'const APP_PATH', config_content):
                config_content = re.sub(
                    r"const APP_PATH = process\.env\.APP_PATH \|\| '[^']*'",
                    f"const APP_PATH = process.env.APP_PATH || '{app_path}'",
                    config_content
                )
            else:
                # Add after imports if not found
                config_content = config_content.replace(
                    "import type { Options } from '@wdio/types';",
                    f"import type {{ Options }} from '@wdio/types';\n\n// App configuration\nconst APP_PATH = process.env.APP_PATH || '{app_path}';"
                )

            # Update APP_PACKAGE
            if re.search(r'const APP_PACKAGE', config_content):
                config_content = re.sub(
                    r"const APP_PACKAGE = process\.env\.APP_PACKAGE \|\| '[^']*'",
                    f"const APP_PACKAGE = process.env.APP_PACKAGE || '{app_package}'",
                    config_content
                )
            else:
                config_content = config_content.replace(
                    "const APP_PATH = process.env.APP_PATH || '';",
                    f"const APP_PATH = process.env.APP_PATH || '{app_path}';\nconst APP_PACKAGE = process.env.APP_PACKAGE || '{app_package}';"
                )

            # Update APP_ACTIVITY
            if re.search(r'const APP_ACTIVITY', config_content):
                config_content = re.sub(
                    r"const APP_ACTIVITY = process\.env\.APP_ACTIVITY \|\| '[^']*'",
                    f"const APP_ACTIVITY = process.env.APP_ACTIVITY || '{app_activity}'",
                    config_content
                )
            else:
                config_content = config_content.replace(
                    f"const APP_PACKAGE = process.env.APP_PACKAGE || '{app_package}';",
                    f"const APP_PACKAGE = process.env.APP_PACKAGE || '{app_package}';\nconst APP_ACTIVITY = process.env.APP_ACTIVITY || '{app_activity}';"
                )

            WDIO_CONFIG_FILE.write_text(config_content, encoding='utf-8')
            return True

        except Exception as e:
            print(f"Error updating app config: {e}")
            return False

