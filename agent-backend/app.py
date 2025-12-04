import os
import subprocess
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import TestGenerationAgent
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AI Agent for Mobile Webdriver")

ROOT_DIR = Path(__file__).resolve().parents[1]
MOBILE_TESTS_DIR = ROOT_DIR / "mobile-tests"


class AcceptanceCriterion(BaseModel):
    id: str
    description: str
    preconditions: Optional[List[str]] = None
    steps: Optional[List[str]] = None
    expectedResult: Optional[str] = None


class AcceptanceCriteriaPayload(BaseModel):
    page: str
    feature: str
    acceptanceCriteria: List[AcceptanceCriterion]


class GenerateResponse(BaseModel):
    page: str
    feature: str
    pom_file: str
    test_file: str
    manual_tests_file: str


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/acceptance-criteria", response_model=GenerateResponse)
async def add_acceptance_criteria(payload: AcceptanceCriteriaPayload) -> GenerateResponse:
    """
    Generate POM, tests, and manual tests using OpenAI.
    """
    api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is not set.")

    # instantiate agent
    agent = TestGenerationAgent(openai_api_key=api_key)

    # convert pydantic models to plain dicts for LLM input
    criteria_list = [c.model_dump() for c in payload.acceptanceCriteria]

    # generate files
    pom_path = agent.generate_pom(page_name=payload.page, criteria=criteria_list)
    test_path = agent.generate_tests(page_name=payload.page, criteria=criteria_list)
    manual_path = agent.generate_manual_tests(page_name=payload.page, feature=payload.feature, criteria=criteria_list)

    return GenerateResponse(
        page=payload.page,
        feature=payload.feature,
        pom_file=pom_path,
        test_file=test_path,
        manual_tests_file=manual_path,
    )


@app.get("/manual-tests")
async def list_manual_tests() -> List[str]:
    manual_dir = MOBILE_TESTS_DIR / "manual-tests"
    if not manual_dir.exists():
        return []
    return [str(p) for p in manual_dir.glob("*.json")]


@app.get("/manual-tests/{page_name}")
async def get_manual_tests(page_name: str) -> dict:
    manual_dir = MOBILE_TESTS_DIR / "manual-tests"
    file_path = manual_dir / f"{page_name.lower()}_manual.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Manual tests not found for this page.")
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=500, detail="Could not read manual tests file.")
    return {"page": page_name, "file": str(file_path), "content": content}


@app.post("/run-tests")
async def run_tests() -> dict:
    """
    Run WebdriverIO from the mobile-tests folder and collect outputs.
    """
    if not MOBILE_TESTS_DIR.exists():
        raise HTTPException(status_code=500, detail=f"mobile-tests directory not found at {MOBILE_TESTS_DIR}")

    try:
        result = subprocess.run(
            ["npx", "wdio", "run", "wdio.conf.ts"],
            cwd=str(MOBILE_TESTS_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to start test run: {exc}")

    success = result.returncode == 0

    # Optionally generate allure HTML report (if allure installed)
    try:
        subprocess.run(
            ["npx", "allure", "generate", "./allure-results", "--clean", "-o", "./allure-report"],
            cwd=str(MOBILE_TESTS_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        # ignore report generation failures for now
        pass

    return {
        "success": success,
        "returncode": result.returncode,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-2000:],
        "allure_report_dir": str(MOBILE_TESTS_DIR / "allure-report"),
    }


@app.post("/crawl-page")
async def crawl_page(page: str) -> dict:
    """
    Run the crawler spec (driver.getPageSource()) to capture page XML.
    """
    if not MOBILE_TESTS_DIR.exists():
        raise HTTPException(status_code=500, detail=f"mobile-tests directory not found at {MOBILE_TESTS_DIR}")

    env = os.environ.copy()
    env["CRAWL_PAGE_NAME"] = page

    try:
        result = subprocess.run(
            ["npx", "wdio", "run", "wdio.conf.ts", "--spec", "./src/tests/crawl-page.e2e.ts"],
            cwd=str(MOBILE_TESTS_DIR),
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to start crawl: {exc}")

    success = result.returncode == 0
    crawl_file = MOBILE_TESTS_DIR / "crawls" / f"{page}.xml"

    return {
        "success": success,
        "returncode": result.returncode,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-2000:],
        "crawl_file": str(crawl_file),
    }


@app.post("/auto-heal")
async def auto_heal() -> dict:
    """
    Minimal auto-healing: regenerate POM for a sample page (login).
    Extend to parse allure-results and map failing tests to pages.
    """
    api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is not set.")

    agent = TestGenerationAgent(openai_api_key=api_key)

    dummy_criteria = [
        {
            "id": "AUTOHEAL_SAMPLE",
            "description": "Regenerate POM to attempt auto-healing of failing selectors.",
        }
    ]
    pom_path = agent.generate_pom(page_name="login", criteria=dummy_criteria)

    return {
        "message": "Auto-heal executed in minimal mode. Extend this to use real failure data.",
        "regenerated_pom": pom_path,
    }
