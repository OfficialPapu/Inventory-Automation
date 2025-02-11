from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import glob

# Constants
URL = "https://www.dreamskinnepal.com/Account/Authentication/Admin Login Interface.php"
USERNAME = "email"  # Replace with your actual admin username
PASSWORD = "********"  # Replace with your actual admin password

# Detect the latest downloaded Excel file dynamically
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
file_pattern = os.path.join(downloads_folder, "Stock Quantity*.xlsx")
files = glob.glob(file_pattern)

if not files:
    print("❌ No inventory update file found in Downloads folder.")
    exit()

# Get the most recent file
FILE_PATH = max(files, key=os.path.getctime)
print(f"📂 Using file: {FILE_PATH}")

# Path to Brave browser (Adjust based on your OS)
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"  # Windows

# Setup Brave browser options
options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_experimental_option("detach", True)  # Keep the browser open after script execution

# Launch Brave with Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the admin login page
driver.get("https://www.dreamskinnepal.com/Admin/")  # Admin login URL
time.sleep(2)  # Wait for the page to load
print("✅ Admin login page opened successfully.")

# Navigate to the authentication page
driver.get(URL)  # Login interface URL
time.sleep(2)  # Allow time for the page to load

# Find the username and password fields
try:
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))  # Adjust if needed
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Pass"))  # Adjust if needed
    )
except Exception as e:
    print(f"❌ Failed to locate login fields: {str(e)}")
    driver.quit()
    exit()

# Send credentials to the login fields
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)

# Find and click the "Login" button
try:
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
except Exception as e:
    print(f"❌ Failed to click login button: {str(e)}")
    driver.quit()
    exit()
time.sleep(3)  # Wait for login to complete

# Navigate to the "Update Stock" page
driver.get("https://www.dreamskinnepal.com/Admin/Update Quantity.php")  # Stock update URL
time.sleep(2)  # Wait for the page to load

# Find the file upload input field
try:
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "ExcelFile"))  # Adjust field name if necessary
    )
    file_input.send_keys(FILE_PATH)  # Provide the file path
    print("✅ File path provided for upload.")
except Exception as e:
    print(f"❌ Failed to locate or upload the file: {str(e)}")
    driver.quit()
    exit()
time.sleep(2)  # Wait for the file upload input to be processed

# Click the "Update Stock" button
try:
    update_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Update"))  # Adjust if needed
    )
    update_button.click()
except Exception as e:
    print(f"❌ Failed to click 'Update Stock' button: {str(e)}")
    driver.quit()
    exit()
time.sleep(5)  # Wait for the update process to complete

# Additional wait time to ensure the update is completed before moving on
time.sleep(10)

# After completing the process, delete the Excel file
try:
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)  # Remove the file after use
        print(f"✅ File {FILE_PATH} deleted successfully.")
    else:
        print(f"❌ File {FILE_PATH} does not exist.")
except Exception as e:
    print(f"❌ Failed to delete the file: {str(e)}")

# Close the browser
driver.quit()

print("✅ Stock updated successfully and browser closed.")
