from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


class WikipediaScraper:
    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = driver_path
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Initialize Selenium WebDriver with options."""
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=options)

    def scrape_tables(self):
        """Extract tables from the Wikipedia page."""
        self.driver.get(self.url)
        time.sleep(3)  # Wait for page to load
        tables = self.driver.find_elements(By.TAG_NAME, "table")
        all_data = []

        for table in tables:
            rows = table.find_elements(By.TAG_NAME, "tr")
            table_data = []
            for row in rows:
                cols = row.find_elements(
                    By.TAG_NAME, "th") + row.find_elements(By.TAG_NAME, "td")
                table_data.append([col.text.strip() for col in cols])

            df = pd.DataFrame(table_data)
            all_data.append(df)

        return all_data

    def save_merged_table_to_csv(self, all_data):
        """Merge all extracted tables into one CSV file."""
        merged_df = pd.concat(all_data, ignore_index=True)
        merged_df.to_csv("merged_data_version_tables.csv",
                         index=False, header=False)
        print("Scraping complete. Merged table saved as CSV file.")

    def close_driver(self):
        """Close the Selenium driver."""
        self.driver.quit()


# Usage
if __name__ == "__main__":
    url = "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information"
    driver_path = "C:/Windows/chromedriver.exe"  # Update path if needed

    scraper = WikipediaScraper(url, driver_path)
    tables = scraper.scrape_tables()
    scraper.save_merged_table_to_csv(tables)
    scraper.close_driver()
