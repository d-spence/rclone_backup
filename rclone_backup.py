# rclone-backup script
# Compress a folder as a zip archive and backup to remote location using rclone
# rclone must be configured separately and should be added to env variable path

import os, zipfile, logging, subprocess
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="{asctime}: {levelname}: {message}",
    datefmt="%y-%m-%d %H:%M:%S",
    style="{",
    )

src_dir = "D:\\Projects" # which folder to backup
local_save_dir = "D:\\Backup" # where to save archive locally
remote_save_dir = "rclone\\backup" # remote save location
remote_alias = "google-drive" # rclone's config name for remote server
filter_file = "D:\\Projects\\filter-file.txt" # rclone filter

save_remotely = True # Will prompt user to upload remotely if True
use_time = True # append time to date for unique filenames
if use_time:
    # Get today's formatted date with time
    date = datetime.now().strftime("%y-%m-%d_%H%M%S")
else:
    date = datetime.now().strftime("%y-%m-%d")
    

def check_dirs():
    # Check that all directories exist; if not, an exception will be raised
    os.chdir(src_dir) # changes current working dir to src_dir
    # TODO -- Need to add checks


def create_zip(f_list, basename=True):
    # Create a compressed zip archive from a list of file paths (f_list)
    # Returns the absolute path of created zip file
    zip_fn = f"{os.path.basename(src_dir)}_{date}.zip"
    zip_full_path = os.path.join(local_save_dir, zip_fn)

    logging.info(f"Creating zip file '{zip_full_path}'")
    # Create a new compressed zip archive using LZMA method
    with zipfile.ZipFile(zip_full_path, 'w', compression=zipfile.ZIP_LZMA) as zip_file:
        for f in f_list:
            # Get relative path to file by combining src_dir and filename
            f_path = os.path.normpath(os.path.join(src_dir, f))
            if basename:
                # Use src_dir's basename as archives root folder
                f = os.path.normpath(os.path.join(os.path.basename(src_dir), f))

            logging.debug(f"Writing '{f_path}' to archive")
            zip_file.write(f_path, f) # Write file to zip archive

    return zip_full_path


def get_zip_info(zip_path):
    # Get info about a newly created zip archive
    logging.info(f"Getting info for zip file '{os.path.basename(zip_path)}'")
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        logging.info(f"File Size: {os.path.getsize(zip_path)} bytes")
        logging.info(f"# of Files: {len(zip_file.filelist)}")


def rclone_list_all():
    # Return a list of every file and folder in src directory
    # Each file path will be relative to the main archive folder (src_dir)
    logging.info(f"Getting list of files in '{src_dir}'")
    result = subprocess.check_output(f"rclone lsf -R {src_dir} --filter-from {filter_file}", 
                                    shell=True, text=True).splitlines()
    
    logging.debug(f"rclone lsf output {result}")
    return result


def rclone_save_to_remote(file_path, auto_upload=False):
    # Save archive file to remote server using rclone
    if auto_upload == False:
        answer = input(f"Would you like to upload archive to '{remote_alias}'? (Y/n) ")

    if answer == "Y" or auto_upload == True:
        logging.info(f"Uploading to '{remote_alias}' remote server...")
        os.system(f"rclone copy {file_path} {remote_alias}:{remote_save_dir}")
    else:
        logging.info(f"Skipping upload to remote server")


check_dirs()
file_list = rclone_list_all()
zip_path = create_zip(file_list)
get_zip_info(zip_path)

if save_remotely:
    rclone_save_to_remote(zip_path)

logging.info("Backup completed!")

input("Press ENTER to exit...") # Require user to press enter to exit script
