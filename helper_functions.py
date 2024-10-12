import os
from operator import itemgetter

def get_files_by_access_time(directory, remove_extension=False):
    # Get all files in the directory
    files = os.listdir(directory)

    # Create a list of tuples (filename, access time)
    file_times = []
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):  # Ensure it's a file, not a subdirectory
            access_time = os.path.getatime(file_path)

            # Remove extension if requested
            if remove_extension:
                file = os.path.splitext(file)[0]

            file_times.append((file, access_time))

    # Sort the list by access time (most recent first)
    file_times.sort(key=itemgetter(1), reverse=True)

    # Extract just the filenames from the sorted list
    sorted_files = [file for file, _ in file_times]

    return sorted_files
