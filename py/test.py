# Stanrdard library imports
import os
import logging
import time

os.add_dll_directory(r"C:\\Program Files\\VideoLAN\\VLC")

# Third party imports
import yt_dlp
import vlc

# Our imports
import core

# Options for the ytdl object
ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to all IPv4 addresses
}

# Create the YTDL object
ytdl = yt_dlp.YoutubeDL(ytdl_opts)

# Logging options
LOG_TO_FILE = False
LOG_FILE_NAME = "bot.log"

# Delete the log file if it exists
if os.path.isfile(path=LOG_FILE_NAME):
    os.remove(path=LOG_FILE_NAME)

# Set up logging
if LOG_TO_FILE:
    log_handler = logging.basicConfig(format='%(asctime)s %(message)s', filename=LOG_FILE_NAME, encoding='utf-8', level=logging.INFO)
else:
    log_handler = logging.basicConfig(format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO)

# Test here for now
if __name__ == '__main__':
    logging.info("Starting test")
    logging.info("Creating objects")
    SP = core.SongPlayer()
    SP.play_song("https://www.youtube.com/watch?v=mOanPc8Vhmw")
    logging.info("Test complete")

