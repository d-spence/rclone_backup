# Load application settings for rclone_backup from ini file
import logging
from configparser import ConfigParser

# logging basic configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime}: {levelname}: {message}",
    datefmt="%y-%m-%d %H:%M:%S",
    style="{",
    )

try:
    # Create parser for ini file
    parser = ConfigParser()
    parser.read('settings.ini')

    # Will prompt user to upload remotely if True
    save_remotely = parser.getboolean('settings', 'save_remotely')
    use_time_in_fn = parser.getboolean('settings', 'use_time_in_fn') # append time to date

    src_dir = parser.get('dirs', 'src_dir') # which folder to backup
    local_save_dir = parser.get('dirs', 'local_save_dir') # where to save archive locally
    remote_save_dir = parser.get('dirs', 'remote_save_dir') # remote save location

    # rclone's config name for remote server
    remote_alias = parser.get('rclone', 'remote_alias') 
    filter_file = parser.get('rclone', 'filter_file') # rclone filter
except Exception as e:
    logging.error(f"Could not load settings from ini file. Exiting now...\n{e}")
    exit(1)