import csv
import os
import tempfile
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException


firefox_profile_temp = Path.home() / '.cache' / 'news-scraper' / 'firefox-profiles'
firefox_profile_temp.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(firefox_profile_temp)
tempfile.tempdir = str(firefox_profile_temp)

# Start a Selenium webdriver with Firefox using GeckoDriverManager to manage the driver
try:
    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=firefox_options,
    )
except WebDriverException as firefox_error:
    print(f"Firefox could not start ({firefox_error}). Falling back to Chrome.")
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

# URL of the news website you want to scrape
url = 'https://indianexpress.com/'

# Open the webpage
driver.get(url)

# Find all links containing 'article' in their href attribute
article_links = []
links = driver.find_elements(By.TAG_NAME, 'a')
for link in links:
    href = link.get_attribute('href')
    if href and 'article' in href:
        article_links.append(href)

# Close the webdriver
driver.quit()

# Write article links to a CSV file
with open('article_links.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Article Links'])
    for article_link in article_links:
        writer.writerow([article_link])

print("Article links saved to article_links.csv")

