from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_reddit(subreddit_url, scroll_limit=3):
    print("🚀 Launching Chrome browser...")

    options = Options()
    # 👇 Temporarily comment out for testing in visible mode
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(subreddit_url)
    time.sleep(3)

    for _ in range(scroll_limit):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    print("🔍 Locating post containers...")
    posts = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='post-container']")
    print(f"📦 Total posts found: {len(posts)}")

    results = []

    for post in posts:
        try:
            title = post.find_element(By.CSS_SELECTOR, 'h3').text
        except:
            title = None

        try:
            post_url = post.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except:
            post_url = None

        try:
            author = post.find_element(By.CSS_SELECTOR, 'a[data-click-id="user"]').text
        except:
            author = None

        try:
            upvotes = post.find_element(By.CSS_SELECTOR, 'div[data-click-id="upvote"]').text
        except:
            upvotes = None

        try:
            comments = post.find_element(By.XPATH, ".//span[contains(text(), 'comment')]").text
        except:
            comments = None

        try:
            time_posted = post.find_element(By.CSS_SELECTOR, "a[data-click-id='timestamp']").text
        except:
            time_posted = None

        results.append({
            "title": title,
            "url": post_url,
            "author": author,
            "upvotes": upvotes,
            "comments": comments,
            "time_posted": time_posted,
        })

    driver.quit()

    return results
