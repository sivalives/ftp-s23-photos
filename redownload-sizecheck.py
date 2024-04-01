import os
from ftplib import FTP

# FTP server credentials
FTP_HOST = '10.0.0.50'
FTP_PORT = 2121  # Change this to your FTP server's port number
FTP_USER = 'android'
FTP_PASS = 'android'

# Remote folder in your phone
REMOTE_FOLDER = '/Camera'

# Local folder to download files
LOCAL_FOLDER = '/Volumes/HDD/photos/s23-pics'

def download_missing_or_mismatched_files():
    # Get dictionaries of local and remote files with their sizes
    local_files = get_files_with_sizes(LOCAL_FOLDER)
    remote_files = get_remote_files_with_sizes()
    
    # Download missing or mismatched files
    for file, remote_size in remote_files.items():
        local_size = local_files.get(file)
        if local_size is None or local_size != remote_size:
            download_file(file)

def get_files_with_sizes(folder):
    files_with_sizes = {}
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            files_with_sizes[file] = file_size
    return files_with_sizes

def get_remote_files_with_sizes():
    remote_files_with_sizes = {}
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(REMOTE_FOLDER)
        files = ftp.nlst()
        for file in files:
            file_size = ftp.size(file)
            remote_files_with_sizes[file] = file_size
    return remote_files_with_sizes

def download_file(file):
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(REMOTE_FOLDER)
        
        local_file_path = os.path.join(LOCAL_FOLDER, file)
        with open(local_file_path, 'wb') as f:
            ftp.retrbinary(f"RETR {file}", f.write)
        print(f"Downloaded: {file}")

if __name__ == "__main__":
    download_missing_or_mismatched_files()
