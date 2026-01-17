import time
import pandas as pd
from playwright.sync_api import sync_playwright
import os

def scrape_tnreginet():
    with sync_playwright() as p:
        # Launch browser (headless=False to verify visually)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to portal...")
        page.goto("https://tnreginet.gov.in/portal", timeout=60000)

        # 1. Switch to English if needed
        try:
            # Fix strict mode: use .first or specific class
            lang_btns = page.locator("#fontSelection")
            if lang_btns.count() > 0:
                btn = lang_btns.first
                if btn.is_visible() and "English" in btn.inner_text():
                    print("Switching to English...")
                    btn.click()
                    page.wait_for_load_state('networkidle')
        except Exception as e:
            print(f"Language switch check skipped/failed: {e}")

        # 2. Navigate to E-Services -> Encumbrance Certificate -> View EC
        print("Navigating to 'View EC'...")
        try:
            # Try specific text match for E-Services
            eservice = page.locator("li.dropdown > a:has-text('E-Services')").first
            if not eservice.is_visible():
                 eservice = page.locator("a[title='E-Services']").first
            
            eservice.hover()
            time.sleep(1)
            
            # Hover over Encumbrance Certificate
            ec_menu = page.locator("a:has-text('Encumbrance Certificate')").first
            ec_menu.hover()
            time.sleep(1)
            
            # Click View EC
            view_ec = page.locator("a:has-text('View EC')").first
            view_ec.click()
            page.wait_for_load_state('networkidle')
            
            # Verify we are on the right page
            print(f"Current URL: {page.url}")
            # Wait for Zone dropdown explicitly
            page.wait_for_selector("#cmb_Zone", state="visible", timeout=10000)
            print("Zone dropdown found.")

        except Exception as e:
            print(f"Navigation failed: {e}")
            print("Please ensure you are on the 'View EC' page. Creating screenshot...")
            page.screenshot(path="navigation_error.png")
            return

        # Prepare for data collection
        data = []
        sl_no = 1
        output_file = "tnreginet_data.xlsx"

        # Selectors
        sel_zone = "#cmb_Zone"
        sel_dist = "#cmb_District"
        sel_sro = "#cmb_SroName"
        sel_village = "#cmb_Village"

        # Helper to get options (excluding "Select")
        def get_options(selector):
            try:
                # Wait for options to be populated (more than 1 if 'Select' is there)
                page.wait_for_function(f"document.querySelector('{selector}').options.length > 1", timeout=5000)
                options = page.locator(f"{selector} option").all()
                # Filter out empty val or "Select" text
                valid_opts = []
                for opt in options:
                    val = opt.get_attribute("value")
                    txt = opt.inner_text().strip()
                    if val and val != "0" and "Select" not in txt:
                        valid_opts.append({"value": val, "text": txt})
                return valid_opts
            except Exception as e:
                print(f"Error getting options for {selector}: {e}")
                return []

        # 3. Iterate Zone
        try:
            zones = get_options(sel_zone)
            print(f"Found {len(zones)} Zones.")
            
            for z in zones:
                zone_name = z['text']
                print(f"Processing Zone: {zone_name}")
                
                # Select Zone
                page.select_option(sel_zone, value=z['value'])
                time.sleep(1.5) # Buffer for JS
                
                districts = []
                districts = get_options(sel_dist)
                if not districts:
                    print(f"  No districts found for Zone {zone_name}")

                for d in districts:
                    dist_name = d['text']
                    print(f"  Processing District: {dist_name}")
                    
                    # Select District
                    page.select_option(sel_dist, value=d['value'])
                    time.sleep(1.5)
                    
                    sros = []
                    sros = get_options(sel_sro)
                    if not sros:
                        print(f"    No SROs found for District {dist_name}")

                    for s in sros:
                        sro_name = s['text']
                        
                        # Select SRO
                        page.select_option(sel_sro, value=s['value'])
                        time.sleep(1.5)
                        
                        villages = []
                        villages = get_options(sel_village)
                        
                        # Collect Data
                        count_new = 0
                        for v in villages:
                            village_name = v['text']
                            
                            row = {
                                "Sl.no": sl_no,
                                "Zone": zone_name,
                                "District": dist_name,
                                "Sub-Registrar Office": sro_name,
                                "Registration Village": village_name
                            }
                            data.append(row)
                            sl_no += 1
                            count_new += 1
                        
                        # Save periodically (after every SRO)
                        if count_new > 0:
                            print(f"      Saved {count_new} villages for SRO {sro_name}")
                            try:
                                df = pd.DataFrame(data)
                                df.to_excel(output_file, index=False)
                            except PermissionError:
                                print(f"      WARNING: Could not save to {output_file} (Permission Denied). Saving to backup...")
                                df.to_excel("tnreginet_data_backup.xlsx", index=False)

        except Exception as e:
            print(f"An error occurred during scraping: {e}")
        finally:
            # Final save
            if data:
                try:
                    df = pd.DataFrame(data)
                    df.to_excel(output_file, index=False)
                    print(f"Final save completed. Total rows: {len(data)}")
                    print(f"File saved to: {output_file}")
                except Exception as e:
                    print(f"Final save failed: {e}")
                    df.to_excel("tnreginet_data_final_backup.xlsx", index=False)
            
            browser.close()

if __name__ == "__main__":
    scrape_tnreginet()
