# Book Web Scraper & Analyzer

A data collection and analytics pipeline built in Python. This project extracts, sanitizes, and evaluates inventory data from a book catalog.

## Features
- **Data Scraping:** Uses `Requests` and `BeautifulSoup` to systematically parse multi-page book listings.
- **Data Cleaning:** Normalizes messy data artifacts, strips currency encoding anomalies, and transforms ratings into clean mathematical integers.
- **Data Exporting:** Automatically saves formatted datasets into distinct tracking spreadsheets using `pandas`.
- **Analytics:** Includes a dedicated script to compute pricing stats and filter top-tier stock.
