import os
from ftplib import FTP
from concurrent.futures import ThreadPoolExecutor

# FTP server credentials
FTP_HOST = '10.0.0.50'
FTP_PORT = 2121  # Change this to your FTP server's port number
FTP_USER = 'android'
FTP_PASS = 'android'

# Remote folder in your phone
REMOTE_FOLDER = '/Camera'

def delete_file(ftp, file):
    try:
        ftp.delete(file)
        print(f"Deleted: {file}")
    except Exception as e:
        print(f"Failed to delete {file}: {e}")

def delete_all_remote_files():
    with FTP() as ftp:
        # Connect to FTP server
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(REMOTE_FOLDER)

        # Get list of files in remote folder
        files = ftp.nlst()

        # Delete files concurrently
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(delete_file, ftp, file) for file in files]
            for future in futures:
                future.result()

if __name__ == "__main__":
    delete_all_remote_files()
