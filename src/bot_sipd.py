"""
A module for automating interactions with SIPD-RI Kemendagri Website.
"""

import os
import time
import json

from src.utils import get_month_name

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


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
        ! DEV ONLY !

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
        Downloads `Laporan Realisasi` for specified months from SIPD.

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

    def posting_jurnal_belanja(self):
        """
        Steps:

        - Masuk ke menu Posting Jurnal
        - Pilih sub-menu Belanja
        - User input secara manual:
            - Pilih SKPD
            - Filter Keyword sesuai dengan kebutuhan untuk Belanja yang harus di-approve dengan
        """
        try:
            self.page.goto(self.URL_AKLAP)
            while self.is_404():
                self.page.goto(self.URL_AKLAP)

            # Menu
            menu_posting_jurnal = self.page.locator(
                'a:has-text("Posting Jurnal")'
            ).first
            menu_posting_jurnal.wait_for()
            menu_posting_jurnal.click()

            # Sub-menu
            submenu_belanja = self.page.locator('a:has-text("Belanja")').first
            submenu_belanja.wait_for()
            submenu_belanja.click()

            # Delay for user input
            print(">>>>>>>>>>> Posting Jurnal Belanja Start")
            input("Press Enter to continue...")

            # Dropdown - Status
            dropdown_status = self.page.locator("#vs5__combobox input")
            dropdown_status.wait_for()
            dropdown_status.click()
            dropdown_status.type("Belum di posting")
            dropdown_status.press("Enter")

            # Filter - Dropdown
            dropdown_filter = self.page.locator(
                'div:has-text("Filter By Keyword") select'
            ).first
            dropdown_filter.wait_for()
            dropdown_filter.click()
            dropdown_filter.select_option("kode_rekening")

            # Pake tipsnya mbak Uyik, 005 bisa nge-grab 0052, 0053, dst.
            metode_beban = ["5.1.02.01.01.005", "5.1.02.01.01.006", "5.1.02.01.01.007"]
            metode_aset = ["5.1.02.01"]

            input_filter = self.page.locator("input[data-v-01f535b6]").first
            btn_terapkan = self.page.locator('button:has-text("Terapkan")')

            print(">>>>>>>>>>>> Metode Beban Start")
            for jurnal in metode_beban:
                print(f"Metode Beban: {jurnal}\n")

                # Filter - Input
                input_filter.wait_for()
                input_filter.click()
                input_filter.clear()
                input_filter.type(jurnal)

                # Button - Terapkan
                btn_terapkan.wait_for()
                btn_terapkan.click()

                input("Press Enter to continue...")

            print(">>>>>>>>>>>> Metode Aset Start")
            # Filter - Input
            input_filter.wait_for()
            input_filter.click()
            input_filter.clear()
            input_filter.type(metode_aset[0])

            # Button - Terapkan
            btn_terapkan.wait_for()
            btn_terapkan.click()

            input("Press Enter to continue...")

            print("Done iterating")
            input("Press Enter to continue...")

        except Exception as e:
            input("Press enter to show error")
            print(e)

    def input_jurnal_umum(self, jurnal_umum: list):
        """
        Input Jurnal Umum accounts in Jurnal Umum -> Input Jurnal Umum menu using list of
        accounts.

        The list should be formatted as:
            - Kode Rekening
            - Debit
            - Kredit
        Each row should be contained in a list. The first row should be Kode Rekening

        Args:
            jurnal_umum (list): A list of Jurnal Umum data that consist of Kode Rekening,
            Debit, and Kredit.

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
            print(">>>>>> Input jurnal mulai")
            input("Press Enter to continue...")

            for i in jurnal_umum:
                kode_rekening = str(i[0])
                debit = str(i[1])
                kredit = str(i[2])

                # Input - Kode Rekening
                kode_rek_id = "#__BVID__224"

                kode_rek_form = self.page.locator(f"{kode_rek_id} input")
                kode_rek_form.scroll_into_view_if_needed()
                kode_rek_form.click()
                kode_rek_form.type(kode_rekening)
                time.sleep(1.5)

                btn_next = self.page.locator(f'{kode_rek_id} button:has-text("Next")')
                btn_next.wait_for()
                time.sleep(0.5)

                kode_rek_form.press("Enter")

                # Input - Debit/Kredit
                debit_id = "#__BVID__229"
                kredit_id = "#__BVID__231"

                if debit != "nan":
                    debit_form = self.page.locator(f"{debit_id} input")
                    debit_form.click()
                    debit_form.type(debit)

                if kredit != "nan":
                    kredit_form = self.page.locator(f"{kredit_id} input")
                    kredit_form.click()
                    kredit_form.type(kredit)

                # Tambah
                tambah_id = "#__BVID__234"
                btn_tambah = self.page.locator(f'{tambah_id} button:has-text("Tambah")')
                btn_tambah.click()

            input("End input jurnal>>>>")

        except Exception as e:
            print(e)

    def table_scrape(self):
        print("This is table scraping")

        self.page.goto(
            "https://sipd.kemendagri.go.id/penatausahaan/pengeluaran/bku/skpd"
        )
        input("Press Enter to scrape table...")

        tables = self.page.query_selector_all("table")
        if not tables:
            print("No tables found on this page.")
            return

        for i, table in enumerate(tables):
            rows = table.query_selector_all("tr")
            table_data = []
            for row in rows:
                cells = row.query_selector_all("td, th")
                table_data.append([cell.text_content().strip() for cell in cells])

        df = pd.DataFrame(table_data[1:], columns=table_data[0])
        output_file = "sample-table.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Tables is saved in {output_file}.")

    def download_neraca(self, output_dir: str, skpd_list: list):
        """
        Download `Neraca` from `Laporan Keuangan` menu.

        Args:
            output_dir (str): _description_
            skpd_list (list): _description_
        """
        try:
            self.page.goto(self.URL_AKLAP)
            time.sleep(5)
            while self.is_404():
                time.sleep(2)
                self.page.goto(self.URL_AKLAP)

            # Menu - Laporan Keuangan
            menu_lk = self.page.locator('a:has-text("Laporan Keuangan")').first
            menu_lk.wait_for()
            menu_lk.click()

            # Submenu - Neraca
            submenu_lk = self.page.locator('li:has-text("Laporan Keuangan")').first
            submenu_lra = submenu_lk.locator('a:has-text("Neraca")').first
            submenu_lra.wait_for()
            submenu_lra.click()

            # Iterate SKPD start
            for skpd in skpd_list:
                print(f"Download start   - {skpd}")

                # Dropdown - Pilih SKPD
                id_skpd = "__BVID__111"
                pilih_skpd = self.page.locator(f"#{id_skpd} input")
                pilih_skpd.scroll_into_view_if_needed()
                pilih_skpd.click()
                pilih_skpd.type(skpd)
                time.sleep(0.3)
                pilih_skpd.press("Enter")

                # Dropdown - Pilih Klasifikasi
                id_klasifikasi = "__BVID__116"
                input_klasifikasi = self.page.locator(f"#{id_klasifikasi} input")
                input_klasifikasi.click()
                input_klasifikasi.type("Sub Rincian Objek")
                time.sleep(0.3)
                input_klasifikasi.press("Enter")

                # Dropdown - Konsolidasi SKPD
                id_konsolidasi = "__BVID__132"
                input_konsolidasi = self.page.locator(f"#{id_konsolidasi} select")
                input_konsolidasi.click()
                # Selecting `SKPD dan Unit Konsolidasi`
                input_konsolidasi.select_option("skpd_mandiri")

                # Button - Terapkan
                btn_terapkan = self.page.locator('button:has-text("Terapkan")').first
                btn_terapkan.wait_for()
                btn_terapkan.click()

                # Button - Cetak
                btn_cetak = self.page.locator('button:has-text("Cetak")').first
                btn_cetak.wait_for()
                btn_cetak.click()

                # File download
                with self.page.expect_download(timeout=120_000) as download_info:
                    # Button - Cetak Sub-Menu
                    btn_cetak_menu = self.page.locator(
                        'ul li a:has-text("Excel")'
                    ).first
                    btn_cetak_menu.wait_for()
                    btn_cetak_menu.click()

                download_name = f"Neraca - {skpd}.xlsx"
                download_path = f"{output_dir}/{download_name}"

                download_file = download_info.value
                download_file.save_as(download_path)

                print(f"Download success - {skpd}")
                print()

                # TODO: add retry logic for failed downloads

            input(">>>>>>>>>>>>>>>>>>>>> Sample end")

        except Exception as e:
            print(f"Critical error occurred: {e}")

    def download_lra(self, output_dir: str, skpd_list: list):
        """
        Download `Laporan Realisasi Anggaran` from `Laporan Keuangan` menu.

        Args:
            output_dir (str): _description_
            skpd_list (list): _description_
        """
        try:
            self.page.goto(self.URL_AKLAP)
            time.sleep(5)
            while self.is_404():
                time.sleep(2)
                self.page.goto(self.URL_AKLAP)

            # Menu - Laporan Keuangan
            menu_lk = self.page.locator('a:has-text("Laporan Keuangan")').first
            menu_lk.wait_for()
            menu_lk.click()

            # Submenu - LRA
            submenu_lk = self.page.locator('li:has-text("Laporan Keuangan")').first
            submenu_lra = submenu_lk.locator('a:has-text("LRA")').first
            submenu_lra.wait_for()
            submenu_lra.click()

            # Iterate SKPD start
            for skpd in skpd_list:
                print(f"Download start   - {skpd}")

                # Dropdown - Pilih SKPD
                id_skpd = "__BVID__111"
                pilih_skpd = self.page.locator(f"#{id_skpd} input")
                pilih_skpd.scroll_into_view_if_needed()
                pilih_skpd.click()
                pilih_skpd.type(skpd)
                time.sleep(0.3)
                pilih_skpd.press("Enter")

                # Dropdown - Pilih Klasifikasi
                id_klasifikasi = "__BVID__116"
                input_klasifikasi = self.page.locator(f"#{id_klasifikasi} input")
                input_klasifikasi.click()
                input_klasifikasi.type("Sub Rincian Objek")
                time.sleep(0.3)
                input_klasifikasi.press("Enter")

                # Dropdown - Konsolidasi SKPD
                id_konsolidasi = "__BVID__132"
                input_konsolidasi = self.page.locator(f"#{id_konsolidasi} select")
                input_konsolidasi.click()
                # Selecting `SKPD dan Unit Konsolidasi`
                input_konsolidasi.select_option("skpd_mandiri")

                # Button - Terapkan
                btn_terapkan = self.page.locator('button:has-text("Terapkan")').first
                btn_terapkan.wait_for()
                btn_terapkan.click()

                # Button - Cetak
                btn_cetak = self.page.locator('button:has-text("Cetak")').first
                btn_cetak.wait_for()
                btn_cetak.click()

                # File download
                with self.page.expect_download(timeout=120_000) as download_info:
                    # Button - Cetak Sub-Menu
                    btn_cetak_menu = self.page.locator(
                        'ul li a:has-text("Excel")'
                    ).first
                    btn_cetak_menu.wait_for()
                    btn_cetak_menu.click()

                download_name = f"LRA - {skpd}.xlsx"
                download_path = f"{output_dir}/{download_name}"

                download_file = download_info.value
                download_file.save_as(download_path)

                print(f"Download success - {skpd}")
                print()

                # TODO: add retry logic for failed downloads

            input(">>>>>>>>>>>>>>>>>>>>> Sample end")

        except Exception as e:
            print(f"Critical error occurred: {e}")

    def download_lo(self, output_dir: str, skpd_list: list):
        """
        Download `Laporan Operasional` from `Laporan Keuangan` menu.

        Args:
            output_dir (str): _description_
            skpd_list (list): _description_
        """
        try:
            self.page.goto(self.URL_AKLAP)
            time.sleep(5)
            while self.is_404():
                time.sleep(2)
                self.page.goto(self.URL_AKLAP)

            # Menu - Laporan Keuangan
            menu_lk = self.page.locator('a:has-text("Laporan Keuangan")').first
            menu_lk.wait_for()
            menu_lk.click()

            # Submenu - LO
            submenu_lk = self.page.locator('li:has-text("Laporan Keuangan")').first
            submenu_lra = submenu_lk.locator('a:has-text("LO")').first
            submenu_lra.wait_for()
            submenu_lra.click()

            # Iterate SKPD start
            for skpd in skpd_list:
                print(f"Download start   - {skpd}")

                # Dropdown - Pilih SKPD
                id_skpd = "__BVID__111"
                pilih_skpd = self.page.locator(f"#{id_skpd} input")
                pilih_skpd.scroll_into_view_if_needed()
                pilih_skpd.click()
                pilih_skpd.type(skpd)
                time.sleep(0.3)
                pilih_skpd.press("Enter")

                # Dropdown - Pilih Klasifikasi
                id_klasifikasi = "__BVID__116"
                input_klasifikasi = self.page.locator(f"#{id_klasifikasi} input")
                input_klasifikasi.click()
                input_klasifikasi.type("Sub Rincian Objek")
                time.sleep(0.3)
                input_klasifikasi.press("Enter")

                # Dropdown - Konsolidasi SKPD
                id_konsolidasi = "__BVID__132"
                input_konsolidasi = self.page.locator(f"#{id_konsolidasi} select")
                input_konsolidasi.click()
                # Selecting `SKPD dan Unit Konsolidasi`
                input_konsolidasi.select_option("skpd_mandiri")

                # Button - Terapkan
                btn_terapkan = self.page.locator('button:has-text("Terapkan")').first
                btn_terapkan.wait_for()
                btn_terapkan.click()

                # Button - Cetak
                btn_cetak = self.page.locator('button:has-text("Cetak")').first
                btn_cetak.wait_for()
                btn_cetak.click()

                # File download
                with self.page.expect_download(timeout=120_000) as download_info:
                    # Button - Cetak Sub-Menu
                    btn_cetak_menu = self.page.locator(
                        'ul li a:has-text("Excel")'
                    ).first
                    btn_cetak_menu.wait_for()
                    btn_cetak_menu.click()

                download_name = f"LO - {skpd}.xlsx"
                download_path = f"{output_dir}/{download_name}"

                download_file = download_info.value
                download_file.save_as(download_path)

                print(f"Download success - {skpd}")
                print()

                # TODO: add retry logic for failed downloads

            input(">>>>>>>>>>>>>>>>>>>>> Sample end")

        except Exception as e:
            print(f"Critical error occurred: {e}")

    def download_lpe(self, output_dir: str, skpd_list: list):
        """
        Download `Laporan Perubahan Ekuitas` from `Laporan Keuangan` menu.

        Args:
            output_dir (str): _description_
            skpd_list (list): _description_
        """
        try:
            self.page.goto(self.URL_AKLAP)
            time.sleep(5)
            while self.is_404():
                time.sleep(2)
                self.page.goto(self.URL_AKLAP)

            # Menu - Laporan Keuangan
            menu_lk = self.page.locator('a:has-text("Laporan Keuangan")').first
            menu_lk.wait_for()
            menu_lk.click()

            # Submenu - LPE
            submenu_lk = self.page.locator('li:has-text("Laporan Keuangan")').first
            submenu_lra = submenu_lk.locator('a:has-text("LPE")').first
            submenu_lra.wait_for()
            submenu_lra.click()

            # Iterate SKPD start
            for skpd in skpd_list:
                print(f"Download start   - {skpd}")

                # Dropdown - Pilih SKPD
                id_skpd = "__BVID__111"
                pilih_skpd = self.page.locator(f"#{id_skpd} input")
                pilih_skpd.scroll_into_view_if_needed()
                pilih_skpd.click()
                pilih_skpd.type(skpd)
                time.sleep(0.3)
                pilih_skpd.press("Enter")

                # Dropdown - Pilih Klasifikasi
                id_klasifikasi = "__BVID__116"
                input_klasifikasi = self.page.locator(f"#{id_klasifikasi} input")
                input_klasifikasi.click()
                input_klasifikasi.type("Sub Rincian Objek")
                time.sleep(0.3)
                input_klasifikasi.press("Enter")

                # Dropdown - Konsolidasi SKPD
                id_konsolidasi = "__BVID__133"
                input_konsolidasi = self.page.locator(f"#{id_konsolidasi} select")
                input_konsolidasi.click()
                # Selecting `SKPD dan Unit Konsolidasi`
                input_konsolidasi.select_option("skpd_mandiri")

                # Button - Terapkan
                btn_terapkan = self.page.locator('button:has-text("Terapkan")').first
                btn_terapkan.wait_for()
                btn_terapkan.click()

                # Button - Cetak
                btn_cetak = self.page.locator('button:has-text("Cetak")').first
                btn_cetak.wait_for()
                btn_cetak.click()

                # File download
                with self.page.expect_download(timeout=120_000) as download_info:
                    # Button - Cetak Sub-Menu
                    btn_cetak_menu = self.page.locator('ul li a:has-text("PDF")').first
                    btn_cetak_menu.wait_for()
                    btn_cetak_menu.click()

                download_name = f"LPE - {skpd}.pdf"
                download_path = f"{output_dir}/{download_name}"

                download_file = download_info.value
                download_file.save_as(download_path)

                print(f"Download success - {skpd}")
                print()

                # TODO: add retry logic for failed downloads

            input(">>>>>>>>>>>>>>>>>>>>> Sample end")

        except Exception as e:
            print(f"Critical error occurred: {e}")

    def download_buku_jurnal(self, output_dir: str, skpd_list: list):
        """
        Download `Laporan Perubahan Ekuitas` from `Laporan Keuangan` menu.

        Args:
            output_dir (str): _description_
            skpd_list (list): _description_
        """
        try:
            self.page.goto(self.URL_AKLAP)
            time.sleep(2)
            while self.is_404():
                time.sleep(2)
                self.page.reload()

            # Menu - Laporan Keuangan
            menu_buku_jurnal = self.page.locator('a:has-text("Buku Jurnal")').first
            menu_buku_jurnal.wait_for()
            menu_buku_jurnal.click()

            # Iterate SKPD start
            for skpd in skpd_list:
                print(f"\nDownload start   - {skpd}")

                title_skpd = self.page.locator('div:has-text("SKPD")')

                # Dropdown - Pilih SKPD
                pilih_skpd = title_skpd.locator("input").first
                pilih_skpd.scroll_into_view_if_needed()
                pilih_skpd.click()
                time.sleep(0.3)
                pilih_skpd.type(skpd)
                time.sleep(0.3)
                pilih_skpd.press("Enter")

                # Button - Terapkan
                btn_terapkan = self.page.locator('button:has-text("Terapkan")').first
                btn_terapkan.wait_for()
                btn_terapkan.click()
                time.sleep(1)

                # Button - Cetak
                btn_cetak = self.page.locator('button:has-text("Cetak")').first
                btn_cetak.wait_for()
                btn_cetak.click()

                # File download
                try:
                    download_timeout = 60_000

                    with self.page.expect_download(
                        timeout=download_timeout
                    ) as download_info:
                        # Button - Cetak Sub-Menu
                        btn_cetak_menu = self.page.locator(
                            'ul li a:has-text("EXCEL")'
                        ).first
                        btn_cetak_menu.wait_for()
                        btn_cetak_menu.click()

                        # Error popup - "Gagal Cetak"
                        try:
                            error_popup = self.page.locator(
                                'div div h2:has-text("Gagal Cetak")'
                            )
                            error_popup.wait_for(state="visible", timeout=10_000)

                            print("Gagal Cetak!")

                            error_button = self.page.locator(
                                'button:has-text("OK")'
                            ).first
                            error_button.click()

                            continue

                        except Exception:
                            pass

                    download_name = f"Buku Jurnal - {skpd}.xlsx"
                    download_path = f"{output_dir}/{download_name}"

                    download_file = download_info.value
                    download_file.save_as(download_path)

                    print(f"Download success - {skpd}")

                except PlaywrightTimeoutError as e:
                    print(f"Download error for {skpd}: {e}")
                    self.page.reload()

                    while self.is_404():
                        time.sleep(2)
                        self.page.reload()

                    # TODO: add retry logic for failed downloads

                except Exception as e:
                    # TODO: there are some SKPD that can't be downloaded using "Semua Transaksi"
                    #       A pop-up that says "Gagal Cetak" will show up.
                    print(f"Download error: {e}")
                    self.page.reload()

                    while self.is_404():
                        time.sleep(2)
                        self.page.reload()

            input(">>>>>>>>>>>>>>>>>>>>> Sample end")

        except Exception as e:
            print(f"Critical error occurred: {e}")
