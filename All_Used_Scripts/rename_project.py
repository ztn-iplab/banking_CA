import os

def rename_project(directory, old_name, new_name):
    """Recursively renames occurrences of old_name with new_name in the specified directory."""
    for root, dirs, files in os.walk(directory):
        # Rename directories
        for dir_name in dirs:
            if old_name in dir_name:
                old_dir_path = os.path.join(root, dir_name)
                new_dir_path = os.path.join(root, dir_name.replace(old_name, new_name))
                try:
                    os.rename(old_dir_path, new_dir_path)
                    print(f"Renamed directory: {old_dir_path} -> {new_dir_path}")
                except OSError as e:
                    print(f"Failed to rename directory: {old_dir_path} ({e})")

        # Rename files and update content
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Rename files
                if old_name in file_name:
                    new_file_name = file_name.replace(old_name, new_name)
                    new_file_path = os.path.join(root, new_file_name)
                    os.rename(file_path, new_file_path)
                    file_path = new_file_path
                    print(f"Renamed file: {file_name} -> {new_file_name}")

                # Update file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                updated_content = content.replace(old_name, new_name)

                if updated_content != content:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    print(f"Updated content in: {file_path}")

            except (UnicodeDecodeError, PermissionError) as e:
                print(f"Skipped: {file_path} ({e})")

if __name__ == "__main__":
    project_directory = "/home/mutabazi/Documents/Users/festusedward-n/Backup for the project/26th November 2024 Backup/banking_system"
    old_project_name = "banking_system"
    new_project_name = "banking_system"
    rename_project(project_directory, old_project_name, new_project_name)
    print("Project renaming complete.")

