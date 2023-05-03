import core
import logging

import time

LOG_TO_FILE = False
LOG_FILE_NAME = "bot.log"

# Delete the log file if it exists
if LOG_TO_FILE and os.path.isfile(path=LOG_FILE_NAME):
    os.remove(path=LOG_FILE_NAME)

# YTDL setup
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

# Set up logging
if LOG_TO_FILE:
    log_handler = logging.basicConfig(format='%(asctime)s %(message)s', filename=LOG_FILE_NAME, encoding='utf-8', level=logging.INFO)
else:
    log_handler = logging.basicConfig(format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO)

def do_song_loop():
    a = core.ApiComms()
    p = core.SongPlayer()

    logging.info(msg="Starting song loop")
    while True:
        # Get the next song
        song_dict = a.get_next_song()

        # Did we get a song?
        if not song_dict:
            logging.error(msg="Failed to get next song, sleeping for 10 seconds")
            time.sleep(a.get_api_request_timeout())
            continue

        # Exract the song URL, and the song ID
        song_url = song_dict['Song_Url']
        song_id = song_dict['Song_ID']
        song_request_id = song_dict['Request_ID']
       
        # Play the song
        logging.info(msg="Playing song: " + song_url)
        p.play_song(song_url)

        # Mark the song as played in the API
        logging.info(msg="Marking song as played")
        a.mark_song_as_played(song_request_id)

if __name__ == '__main__':
    do_song_loop()