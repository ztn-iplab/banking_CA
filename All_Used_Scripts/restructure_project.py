import os
import shutil

# Define current and new project paths
current_project_path = "/home/mutabazi/Documents/Users/festusedward-n/Backup for the project/26th November 2024 Backup/banking_system"
new_project_path = "/home/mutabazi/Documents/Projects/banking_system"

# Define folder renaming mapping
rename_mapping = {
    "logger": "activity_logger",
    "keylogger": "keylogger",
    "transactions": "transactions",
    "accounts": "accounts",
    "analytics": "analytics",
    "core": "core"
}

# Ensure the new project path exists
os.makedirs(new_project_path, exist_ok=True)

# Step 1: Copy and Rename Files/Folders
print("Copying and renaming folders...")
for item in os.listdir(current_project_path):
    current_item_path = os.path.join(current_project_path, item)
    new_item_name = rename_mapping.get(item, item)  # Get new name if defined, else keep the same
    new_item_path = os.path.join(new_project_path, new_item_name)

    if os.path.isdir(current_item_path):
        if item == '.git':
            print(f"Skipping .git folder: {item}")
            continue
        print(f"Copying folder: {item} -> {new_item_name}")
        shutil.copytree(current_item_path, new_item_path, dirs_exist_ok=True)
    else:
        print(f"Copying file: {item}")
        shutil.copy2(current_item_path, new_item_path)

# Step 2: Update References in Code
print("Updating references in code files...")
def update_references_in_file(file_path, replacements):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        for old, new in replacements.items():
            content = content.replace(old, new)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except (UnicodeDecodeError, FileNotFoundError):
        print(f"Skipping non-text or problematic file: {file_path}")

# Prepare replacements for folder name changes
replacements = {f"'{old}'": f"'{new}'" for old, new in rename_mapping.items()}

for root, dirs, files in os.walk(new_project_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        # Skip hidden or binary files
        if file_name.startswith('.') or not file_name.endswith(('.py', '.html', '.txt', '.json', '.md')):
            continue
        print(f"Updating file: {file_path}")
        update_references_in_file(file_path, replacements)

# Step 3: Update Settings and Virtual Environment
print("Updating settings and virtual environment...")
settings_file = os.path.join(new_project_path, "banking_system/settings.py")
venv_path = os.path.join(new_project_path, "venv")

if os.path.exists(settings_file):
    print(f"Updating settings file: {settings_file}")
    update_references_in_file(settings_file, {
        current_project_path: new_project_path
    })

# Step 4: Inform User and Test
print("Project restructuring completed.")
print("\nNext steps:")
print("1. Navigate to the new project directory:")
print(f"   cd {new_project_path}")
print("2. Activate the virtual environment (if applicable):")
print(f"   source {venv_path}/bin/activate")
print("3. Run the server to verify everything works:")
print("   python3 manage.py runserver")

