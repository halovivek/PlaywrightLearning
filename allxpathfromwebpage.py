from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import openpyxl

# Initialize Excel workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "XPath Mapping"
ws.append(["Element Name", "XPath", "Frame Info", "Page URL"])

# Function to generate relative XPath
def get_xpath(element):
    tag = element.tag_name
    attrib_id = element.get_attribute("id")
    attrib_name = element.get_attribute("name")
    attrib_class = element.get_attribute("class")
    text = element.text.strip()

    if attrib_id:
        return f"//{tag}[@id='{attrib_id}']"
    elif attrib_name:
        return f"//{tag}[@name='{attrib_name}']"
    elif attrib_class:
        return f"//{tag}[@class='{attrib_class}']"
    elif text and len(text) < 30:
        return f"//{tag}[text()='{text}']"
    else:
        return f"//{tag}"

# Function to process a single page (no crawling)
def process_page(driver, url, frame_info="Main Document"):
    driver.get(url)
    time.sleep(2)

    # Handle frames/iframes
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for idx, frame in enumerate(frames):
        driver.switch_to.frame(frame)
        process_page(driver, driver.current_url, frame_info=f"Frame {idx}")
        driver.switch_to.default_content()

    # Collect elements
    elements = driver.find_elements(By.XPATH, "//*")
    for el in elements:
        try:
            name = el.tag_name
            xpath = get_xpath(el)
            ws.append([name, xpath, frame_info, url])
        except Exception:
            continue

# Main execution
driver = webdriver.Chrome()  # or Firefox
start_url = "https://tnreginet.gov.in/portal/"  # Replace with your site
process_page(driver, start_url)

# Save Excel
wb.save("xpath_mapping.xlsx")
driver.quit()
