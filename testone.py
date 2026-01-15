from playwright.sync_api import sync_playwright
import os
from datetime import datetime

def run():
    with sync_playwright() as p:
        # 1. Open the firefox browser
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        # 2. go to website www.yahoo.com
        # Yahoo can be slow to fully load all resources (ads, etc.), so we wait for DOMContentLoaded
        page.goto("https://www.yahoo.com", wait_until="domcontentloaded", timeout=60000)

        # 3. find the search & 4. enter the text halovivek
        # Yahoo's search input typically has name="p"
        page.fill('input[name="p"]', "halovivek")

        # 5. Click the search button
        # We use Enter to submit the form, which is equivalent to clicking the search button.
        # This is more robust than looking for a specific button ID that might change.
        
        # Capture current pages to detect if a new one opens
        initial_pages_count = len(page.context.pages)
        
        page.press('input[name="p"]', 'Enter')
        
        # Wait for the new windows or New tab or existing tab to load the search results
        # We wait a short time to see if a new page is created (e.g. 3 seconds)
        page.wait_for_timeout(3000)
        
        # Switch to the new window or tab or stay in the existing tab
        current_pages = page.context.pages
        if len(current_pages) > initial_pages_count:
            # New page opened, switch to the last one
            target_page = current_pages[-1]
            print("Switched to new window/tab.")
        else:
            # Stay on same page
            target_page = page
            print("Staying in existing tab.")
            
        # Once the results are loaded
        target_page.wait_for_load_state("domcontentloaded")

        # 6. take the screenshot and save
        # Format: filenameDDMMYYYY_Time
        now = datetime.now()
        timestamp = now.strftime("%d%m%Y_%H%M%S")
        screenshot_filename = f"yahoo_search_results_{timestamp}.png"
        
        target_page.screenshot(path=screenshot_filename)
        
        # Get absolute path and print it
        absolute_path = os.path.abspath(screenshot_filename)
        print(f"Screenshot saved at: {absolute_path}")

        # 7. close the browser
        browser.close()

if __name__ == "__main__":
    run()
