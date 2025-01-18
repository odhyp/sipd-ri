<!-- PROJECT SHIELDS -->

[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![License][license-shield]][license-url]
[![Sponsor][sponsor-shield]][sponsor-url]

<!-- PROJECT LOGO -->
<br />
<br />
<div align="center">
  <a href="https://github.com/odhyp/sipd-ri">
    <img src="assets/img/logo_sipd.png" alt="Logo" width="auto" height="80">
  </a>

  <h3 align="center">SIPD-RI</h3>

  <p align="center">
    A simple command-line application<br />to automate SIPD-RI tasks
    <br />
    <a href="https://github.com/odhyp/sipd-ri"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/odhyp/sipd-ri/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/odhyp/sipd-ri/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
    ·
    <a href="https://github.com/sponsors/odhyp">Donate</a>
  </p>
</div>
<br />

<!-- ABOUT THE PROJECT -->

## 🏖️ About This Project

![Product Screenshot](/assets/img/product.png)

TODO: update the product screenshot

This project is a command-line application which helps SIPD-RI users automate repetitive tasks in [SIPD-RI](https://sipd.kemendagri.go.id/landing) web application, such as downloading reports, scraping tables, and performing batch operations such as approving or inputting data.

<!-- FEATURES -->

## 📌 Features

These are the main features that SIPD-RI helper offers:

1. Input Jurnal Umum
2. Download all of Laporan Keuangan components

   > Able to download Neraca, LRA, LO, and LPE for all SKPD (PA or KPA)

3. Download Buku Jurnal

   > For all SKPD (PA or KPA)

4. Download Laporan Realisasi

   > For all months and consolidate them

5. Scrape BKU Pajak Table

Additionally, SIPD-RI helper also provides useful office tasks such as:

1. Compile, compress, and consolidate Excel files

2. Convert `.xls` to `.xlsx`

<!-- GETTING STARTED -->

## 👍 Getting Started

To get started with this project, you can either run it directly from the source code or use the pre-built `.exe` version for Windows.

### Option 1: Using the Pre-Built `.exe`

1. **Download the Latest Release**: Go to the [releases page]() and download the latest `.exe` file for your system.
2. **Run the Application**: Once downloaded, simply double-click the `.exe` file to launch the app.

### Option 2: Running from Source Code

If you prefer to run the app from source, follow these steps:

1. Make sure you have Python 3.13 (or higher) installed. You can download it from the [official Python website](https://www.python.org/downloads/).

2. Clone the repository to your local machine

   ```bash
    git clone https://github.com/odhyp/sipd-ri.git
   ```

3. Navigate to the project directory

   ```bash
   cd sipd-ri
   ```

4. Install Python dependencies

   ```bash
   pip install -r requirements.txt
   ```

5. Install Playwright and its browser binaries

   ```bash
   playwright install
   ```

6. Run the application

   ```bash
   python main.py
   ```

<!-- USAGE EXAMPLES -->

## 📙 Usage

After launching the application (either by running the `.exe` file or via Python), you can begin automating tasks by selecting the desired menu option in the command-line interface.

_For more examples, please refer to the [Documentation](https://example.com)_
TODO: update the docs url

<!-- ROADMAP -->

## 🗺️ Roadmap

- [ ] AKLAP - Posting Jurnal (Belanja)
- [ ] Penatausahaan - Scrape BKU Pajak
- [ ] Data cleaning Laporan Realisasi Compile
- [ ] Convert `.xls` to `.xlsx`
- [ ] remove/change test print and time.sleep
- [ ] add docstring for class and class methods
- [ ] prettify the print output and add progress bar using `rich`

See the [open issues](https://github.com/odhyp/sipd-ri/issues) for a full list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## 💌 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this project better, please fork the repo and create a pull request. You can also simply [open an issue](https://github.com/odhyp/sipd-ri/issues/new?template=feature_request.md) for a feature request.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit your Changes (`git commit -m 'Add some YourFeature'`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/odhyp/sipd-ri/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=odhyp/sipd-ri" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->

## 💼 License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/odhyp/sipd-ri.svg?style=for-the-badge
[contributors-url]: https://github.com/odhyp/sipd-ri/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/odhyp/sipd-ri.svg?style=for-the-badge
[forks-url]: https://github.com/odhyp/sipd-ri/network/members
[stars-shield]: https://img.shields.io/github/stars/odhyp/sipd-ri.svg?style=for-the-badge
[stars-url]: https://github.com/odhyp/sipd-ri/stargazers
[issues-shield]: https://img.shields.io/github/issues/odhyp/sipd-ri.svg?style=for-the-badge
[issues-url]: https://github.com/odhyp/sipd-ri/issues
[license-shield]: https://img.shields.io/github/license/odhyp/sipd-ri.svg?style=for-the-badge
[license-url]: https://github.com/odhyp/sipd-ri/blob/master/LICENSE
[sponsor-url]: https://github.com/sponsors/odhyp
[sponsor-shield]: https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#white
