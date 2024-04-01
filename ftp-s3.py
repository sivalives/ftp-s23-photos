import os
from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor
from progress.bar import Bar  # Importing Bar from progress.bar

# FTP server credentials
FTP_HOST = '10.0.0.50'
FTP_PORT = 2121  # Change this to your FTP server's port number
FTP_USER = 'android'
FTP_PASS = 'android'

# Remote folder in your phone
#REMOTE_FOLDER = '/DCIM/Camera'
REMOTE_FOLDER = '/Camera'

# Local folder to download files
LOCAL_FOLDER = '/Volumes/HDD/photos/s23-pics'

# File to keep track of successfully copied files
LOG_FILE = 'copied_files.log'

# File to store failed downloads
FAILED_LOG_FILE = 'failed_downloads.log'

# Number of threads for parallel downloading
NUM_THREADS = 15  # Adjust this value according to your preference

def remove_copied_files():
    # Get list of files in local folder
    local_files = os.listdir(LOCAL_FOLDER)
    
    # Read log file to get already copied files
    with open(LOG_FILE, 'r') as f:
        copied_files = set(f.read().splitlines())

    # Iterate over local files
    for file in local_files:
        file_path = os.path.join(LOCAL_FOLDER, file)
        # Check if file size is greater than 0 and if it's in copied_files
        if os.path.getsize(file_path) > 0 and file in copied_files:
            copied_files.remove(file)
            print(f"Removed from copied_files list: {file}")
    return len(local_files)

def download_file(filename, copied_files, bar):
    local_file_path = os.path.join(LOCAL_FOLDER, filename)
    
    # Connect to FTP server
    with FTP() as ftp:
        try:
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            ftp.cwd(REMOTE_FOLDER)
            
            # Check if file is already copied
            if filename in copied_files:
                bar.next()  # Increment progress bar
                return
        
            # Download the file
            with open(local_file_path, 'wb') as f:
                ftp.retrbinary(f"RETR {filename}", f.write)
            print(f"Downloaded: {filename}")
            
            # Update copied files in log file
            with open(LOG_FILE, 'a') as f:
                f.write(f"{filename}\n")
            
            # Update copied_files set
            copied_files.add(filename)
            
            # Increment progress bar
            bar.next()
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            # Log failed download
            with open(FAILED_LOG_FILE, 'a') as f:
                f.write(f"{filename}\n")

def download_files():
    # Connect to FTP server
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(REMOTE_FOLDER)
        
        # Get list of files in remote folder
        files = ftp.nlst()

    # Check if log file exists, create if not
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()

    # Check if failed downloads log file exists, create if not
    if not os.path.exists(FAILED_LOG_FILE):
        open(FAILED_LOG_FILE, 'w').close()

    # Read log file to get already copied files
    with open(LOG_FILE, 'r') as f:
        copied_files = set(f.read().splitlines())

    files_exist = remove_copied_files()

    total_files = len(files) - files_exist
    print(f"Files to be copied {files_exist}")


    # Use ThreadPoolExecutor to download files in parallel with specified number of threads
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        with Bar('Downloading', max=total_files) as bar:  # Initialize progress bar
            for file in files:
                executor.submit(download_file, file, copied_files, bar)

if __name__ == "__main__":
    download_files()
