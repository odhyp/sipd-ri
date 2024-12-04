import json
from playwright.sync_api import sync_playwright


def save_cookies():
    url_login = "https://sipd.kemendagri.go.id/penatausahaan/login"

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto(url_login, timeout=120_000)
    page.bring_to_front()

    print("Please fill the login and CAPTCHA form")
    print("Only continue after successfully logged in!")
    input("\nPress Enter to continue...")

    cookies = context.cookies()
    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f)

    print("Cookies saved successfully")
