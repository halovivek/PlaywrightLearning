# TN REGINET Scraper

A robust Python automation tool built with Playwright to extract Encumbrance Certificate (EC) related data from the [TNREGINET Portal](https://tnreginet.gov.in/portal).

## 🚀 Overview

This script automates the tedious process of manually navigating through the Tamil Nadu Registration Department's website. It recursively scrapes nested dropdown data starting from **Zones** down to **Registration Villages**, ensuring comprehensive data collection for analyses or records.

## ✨ Features

*   **Smart Navigation**: Automatically switches the portal language to English and navigates to the "View EC" section.
*   **Deep Scraping**: Iterates through all available levels:
    *   Zone
    *   District
    *   Sub-Registrar Office (SRO)
    *   Registration Village
*   **Data Persistence**: Saves progress incrementally (after every SRO) to `tnreginet_data.xlsx` to prevent data loss during long scraping sessions.
*   **Robust Error Handling**: Includes retries, fallback toggles, and screenshot capture for navigation failures.
*   **Headful Mode**: Runs with the browser visible for monitoring and debugging.

## 🛠️ Prerequisites

*   Python 3.8+
*   Google Chrome / Chromium

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/tnreginet-scraper.git
    cd tnreginet-scraper
    ```

2.  **Install Dependencies**
    ```bash
    pip install pandas openpyxl playwright
    ```

3.  **Install Playwright Browsers**
    ```bash
    playwright install chromium
    ```

## 💻 Usage

Run the script directly from your terminal:

```bash
python scrape_tnreginet.py
```

### Output
The script generates an Excel file **`tnreginet_data.xlsx`** with the following columns:
1.  Sl.no
2.  Zone
3.  District
4.  Sub-Registrar Office
5.  Registration Village

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Please respect the terms of service of the TNREGINET portal. Ensure you do not overwhelm the server with excessive requests; the script uses sequential processing with waits to be gentle on the target server.

## 📄 License
[MIT](LICENSE)
