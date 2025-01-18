import os
import shutil
from concurrent.futures import ThreadPoolExecutor

# Define month abbreviations dictionary
month_abbr = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

# Function to create directories for each month in a given year
def create_month_directory(year, month):
    month_abbr_value = month_abbr[month]
    month_folder = os.path.join(year, month_abbr_value)
    os.makedirs(month_folder, exist_ok=True)

# Function to organize files into correct year and month folders
def organize_file(filename, source_dir, target_dir):
    if filename.endswith('.jpg') or filename.endswith('.mp4'):
        if filename.startswith('IMG_'):
            file_parts = filename.split('_')[-1]
        else:
            file_parts = filename.split('.')[0]  # Remove extension
        year = file_parts[:4]
        month = int(file_parts[4:6])
        day = int(file_parts[6:8])
        target_month_dir = os.path.join(target_dir, year, month_abbr[month])
        if not os.path.exists(target_month_dir):
            create_month_directory(os.path.join(target_dir, year), month)
        shutil.copy(os.path.join(source_dir, filename), target_month_dir)

# Function to organize files in parallel using ThreadPoolExecutor
def organize_files_parallel(source_dir, target_dir, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        filenames = os.listdir(source_dir)
        executor.map(lambda filename: organize_file(filename, source_dir, target_dir), filenames)

# Source and target directories
source_directory = '/wd-black/photos_s23_2025'  # Change this to your source directory
target_directory = '/media/siva/Seagate_4TB/staging_photos'  # Change this to your target directory
num_threads = 50  # Change this to the desired number of threads

# Organize files in parallel with specified number of threads
organize_files_parallel(source_directory, target_directory, num_threads)
