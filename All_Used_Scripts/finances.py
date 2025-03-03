import os

# Define paths and replacement
project_path = "/home/mutabazi/Documents/Projects/banking_system"
old_reference = "transactions"
correct_reference = "transactions"

def fix_references_in_file(file_path, old_ref, new_ref):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if old_ref in content:
            content = content.replace(old_ref, new_ref)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Fixed references in: {file_path}")
    except (UnicodeDecodeError, FileNotFoundError):
        print(f"Skipped non-text or problematic file: {file_path}")

for root, _, files in os.walk(project_path):
    for file in files:
        if file.endswith(('.py', '.html', '.txt', '.json')):
            file_path = os.path.join(root, file)
            fix_references_in_file(file_path, old_reference, correct_reference)

print("Reference fixing completed.")

