import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class SIPDBot:
    _URL_LOGIN = "https://sipd.kemendagri.go.id/penatausahaan/login"
    _URL_PENATAUSAHAAN = "https://sipd.kemendagri.go.id/penatausahaan"
    _URL_PENATAUSAHAAN_REALISASI = (
        f"{_URL_PENATAUSAHAAN}/penatausahaan/pengeluaran/laporan/realisasi"
    )
    _URL_AKLAP = "https://sipd.kemendagri.go.id/penatausahaan/aklap"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = None
        self.context = None
        self.page = None

    def _initialize_browser(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=False, args=["--start-maximized"]
        )
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()

    # TODO: add refresh page method, using locator for reusability
    # TODO: add reload page method, using locator for reusability

    def _login(self):
        if not self.page:
            self._initialize_browser()

        # TODO: add fail-safe for bad connection
        self.page.goto(self._URL_LOGIN, timeout=120_000)

        # Login Form
        input_username = self.page.locator("#ed_username")
        input_username.wait_for(state="visible")
        input_username.focus()
        input_username.type(self.username)
        input_password = self.page.locator("#ed_password")
        input_password.wait_for()
        input_password.type(self.password)
        input_password.press("Enter")

        # Account card
        card_account = self.page.locator(
            "div.account-select-card:has-text('Bendahara Umum Daerah')"
        )
        btn_account = card_account.locator("button:has-text('Pilih Akun ini')")
        card_account.wait_for()
        btn_account.click()

        # CAPTCHA form
        # TODO: add input() to delay automation after user fill the CAPTCHA form

        # Sidebar - Akuntansi
        # TODO: change wait for a more universal element e.g. title
        menu_link = self.page.locator('a:has-text("Akuntansi")').first
        # TODO: add fail-safe method
        menu_link.wait_for(timeout=120_000)

        time.sleep(5)
        print(">>>>>>>>>>>>>>>>>>>>>>HERE")

    def start_browser(self):
        self._login()

    def close_browser(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()

    def download_realisasi(self, month=1):
        month_list = [
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni",
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember",
        ]

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DOWNLOAD REALISASI START")

        self.page.goto(self._URL_PENATAUSAHAAN_REALISASI)
        menu_title = self.page.locator('h1:has-text("Laporan Realisasi")')
        menu_title.wait_for()

        # Download form - SKPD
        submenu_skpd = self.page.locator("div.css-j93siq input").first
        submenu_skpd.wait_for()
        submenu_skpd.click()
        submenu_skpd.type("Unduh Semua SKPD")
        submenu_skpd.press("Enter")

        for i in range(month):
            current = i + 1
            print(f"({current}/{month}) --- Downloading file...")

            try:
                # Download form - Bulan
                submenu_bulan = self.page.locator("div.css-j93siq input").nth(1)
                submenu_bulan.wait_for(timeout=60_000)
                submenu_bulan.click()
                submenu_bulan.type(month_list[i])
                submenu_bulan.press("Enter")

                # FIXME: handle error for failed/timeout download
                try:
                    with self.page.expect_download(timeout=120_000) as download_info:
                        btn_download = self.page.locator('button:has-text("Download")')
                        btn_download.click()

                    download_name = f"Laporan Realisasi - {current}.xlsx"
                    download_file = download_info.value
                    download_file.save_as(download_name)

                    print(f"({current}/{month}) --- Download success!")
                    print(f"({current}/{month}) --- File saved as {download_name}")

                except PlaywrightTimeoutError as e:
                    print(f"({current}/{month}) --- Download failed: {e}")
                    # TODO: add retry download for failed downloads

            except IndexError:  # Catching month values > 12
                print(f"({current}/{month}) --- There are only 12 months!")

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>DOWNLOAD REALISASI END")

    def sample(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ACCESS AKLAP START")

        self.page.goto(self._URL_AKLAP)
        time.sleep(5)

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ACCESS AKLAP END")
