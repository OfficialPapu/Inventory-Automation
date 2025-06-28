import pandas as pd
import os
import time
import glob

# Define the user's downloads folder dynamically
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

# Find the latest Excel file matching "report_inventory_position.xlsx"
file_pattern = os.path.join(downloads_folder, "report_inventory_position*.xlsx")
files = glob.glob(file_pattern)
if not files:
    print("❌ No inventory report found in Downloads folder.")
    exit()

# Get the most recently downloaded inventory report
file_path = max(files, key=os.path.getctime)
print(f"📂 Using file: {file_path}")

time.sleep(2)  # Allow time for the file to be fully available

try:
    # Load the Excel data and skip unnecessary header rows
    df = pd.read_excel(file_path, skiprows=7)
    print("✅ Excel file loaded successfully!")
except Exception as e:
    print("❌ Failed to load Excel file:", str(e))
    exit()

# Rename columns for consistency
df.columns = ["Code/Goods", "Category", "Qty", "UOM", "Rate", "Amount"]

# Extract the last 6 characters from 'Code/Goods' and clean data
df["ID"] = df["Code/Goods"].astype(str).str[-6:].str.replace(")", "", regex=False)

# Select relevant columns and rename them
df = df[["ID", "Code/Goods", "Qty"]]
df.columns = ["ID", "Product Title", "Quantity"]
df = df.dropna()  # Remove rows with missing values

# Save processed data
new_file_path = os.path.join(downloads_folder, "Stock Quantity.xlsx")
try:
    df.to_excel(new_file_path, index=False)
    print(f"✅ Processed file saved as: {new_file_path}")
except Exception as e:
    print("❌ Failed to save the new file:", str(e))

time.sleep(1)

# Safely delete the original file
try:
    os.remove(file_path)
    print(f"✅ Original file {file_path} deleted successfully.")
except Exception as e:
    print("❌ Failed to delete the original file:", str(e))

print("✅ Process Completed! Generated Excel file.")
