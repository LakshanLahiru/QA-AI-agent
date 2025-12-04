import json
import os
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ROOT_DIR = Path(__file__).resolve().parents[1]  # .../mobile-ai-agent
MOBILE_TESTS_DIR = ROOT_DIR / "mobile-tests"
PAGEOBJECTS_DIR = MOBILE_TESTS_DIR / "src" / "pageobjects"
TESTS_DIR = MOBILE_TESTS_DIR / "src" / "tests"
MANUAL_TESTS_DIR = MOBILE_TESTS_DIR / "manual-tests"


class TestGenerationAgent:
    """
    Simple OpenAI-based agent (no LangChain) that:
    - Takes acceptance criteria
    - Generates POM TypeScript classes
    - Generates/extends WebdriverIO TypeScript tests
    - Generates manual test cases JSON
    """

    def __init__(self, openai_api_key: str | None = None):
        api_key = openai_api_key or OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        # instantiate OpenAI client (v1.x SDK)
        self.client = OpenAI(api_key=api_key)
        # model choice (use your available model)
        self.model = "gpt-4.1-mini"

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Calls the new OpenAI Python SDK chat completions endpoint.
        Returns the assistant content string.
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=1600,
        )
        # defensive access
        try:
            return resp.choices[0].message.content or ""
        except Exception:
            return ""

    def _read_existing_summary(self, path: Path) -> str:
        if not path.exists():
            return "No existing file."
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return "Existing file not readable."
        return content[:2000]

    def generate_pom(self, page_name: str, criteria: List[Dict[str, Any]]) -> str:
        criteria_json = json.dumps(criteria, indent=2, ensure_ascii=False)
        pom_file = PAGEOBJECTS_DIR / f"{page_name.capitalize()}Page.ts"
        existing_summary = self._read_existing_summary(pom_file)

        system_prompt = (
            "You are an expert mobile QA automation engineer. "
            "Generate a TypeScript Page Object class for WebdriverIO + Appium. "
            "Use async/await and export a default class PLUS a named instance if helpful. "
            "Do NOT include any explanations, only valid TypeScript code."
        )
        user_prompt = (
            f"Page name: {page_name}\n"
            f"Platform(s): Android/iOS\n"
            f"Acceptance criteria (JSON):\n{criteria_json}\n\n"
            f"Existing selectors summary (if any):\n{existing_summary}\n"
            "Remember: this must fit into the POM structure under src/pageobjects."
        )

        ts_code = self._chat(system_prompt, user_prompt)

        PAGEOBJECTS_DIR.mkdir(parents=True, exist_ok=True)
        pom_file.write_text(ts_code, encoding="utf-8")
        return str(pom_file)

    def generate_tests(self, page_name: str, criteria: List[Dict[str, Any]]) -> str:
        criteria_json = json.dumps(criteria, indent=2, ensure_ascii=False)
        test_file = TESTS_DIR / f"{page_name.lower()}.e2e.ts"
        existing_summary = self._read_existing_summary(test_file)

        system_prompt = (
            "You are an expert in WebdriverIO with TypeScript and Mocha. "
            "Generate ONE OR MORE 'describe' blocks with 'it' tests that use Page Object classes. "
            "Follow Page Object Model strictly. "
            "Use async/await style. "
            "Do NOT overwrite older tests; new tests should be appended safely. "
            "Do NOT include explanations, only valid TypeScript code."
        )
        user_prompt = (
            f"Page name: {page_name}\n"
            f"POM class file name: {page_name.capitalize()}Page.ts\n"
            f"Acceptance criteria (JSON):\n{criteria_json}\n"
            f"Existing tests summary (if any):\n{existing_summary}\n"
            "Your output will be appended to or placed in a .ts test file under src/tests.\n"
        )

        ts_code = self._chat(system_prompt, user_prompt)

        TESTS_DIR.mkdir(parents=True, exist_ok=True)
        mode = "a" if test_file.exists() else "w"
        with test_file.open(mode, encoding="utf-8") as f:
            if mode == "a":
                f.write("\n\n")
            f.write(ts_code)
        return str(test_file)

    def generate_manual_tests(self, page_name: str, feature: str, criteria: List[Dict[str, Any]]) -> str:
        """
        Generate structured manual test cases and store as JSON.
        """
        criteria_json = json.dumps(criteria, indent=2, ensure_ascii=False)
        system_prompt = (
            "You are a senior QA test analyst. "
            "From acceptance criteria, create detailed MANUAL test cases in JSON array form. "
            "Each test case must have: id, title, preconditions, steps (array), expectedResults (array). "
            "Only output valid JSON, no comments or explanations."
        )
        user_prompt = (
            f"Feature: {feature}\n"
            f"Page: {page_name}\n"
            f"Acceptance criteria (JSON):\n{criteria_json}\n"
        )

        manual_json = self._chat(system_prompt, user_prompt)

        MANUAL_TESTS_DIR.mkdir(parents=True, exist_ok=True)
        out_file = MANUAL_TESTS_DIR / f"{page_name.lower()}_manual.json"
        out_file.write_text(manual_json, encoding="utf-8")
        return str(out_file)
