"""
A helper module for managing cookies used in SIPDBot class.
"""

import os
import json
from playwright.sync_api import sync_playwright


class CookieHelper:
    """
    A helper class that provides a methods to check for the existance of a cookie file
    and to save cookie after a successful login session. Cookies are stored in a JSON
    file for use in subsequent sessions.
    """

    @staticmethod
    def is_cookies_exist(cookie_file="cookies.json") -> bool:
        """
        Checks if the specified cookie file exists.

        Args:
            cookie_file (str, optional): The name of the cookie file to check. Defaults to "cookies.json".

        Returns:
            bool: True if the cookie file exists, False otherwise.
        """
        return os.path.exists(cookie_file)

    @staticmethod
    def save_cookies():
        """
        Save current session cookies after a successful login attempt.

        User need to manually fill the login and CAPTCHA form. After a successful login,
        press Enter to continue and save the cookies.

        Output:
            cookies.json (file): A JSON file containing the session cookies.
        """
        url_login = "https://sipd.kemendagri.go.id/penatausahaan/login"

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=False, args=["--start-maximized"]
            )
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
            input("\nPress Enter to continue...")
