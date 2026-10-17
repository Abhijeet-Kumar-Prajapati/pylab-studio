import os
import re

# Function to generate corrected file names
def generate_corrected_name(original_name):
    """
    Generate a corrected name for a file by cleaning up special characters
    and adding a 'game_' prefix for game-related files.
    """
    name_without_extension = os.path.splitext(original_name)[0]
    extension = os.path.splitext(original_name)[1]

    # Clean special characters from name
    cleaned_name = re.sub(r"[^a-zA-Z0-9_ ]", "", name_without_extension).strip()

    # Add 'game_' prefix if it's a game file (based on file extension or type logic)
    if extension.lower() in ['.exe', '.iso', '.dll', '.dat']:  # Example game-related extensions
        return f"game_{cleaned_name}{extension}"
    else:
        return f"corrected_{cleaned_name}{extension}"

# Function to rename all files in a directory (recursively)
def rename_files_recursively(root_directory):
    """
    Traverse all directories and rename files intelligently based on their names or type.
    """
    try:
        for dirpath, _, filenames in os.walk(root_directory):
            for filename in filenames:
                # Original file path
                original_path = os.path.join(dirpath, filename)

                # Generate new name
                new_name = generate_corrected_name(filename)

                # New file path
                new_path = os.path.join(dirpath, new_name)

                # Rename the file
                os.rename(original_path, new_path)
                print(f"Renamed: {original_path} -> {new_path}")
    except Exception as e:
        print(f"Error: {e}")

# Entry point: Specify the root directory (e.g., root folder of a system or game files)
if __name__ == "__main__":
    # Replace this with the starting directory you want to rename files from
    root_folder = "path/to/your/system_or_game_folder"
    rename_files_recursively(root_folder)
