from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://www.example.com/deals')

time.sleep(5)  # Wait for JavaScript to load content

deals = []
items = driver.find_elements(By.CLASS_NAME, 'deal-item')
for item in items:
    title = item.find_element(By.TAG_NAME, 'h2').text
    discount = item.find_element(By.CLASS_NAME, 'discount').text
    expiry = item.find_element(By.CLASS_NAME, 'expiry').text
    deals.append({'title': title, 'discount': discount, 'expiry': expiry})

driver.quit()
print(deals)
