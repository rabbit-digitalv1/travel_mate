from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

# 👇 Ensure headless is OFF
# options.add_argument("--headless")

print("🚀 Attempting to open Chrome...")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.google.com")

input("🔍 Press Enter to quit browser...")  # keep browser open

driver.quit()
