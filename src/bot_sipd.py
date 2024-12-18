"""
A module for automating interactions with SIPD-RI Kemendagri Website.
"""

import os
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.utils import get_month_name


class SIPDBot:
    """
    A bot for automating interactions with the SIPD-RI

    To-do List:
    # TODO: add refresh page method, using locator for reusability
    # TODO: add reload page method, using locator for reusability
    """

    URL_LOGIN = "https://sipd.kemendagri.go.id/penatausahaan/login"
    URL_PENATAUSAHAAN = "https://sipd.kemendagri.go.id/penatausahaan"
    URL_AKLAP = "https://sipd.kemendagri.go.id/penatausahaan/aklap"
    URL_AKLAPV2 = "https://peta.sipd.kemendagri.go.id/aklapv2"

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    def __enter__(self):
        """
        Initializes the browser and page when entering the context.

        Attributes:
            self.browser (Browser): The Playwright browser instance.
            self.context (BrowserContext): The context for managing browser settings and cookies.
            self.page (Page): The active page within the browser context for navigation and
                              interaction.

        Notes:
            - The browser is launched in non-headless mode (`headless=False`) to allow visual
              debugging.
            - The `--start-maximized` argument ensures the browser opens in maximized mode.
            - A universal viewport is disabled using `no_viewport=True`.
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False, args=["--start-maximized"]
        )
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the browser and cleans up resources when exiting the context.
        """
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def reload_page(self):
        """
        Reloads the current page from the server.
        """
        current_url = self.page.url
        self.page.goto(current_url)

    def is_404(self) -> bool:
        """
        Check if the current page is "404 - Page not found" page.

        Returns:
            bool: True if it's 404 page, False otherwise.
        """
        try:
            page_404 = self.page.locator('h1:has-text("404")')
            page_404.wait_for(timeout=5_000)
            return True
        except Exception:
            return False

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
        return os.path.exists(cookie_file)

    def save_cookies(self):
        """
        Save current session cookies after a successful login attempt.

        User need to manually fill the login and CAPTCHA form. After a successful login,
        press Enter to continue and save the cookies.

        Output:
            cookies.json (file): A JSON file containing the session cookies.
        """
        cookies = self.context.cookies()
        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f)

    def login(self):
        """
        Log in to SIPD-RI. Log in method is picked based on the existence of session cookie file.
        """
        if self.is_cookies_exist():
            self.login_with_cookies()
        else:
            self.login_manual()
            self.save_cookies()

    def login_manual(self):
        """
        Log in to SIPD-RI manually.

        This method navigates to the login page and the user fill the login
        credentials manually.
        """
        self.page.goto(self.URL_LOGIN, timeout=120_000)
        self.page.bring_to_front()
        self.page.wait_for_url("**/dashboard", timeout=300_000)

        menu_link = self.page.locator('a:has-text("Akuntansi")').first
        menu_link.wait_for(timeout=120_000)

    def login_with_env(self, username, password):
        """
        Log in to SIPD-RI using the provided credentials in the `.env` file

        This method navigates to the login page, enters the username and password,
        and then selects the appropriate account. The user must manually complete the
        CAPTCHA before proceeding.

        Args:
            username (str): The username to log in with.
            password (str): The password for the specified username.

        Raises:
            PlaywrightTimeoutError: If any page elements fail to load within the
            timeout period.

        Notes:
            - The CAPTCHA must be completed manually. Automation pauses to allow the
              user to handle it.
            - A delay may be introduced for bad connections using a fail-safe.
        """
        # TODO: add fail-safe for bad connection
        self.page.goto(self.URL_LOGIN, timeout=120_000)

        # Login Form
        input_username = self.page.locator("#ed_username")
        input_username.wait_for(state="visible")
        input_username.focus()
        input_username.type(username)
        input_password = self.page.locator("#ed_password")
        input_password.wait_for()
        input_password.type(password)
        input_password.press("Enter")

        # Account card
        card_account = self.page.locator(
            "div.account-select-card:has-text('Bendahara Umum Daerah')"
        )
        btn_account = card_account.locator("button:has-text('Pilih Akun ini')")
        card_account.wait_for()
        btn_account.click()

        # CAPTCHA form
        self.page.bring_to_front()
        input("Press Enter after successful login...")

        # Sidebar - Akuntansi
        menu_link = self.page.locator('a:has-text("Akuntansi")').first
        menu_link.wait_for(timeout=120_000)

    def login_with_cookies(self):
        """
        Log in to SIPD-RI using the previously saved session cookies. It will load
        cookie file named `cookie.json`.

        Raises:
            FileNotFoundError: If the `cookies.json` file does not exist.
            json.JSONDecodeError: If the `cookies.json` file contains invalid JSON.

        Notes:
            - The method assumes that the `cookies.json` file exists and contains valid cookies.
            - If the cookies are expired or invalid, the session will not be authenticated
              successfully.

        """
        try:
            with open("cookies.json", "r", encoding="utf-8") as f:
                cookies = json.load(f)
                self.context.add_cookies(cookies)

            self.page.goto(self.URL_LOGIN, timeout=120_000)
            self.page.bring_to_front()
            self.page.wait_for_url("**/dashboard", timeout=300_000)

        except json.JSONDecodeError:
            # For expired or invalid session cookie.
            os.remove("cookies.json")
            self.login()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def download_realisasi(self, output_dir: str, start_month=1, end_month=1):
        """
        Downloads realisasi reports for specified months from the SIPD system.

        Args:
            output_dir (str): The output directory where the file will be saved
            start_month (int): The starting month (1-12).
            end_month (int): The ending month (1-12).

        Notes:
            - Handles potential errors during navigation, element interaction, and downloads.
            - Downloads reports for each month between `start_month` and `end_month`, inclusive.
            - Ensures robust handling of unexpected issues, such as timeouts or invalid months.

        Raises:
            Exception: If a critical error occurs during the process.

        To-do:
            - [ ] add output_path parameter
        """
        try:
            url = (
                self.URL_PENATAUSAHAAN + "/penatausahaan/pengeluaran/laporan/realisasi"
            )
            self.page.goto(url)
            menu_title = self.page.locator('h1:has-text("Laporan Realisasi")')
            menu_title.wait_for()

            # Download form - SKPD
            submenu_skpd = self.page.locator("div.css-j93siq input").first
            submenu_skpd.wait_for()
            submenu_skpd.click()
            submenu_skpd.type("Unduh Semua SKPD")
            submenu_skpd.press("Enter")

            for i in range(start_month, end_month + 1):
                print(f"({i}/{end_month}) --- Downloading file...")

                try:
                    # Download form - Bulan
                    submenu_bulan = self.page.locator("div.css-j93siq input").nth(1)
                    submenu_bulan.wait_for(timeout=60_000)
                    submenu_bulan.click()
                    submenu_bulan.type(get_month_name(i))
                    submenu_bulan.press("Enter")

                    try:
                        with self.page.expect_download(
                            timeout=120_000
                        ) as download_info:
                            btn_download = self.page.locator(
                                'button:has-text("Download")'
                            )
                            btn_download.click()

                        # FIXME: remove the output_dir naming, use the parameter instead
                        download_name = f"2024-{i:02d}-Laporan Realisasi.xlsx"
                        download_path = f"{output_dir}/{download_name}"

                        download_file = download_info.value
                        download_file.save_as(download_path)

                        print(
                            f"({i}/{end_month}) --- Download success! File saved as {download_name}"
                        )

                    except PlaywrightTimeoutError as e:
                        print(f"({i}/{end_month}) --- Download failed: {e}")
                        print("Retrying...")
                        # TODO: Retry logic for failed downloads.

                except IndexError:  # Catching month values > 12
                    print(
                        f"({i}/{end_month}) --- Invalid month! There are only 12 months."
                    )

                except Exception as e:
                    print(f"({i}/{end_month}) --- Unexpected error: {e}")
                    print("Skipping to the next month.")

        except PlaywrightTimeoutError as e:
            print(f"Page load timed out: {e}")

        except Exception as e:
            print(f"Critical error occurred: {e}")

    def input_jurnal_umum(self):
        """
        Steps:

        - Masuk ke menu Jurnal Umum
        - Pilih sub-menu Input Jurnal Umum
        - User input secara manual:
            - Pilih SKPD
            - Tanggal Jurnal
            - Tanggal Dokumen Sumber
            - No. Dokumen Sumber
            - Unggah Dokumen Sumber
            - Keterangan
        - Isi drop-down Kode Rekening dengan "type" (bukan click atau fill)
        - Wait sampai akunnya muncul
        - Isi Debit atau Kredit
        - Klik tambah
        - Klik simpan manual oleh user
        """
        print(">>>>>>>>>>>>> START TEST")
        print(">>>>>>>>>>>>> Input Jurnal Umum")

        try:
            self.page.goto(self.URL_AKLAP)
            while self.is_404():
                self.page.goto(self.URL_AKLAP)

            # Menu
            menu_jurnal_umum = self.page.locator('a:has-text("Jurnal Umum")').first
            menu_jurnal_umum.wait_for()
            menu_jurnal_umum.click()

            # Sub-menu
            submenu_jurnal_umum = self.page.locator(
                'a:has-text("Input Jurnal Umum")'
            ).first
            submenu_jurnal_umum.wait_for()
            submenu_jurnal_umum.click()

            # Delay for user input
            input("Press Enter to continue...")

            # Input - Kode Rekening
            kode_rek_id = "#__BVID__225"

            kode_rek_form = self.page.locator(f"{kode_rek_id} input")
            kode_rek_form.scroll_into_view_if_needed()
            kode_rek_form.click()
            kode_rek_form.type("5.2.01")

            btn_next = self.page.locator(f'{kode_rek_id} button:has-text("Next")')
            btn_next.wait_for()

            kode_rek_form.press("Enter")

            # Input - Debit/Kredit
            debit_id = "#__BVID__230"
            kredit_id = "#__BVID__232"

            debit_form = self.page.locator(f"{debit_id} input")
            debit_form.click()
            debit_form.type("26348500")

            # --------- TEST
            input("Cek debit/kredit")
            debit_form.clear()
            # --------- TEST

            kredit_form = self.page.locator(f"{kredit_id} input")
            kredit_form.click()
            kredit_form.type("123500")

            # Tambah
            tambah_id = "#__BVID__235"
            btn_tambah = self.page.locator(f'{tambah_id} button:has-text("Tambah")')
            btn_tambah.click()

            input(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HERE")

        except Exception as e:
            print(e)

        print(">>>>>>>>>>>>> END TEST")
