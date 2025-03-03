import os

# Define paths and replacements
project_path = "/home/mutabazi/Documents/Projects/banking_system"
rename_map = {
    "logger": "logger",
    "keylogger": "keylogger",
    "transactions": "transactions",
    "accounts": "accounts",
    "analytics": "analytics",
    "core": "core",
}

def revert_references_in_file(file_path, rename_map):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated = False
        for current, original in rename_map.items():
            if current in content:
                content = content.replace(current, original)
                updated = True

        if updated:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Reverted references in: {file_path}")
    except (UnicodeDecodeError, FileNotFoundError):
        print(f"Skipped non-text or problematic file: {file_path}")

# Walk through the project and revert references
for root, _, files in os.walk(project_path):
    for file in files:
        if file.endswith(('.py', '.html', '.txt', '.json')):
            file_path = os.path.join(root, file)
            revert_references_in_file(file_path, rename_map)

print("Reverting references completed.")

