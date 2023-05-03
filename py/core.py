import logging
import os
import subprocess
import sys
import time
import json

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

# Try to import libraries
try:
    logging.info(msg="Importing libraries...")
    # TODO: Add other needed libraries here
    import yt_dlp
    import vlc
    import requests

except ImportError:
    # Log which libraries failed to import
    logging.error(msg="Failed to import libraries: " + str(sys.exc_info()[1]))

    # Install requirements from requirements.txt, restart the script and exit
    logging.error(msg="Failed to import libraries, installing requirements...")
    subprocess.call(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])

    # Restart the script
    logging.info(msg="Restarting script...")
    subprocess.call(['python', 'main.py'])
    exit()

class SongPlayer:
    # SongPlayer class variables
    def __init__(self):
        self.ytdl = yt_dlp.YoutubeDL(ytdl_opts)

    def get_video(self, url):
        logging.info(msg="Getting video: " + url)
        info = self.ytdl.extract_info(url, download=False)

        formats = info['formats']

        # Get the best audio format
        for f in formats:
            if f.get('acodec') == 'opus':
                best_audio_format = f
                break
        
        # If we didn't find an opus format, just use the first one
        if not best_audio_format:
            best_audio_format = formats[0]

        # Return the url
        if not best_audio_format['url']:
            logging.error(msg="Failed to get video url")
            return None
        else:
            logging.info(msg="Got video url")
        return best_audio_format['url']

    def play_song(self, url):
        # Get the source url
        logging.info(msg="Starting play_song")
        source_url = self.get_video(url)

        # Create the vlc instance
        logging.info(msg="Setting up vlc")
        vlc_instance = vlc.Instance(["prefer-insecure"])
        vlc_player = vlc_instance.media_player_new()
        media = vlc_instance.media_new(source_url)
        vlc_player.set_media(media)

        # Play the media, wait until it's done playing
        logging.info(msg="Playing song")
        vlc_player.play()
        time.sleep(1.5)
        while vlc_player.is_playing():
            time.sleep(1)

        logging.info(msg="Song finished playing")

        # Stop the player
        vlc_player.stop()
        logging.info(msg="Stopped player")

    def test(self):
        self.play_song("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

class ApiComms():
    def __init__(self):
        # Setup API comms
        logging.info(msg="Setting up API comms")
        self.api_url = "https://richard.keithsoft.com/hkmb/api.php"
        self.api_request_timeout = 10

        # Test the API connection with request -1
        logging.info(msg="Testing API connection")
        self.do_api_request(-1, {})
        logging.info(msg="API connection successful")

    def get_api_request_timeout(self):
        return self.api_request_timeout
        
    def do_api_request(self, request_type, params):
        logging.info(msg="Doing API request: " + str(request_type))

        # Get the request string
        request_str = self.api_url + "?request=" + str(request_type)

        # Add the params to the request string
        for param in params.keys():
            # Each param is a name and type in a dict
            request_str += "&" + param + "=" + str(params[param])

        # Make the request
        try:
            logging.info(msg="Making API request")
            response = requests.get(url=request_str)
            
            # If this was an API connection test request, if the respose is "OK" then the connection is good
            if request_type == -1:
                if response.text == "OK":
                    logging.info(msg="API connection test successful")
                    return True
                else:
                    logging.error(msg="API connection test failed")
                    return False

            # Check the response code
            if response.status_code != 200:
                logging.error(msg="API request failed: " + str(response.status_code))
                return None
            
            # Return the JSON we got as a dict
            logging.info(msg="API request successful")
            return json.loads(response.text)

        except Exception as e:
            # Log the error
            logging.error(msg="API request failed: " + str(e))
            return None

    def get_next_song(self):
        logging.info(msg="Getting next song")
        # Make request to API
        response = self.do_api_request(request_type=0, params={})

        # Check the response
        if not response:
            logging.error(msg="Failed to get next song")
            return None

        # Response is a list of dicts, ordered by votes, and each dict has a "Song_ID", which is what we want
        next_song_id = response[0]["Song_ID"]
        request_id = response[0]["Request_ID"]

        # Ask the API for details about the song
        response = self.do_api_request(request_type=4, params={"song_id": next_song_id})

        # Check the response
        if not response:
            logging.error(msg="Failed to get song details")
            return None

        # Add the request ID to the dict, and return it
        song_dict = response
        song_dict["Request_ID"] = request_id
        return song_dict

    def get_song_id_from_request_id(self, request_id):
        logging.info(msg="Getting song ID from request ID: " + str(request_id))
        

    def mark_song_as_played(self, request_id):
        logging.info(msg="Marking song as played: " + str(request_id))
        # Make request to API
        response = self.do_api_request(request_type=1, params={"request_id": request_id})
        
        # Check the response
        if not response:
            logging.error(msg="Failed to mark song as played")
            return False

        # Response is a dict with a "Result" key
        if response == "{\"OK\":true}":
            logging.info(msg="Marked song as played")
            return True
        else:
            logging.error(msg="Failed to mark song as played")
            return False
        