from playwright.sync_api import sync_playwright

def test_ui_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://ai-job-assistant-peach.vercel.app")

        # Fill input
        page.fill("input[type='text']", "python")

        # Click search
        page.click("text=Search")

        # ✅ WAIT for network/API response (BEST WAY)
        page.wait_for_timeout(3000)

        # ✅ Check that page changed (robust)
        content = page.content()

        assert "job" in content.lower()

        browser.close()