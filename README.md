<!-- PROJECT SHIELDS -->

<!-- [![Forks][forks-shield]][forks-url] -->

[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![License][license-shield]][license-url]
[![Sponsor][sponsor-shield]][sponsor-url]

<!-- PROJECT LOGO -->
<br />
<br />
<br />
<div align="center">
  <a href="https://github.com/odhyp/sipd-ri">
    <img src="assets/img/logo_sipd.png" alt="Logo" width="auto" height="80">
  </a>

  <h3 align="center">SIPD-RI</h3>

  <p align="center">
    A simple command-line Python application<br />to help with SIPD-RI and accounting tasks.
    <br />
    <a href="https://github.com/odhyp/sipd-ri"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <br />
    <a href="https://github.com/odhyp/sipd-ri/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/odhyp/sipd-ri/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
    ·
    <a href="">Donate</a>
  </p>
</div>
<br />

TODO: update the donate/sponsor links

<!-- ABOUT THE PROJECT -->

## About This Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)
TODO: update the product screenshot

This project helps SIPD-RI users automate repetitive tasks like downloading reports, scraping tables, and performing batch operations such as approving or inputting data. It also offers additional features like compressing and merging Excel files, as well as converting `.xls` files to the newer `.xlsx` format.

<!-- GETTING STARTED -->

## Getting Started

To get started with this project, you can either run it directly from the source code or use the pre-built `.exe` version for Windows.

### Option 1: Using the Pre-Built `.exe`

1. **Download the Latest Release**: Go to the [releases page]() and download the latest `.exe` file for your system.
2. **Run the Application**: Once downloaded, simply double-click the `.exe` file to launch the app.

### Option 2: Running from Source Code

If you prefer to run the app from source, follow these steps:

1. Make sure you have Python 3.6 (or higher) installed. You can download it from the [official Python website](https://www.python.org/downloads/).
2. Clone the repository to your local machine.
   ```bash
    git clone https://github.com/odhyp/sipd-ri.git && cd sipd-ri
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application
   ```bash
   python main.py
   ```

<!-- USAGE EXAMPLES -->

## Usage

After launching the application (either by running the `.exe` or via Python), you can start using it to automate tasks.

_For more examples, please refer to the [Documentation](https://example.com)_
TODO: update the docs url

<!-- ROADMAP -->

## Roadmap

- SIPDBot
  - [x] Penatausahaan --- Download Realisasi for given month(s)
  - [ ] AKLAP --- Input Jurnal Umum (Penyusutan)
  - [ ] AKLAP --- Posting Jurnal (Approve Jurnal) Belanja
- ExcelHelper
  - [x] compress excel files
  - [x] compile Laporan Realisasi
  - [ ] data cleaning Laporan Realisasi Compile
  - [ ] compress file excel (optional)
  - [ ] create LRA Mingguan
  - [ ] create LRA Bulanan
- Other
  - [x] add utils.py
  - [ ] remove/change test print and time.sleep
  - [ ] add docstring for class and class methods
  - [ ] prettify the print output using `rich`

See the [open issues](https://github.com/odhyp/sipd-ri/issues) for a full list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- ### Top contributors:

<a href="https://github.com/odhyp/sipd-ri/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=odhyp/sipd-ri" alt="contrib.rocks image" />
</a> -->

<!-- LICENSE -->

## License

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
[product-screenshot]: assets/img/product.png
