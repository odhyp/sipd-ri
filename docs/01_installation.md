# :wrench: Installation

## Using the Pre-Built `.exe`

1. **Download the Latest Release**: Go to the [releases page]() and download the latest `.exe` file for your system.
2. **Run the Application**: Once downloaded, simply double-click the `.exe` file to launch the app.

## Optional: Running from Source Code

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
