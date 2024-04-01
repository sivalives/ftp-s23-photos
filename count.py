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

def download_missing_files():
    # Connect to FTP server
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(REMOTE_FOLDER)
        
        # Get list of files in remote folder
        remote_files = ftp.nlst()
    
    # Get list of files in local folder
    local_files = os.listdir(LOCAL_FOLDER)
    
    # Convert to sets for faster comparison
    remote_files_set = set(remote_files)
    local_files_set = set(local_files)
    
    # Find missing files (present in remote but not in local)
    missing_files = remote_files_set - local_files_set
    
    # Download missing files
    with FTP() as ftp:
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(REMOTE_FOLDER)
        
        for file in missing_files:
            local_file_path = os.path.join(LOCAL_FOLDER, file)
            with open(local_file_path, 'wb') as f:
                ftp.retrbinary(f"RETR {file}", f.write)
            print(f"Downloaded: {file}")

if __name__ == "__main__":
    download_missing_files()
