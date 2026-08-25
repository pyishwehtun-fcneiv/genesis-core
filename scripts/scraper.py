"""
GENESIS Scraper Module — runs natively inside GitHub Actions runner.
No external server dependency (replaces HF Space Gradio approach).
"""
import sys
import json
from playwright.sync_api import sync_playwright


def stealth_scrape(url: str) -> dict:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page = context.new_page()
            page.goto(url, timeout=30000, wait_until="networkidle")
            content = page.content()
            title = page.title()
            browser.close()
            return {"title": title, "html": content[:50000], "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}


if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    result = stealth_scrape(target_url)
    print(json.dumps(result, indent=2))
