import os
import shutil

rezultati = [
    "C:/dev/Enterprise/NenadTips/scraper/bookmakers/Soccer/rezultati",
    "C:/dev/Enterprise/NenadTips/scraper/bookmakers/Mozzart/rezultati"
]

def delete_files_in_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory '{directory_path}' does not exist.")
        return

    # Check if the path is a directory
    if not os.path.isdir(directory_path):
        print(f"'{directory_path}' is not a directory.")
        return

    # Iterate over all files in the directory and delete them
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Delete the file or symbolic link
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Delete the subdirectory and its contents
                print(f"Deleted directory: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    for directory_path in rezultati:
        delete_files_in_directory(directory_path)