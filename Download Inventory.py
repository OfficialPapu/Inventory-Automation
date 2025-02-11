from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Define a fixed download path (change as needed)
download_path = os.path.join(os.path.expanduser("~"), "Downloads",)

# Ensure the directory exists
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Configure ChromeOptions for default browser and download path
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Keep browser open after script execution
options.add_experimental_option("prefs", {
    "download.default_directory": download_path,  # Set download location
    "download.prompt_for_download": False,  # Disable download prompt
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True  # Enable safe browsing
})

# Launch Chrome (or default browser)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 1️⃣ Open Tigg Login Page
driver.get("https://dream.tigg.app/erp/#/")
wait = WebDriverWait(driver, 10)

# 2️⃣ Log in to Tigg
username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
password = driver.find_element(By.XPATH, "//input[@type='password']")

username.send_keys("email")  # Replace with actual credentials
password.send_keys("********")  
password.send_keys(Keys.RETURN)  

# 3️⃣ Navigate to Inventory Summary
time.sleep(1)
driver.get("https://dream.tigg.app/erp/#/reports/new/inventory-summary")

# 4️⃣ Click "Options" Button
try:
    options_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "rl-button-wrapper")))
    options_button.click()
except Exception as e:
    print("❌ Failed to click 'Options' button:", str(e))

# 6️⃣ Click "Export"
try:
    full_export_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), 'Export') and contains(@class, 'popover-buttton-item')]")
    ))
    full_export_button.click()
except Exception as e:
    print("❌ Failed to click 'Export' button:", str(e))

# 7️⃣ Click "Export Full List"
try:
    export_full_list_radio = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'report-filter-radio')]//div[contains(text(), 'Export Full List')]/following-sibling::label[@class='ant-radio-wrapper']")
    ))
    export_full_list_radio.click()
except Exception as e:
    print("❌ Failed to click 'Export Full List' radio button:", str(e))

# 8️⃣ Click "Export Report" Button
try:
    final_export_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'rl-button') and contains(@class, 'small')]//div[contains(text(), 'Export Report')]")
    ))
    actions = ActionChains(driver)
    actions.move_to_element(final_export_button).click().perform()
    
    print("✅ Downloading Inventory Report...")

except Exception as e:
    print("❌ Failed to click 'Export Report' button:", str(e))

# Wait for file to download (adjust timeout as needed)
time.sleep(5)
print(f"✅ Inventory report saved in: {download_path}")

driver.quit()
