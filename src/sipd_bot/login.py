"""
This module provides the LoginMixin class for the SIPDBot automation framework.

The LoginMixin encapsulates all functionality related to logging in to the
SIPD-RI web application. It supports two login mechanisms:
    1. Manual login through browser interaction.
    2. Session restoration via saved cookies.

Features:
- Automatically determines whether to log in manually or restore from session cookies.
- Saves session cookies to `cookies.json` after manual login.
- Loads cookies from file and injects them into the browser context.
- Handles invalid or expired cookies gracefully by falling back to manual login.

Intended to be used as a mixin alongside SIPDBotBase for browser and page access.
"""

import os
import json
import logging


logger = logging.getLogger(__name__)


class LoginMixin:
    """
    Provides login functionality for SIPDBot.

    This mixin handles login logic using session cookies if available,
    or performs manual login and saves cookies for future use.
    """

    URL_LOGIN = "https://sipd.kemendagri.go.id/penatausahaan/login"

    def login(self):
        """
        Log in to SIPD-RI. Log in method is picked based on the existence of session cookie file.
        """
        if self.is_cookies_exist():
            logger.info("Cookie file found, logging in with cookies")
            self.login_with_cookies()
        else:
            logger.info("Cookie file not found, performing manual login")
            self.login_manual()
            self.save_cookies()

    @staticmethod
    def is_cookies_exist(cookie_file="cookies.json") -> bool:
        """
        Checks if the specified cookie file exists.

        Args:
            cookie_file (str, optional): The name of the cookie file to check.
            Defaults to "cookies.json".

        Returns:
            bool: True if the cookie file exists, False otherwise.
        """
        exists = os.path.exists(cookie_file)
        logger.debug("Checking for cookie file: %s -> %s", cookie_file, exists)
        return exists

    def save_cookies(self):
        """
        Saves the current session cookies to a JSON file.

        Output:
            cookies.json (file): A JSON file containing the session cookies.
        """
        cookies = self.context.cookies()
        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f)
        logger.info("Cookies saved to cookies.json")

    def login_manual(self):
        """
        Perform a manual login to SIPD-RI.

        This method navigates to the login page and allows the user to input
        credentials manually.
        """
        logger.info("Navigating to login page manually: %s", self.URL_LOGIN)
        self.page.goto(self.URL_LOGIN, timeout=120_000)
        self.page.bring_to_front()
        logger.debug("Waiting for dashboard URL after manual login...")
        self.page.wait_for_url("**/dashboard", timeout=300_000)

        menu_link = self.page.locator('a:has-text("Akuntansi")').first
        menu_link.wait_for(timeout=120_000)
        logger.info("Manual login successful")

    def login_with_cookies(self):
        """
        Attempt to log in to SIPD-RI using saved session cookies.

        This method loads cookies from `cookies.json` and tries to authenticate the
        session without manual input.

        Raises:
            FileNotFoundError: If the cookie file does not exist.
            json.JSONDecodeError: If the cookie file is not valid JSON.

        Notes:
            - If cookies are expired or invalid, the method will fall back to manual login.
        """
        try:
            logger.debug("Loading cookies from cookies.json...")
            with open("cookies.json", "r", encoding="utf-8") as f:
                cookies = json.load(f)
                self.context.add_cookies(cookies)

            logger.info("Cookies loaded successfully. Attempting to login...")
            self.page.goto(self.URL_LOGIN, timeout=120_000)
            self.page.bring_to_front()
            self.page.wait_for_url("**/dashboard", timeout=300_000)

            logger.info("Logged in using cookies")

        except json.JSONDecodeError:
            logger.warning(
                "Invalid or expired cookies. Deleting cookies.json and retrying manual login"
            )
            os.remove("cookies.json")
            self.login()

        except FileNotFoundError:
            logger.error("Cookie file not found. Falling back to manual login")
            self.login()
