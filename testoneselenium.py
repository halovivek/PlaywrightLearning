from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import glob
from datetime import datetime
import time
import sys

def run():
    # 1. Open the browser (Switching to Chrome as requested/fallback)
    # Ensure you have 'chromedriver' installed and in your PATH.
    
    options = Options()
    # options.add_argument("--headless") # Uncomment to run in headless mode
    
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        print("Ensure you have Chrome installed and 'chromedriver' in your PATH.")
        sys.exit(1)
    
    try:
        # 2. go to website www.yahoo.com
        driver.get("https://www.yahoo.com")

        # 3. find the search & 4. enter the text halovivek
        # Yahoo's search input typically has name="p"
        # Wait for the element to be present
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "p")))
        
        search_box.send_keys("halovivek")

        # 5. Click the search button (or press Enter)
        
        # Capture current window handles to detect if a new one opens
        initial_handles = driver.window_handles
        
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the new windows or New tab or existing tab to load the search results
        time.sleep(3) # Short wait to allow new window to trigger if any
        
        # Switch to the new window or tab or stay in the existing tab
        current_handles = driver.window_handles
        if len(current_handles) > len(initial_handles):
            # New page opened, switch to the new one (usually the last one)
            new_window = [h for h in current_handles if h not in initial_handles][-1]
            driver.switch_to.window(new_window)
            print("Switched to new window/tab.")
        else:
            print("Staying in existing tab.")
            
        # Once the results are loaded
        # We can wait for the title to contain the search term or some element to appear
        wait.until(EC.title_contains("halovivek"))

        # 6. take the screenshot and save
        # Format: filenameDDMMYYYY_Time
        now = datetime.now()
        timestamp = now.strftime("%d%m%Y_%H%M%S")
        screenshot_filename = f"yahoo_search_results_{timestamp}.png"
        
        # Save screenshot
        driver.save_screenshot(screenshot_filename)
        
        # Get absolute path and print it
        absolute_path = os.path.abspath(screenshot_filename)
        print(f"Screenshot saved at: {absolute_path}")

    finally:
        # 7. close the browser
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run()
