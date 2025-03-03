import os

# Define paths and replacement
project_path = "/home/mutabazi/Documents/Projects/banking_system"
old_name = "accounts"
new_name = "accounts"

# File extensions to update
extensions = (".py", ".html", ".json", ".txt", ".md")

def update_references_in_file(file_path, old, new):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if old in content:
            content = content.replace(old, new)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated references in: {file_path}")
    except (UnicodeDecodeError, FileNotFoundError):
        print(f"Skipped non-text or problematic file: {file_path}")

# Walk through the project and update references
for root, dirs, files in os.walk(project_path):
    for file_name in files:
        if file_name.endswith(extensions):
            file_path = os.path.join(root, file_name)
            update_references_in_file(file_path, old_name, new_name)

print("Reference update completed.")

