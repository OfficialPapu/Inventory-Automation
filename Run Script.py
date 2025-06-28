import subprocess
import os

# Define the absolute paths to your scripts
script_dir = r"D:\Tool"  # Change this to the correct directory
venv_python = rf"{script_dir}\.venv\Scripts\python.exe" 
scripts = [
    os.path.join(script_dir, "Download Inventory.py"),
    os.path.join(script_dir, "Generate Excel Sheet.py"),
    os.path.join(script_dir, "Update Stock.py")
]

for script in scripts:
    try:
        print(f"Running: {script}")
        result = subprocess.run([venv_python, script], check=True)
    except subprocess.CalledProcessError:
        print(f"Error executing {script}. Stopping further execution.")
        break
