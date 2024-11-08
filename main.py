import os
import time
import winsound

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

URL_SIPD_LOGIN = "https://sipd.kemendagri.go.id/penatausahaan/login"
URL_SIPD_AKLAP = "https://sipd.kemendagri.go.id/penatausahaan/aklap"


def play_notification():
    sound_path = "assets/notification.wav"
    try:
        winsound.PlaySound(sound_path, winsound.SND_FILENAME)
    except KeyboardInterrupt:
        pass


class SIPDBot:
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

    def _login(self):
        if not self.page:
            self._initialize_browser()

        # TODO: add fail-safe for bad connection
        self.page.goto(URL_SIPD_LOGIN, timeout=60_000)

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
        play_notification()

        # Sidebar - Akuntansi
        # TODO: change wait for a more universal element e.g. title
        menu_link = self.page.locator('a:has-text("Akuntansi")').first
        # TODO: add fail-safe method
        menu_link.wait_for(timeout=60_000)

        time.sleep(5)
        print(">>>>>>>>>>>>>>>>>>>>>>HERE")

    def close_browser(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()

    def download_realisasi(self):
        self._login()

        url_realisasi = "https://sipd.kemendagri.go.id/penatausahaan/penatausahaan/pengeluaran/laporan/realisasi"
        self.page.goto(url_realisasi)

        menu_title = self.page.locator('h1:has-text("Laporan Realisasi")')
        menu_title.wait_for()

        # Download form
        submenu_skpd = self.page.locator("div.css-j93siq input").first
        submenu_skpd.wait_for()
        submenu_skpd.click()
        submenu_skpd.type("Unduh Semua SKPD")
        submenu_skpd.press("Enter")

        submenu_bulan = self.page.locator("div.css-j93siq input").nth(1)
        submenu_bulan.wait_for()
        submenu_bulan.click()
        submenu_bulan.type("Januari")
        submenu_bulan.press("Enter")

        with self.page.expect_download(timeout=60_000) as download_info:
            btn_download = self.page.locator('button:has-text("Download")')
            btn_download.click()

        download_file = download_info.value
        download_file.save_as(download_file.suggested_filename)

        print("SAMPLE >>>>>>>>>>>>>>>")
        time.sleep(5)


def main():
    username = os.getenv("SIPD_USERNAME")
    password = os.getenv("SIPD_PASSWORD")

    bot = SIPDBot(username=username, password=password)
    bot.download_realisasi()
    bot.close_browser()


if __name__ == "__main__":
    main()
