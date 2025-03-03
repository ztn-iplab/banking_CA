import subprocess

# Define the backup directory
backup_dir = "/home/mutabazi/Documents/Users/festusedward-n/Backup for the project/26th November 2024 Backup/banking_system"

# Find and replace occurrences of 'banking_system' with 'banking_system' in .py and .md files
command = f'find "{backup_dir}" -type f \\( -name "*.py" -o -name "*.md" \\) -exec sed -i "s/banking_system/banking_system/g" {{}} +'

try:
    # Execute the shell command
    subprocess.run(command, shell=True, check=True)
    print("Command executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")

