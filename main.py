import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Start a Selenium webdriver with Firefox using GeckoDriverManager to manage the driver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
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

