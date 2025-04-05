from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_reddit(subreddit_url, scroll_limit=3):
    print("🚀 Launching Chrome browser...")

    options = Options()
    # options.add_argument("--headless=new")  # Disable headless for testing
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(subreddit_url)

    wait = WebDriverWait(driver, 10)

    # ✅ Wait for first post container to be visible
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='post-container']")))
    except:
        print("⚠️ Post container not found.")
        driver.quit()
        return []

    # ✅ Scroll to load more
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
