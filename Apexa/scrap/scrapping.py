from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up Selenium WebDriver options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Path to ChromeDriver (Update with correct path if needed)
service = Service("C:/Windows/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Open the Wikipedia page
driver.get(
    "https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information")
time.sleep(3)  # Wait for the page to load

# Find all tables
tables = driver.find_elements(By.TAG_NAME, "table")
all_data = []

# Loop through each table and extract data
for table in tables:
    rows = table.find_elements(By.TAG_NAME, "tr")
    table_data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "th") + \
            row.find_elements(By.TAG_NAME, "td")
        table_data.append([col.text.strip() for col in cols])

    # Convert to DataFrame and store
    df = pd.DataFrame(table_data)
    all_data.append(df)

# Close the Selenium driver
driver.quit()

# Save tables to CSV files
for i, df in enumerate(all_data):
    df.to_csv(f"java_version_table_{i+1}.csv", index=False, header=False)

print("Scraping complete. Tables saved as CSV files.")
