import os
import re

# Define paths
project_root = "/home/mutabazi/Documents/Projects/banking_system"

# Define the replacements
replacements = {
    "logger": "logger"
}

def update_references(file_path, replacements):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated_content = content
        for old, new in replacements.items():
            updated_content = re.sub(rf'\b{old}\b', new, updated_content)

        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Updated references in: {file_path}")
    except (UnicodeDecodeError, FileNotFoundError, PermissionError):
        print(f"Failed to update {file_path}: Non-UTF-8 or inaccessible file.")

def process_directory(root_path, replacements, excluded_dirs):
    for root, dirs, files in os.walk(root_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in excluded_dirs]

        for file_name in files:
            # Skip hidden files and unsupported extensions
            if file_name.startswith('._') or not file_name.endswith(('.py', '.html', '.txt', '.json')):
                continue

            file_path = os.path.join(root, file_name)
            update_references(file_path, replacements)

# Run the script
print("Starting reference updates...")
process_directory(project_root, replacements, excluded_dirs=[])
print("Reference updates completed.")

