import logging
import os
import subprocess
import sys

class core:
    # Core class variables
    LOG_TO_FILE = False
    LOG_FILE_NAME = "bot.log"

    def __init__(self):
        # Delete the log file if it exists
        if os.path.isfile(path=core.LOG_FILE_NAME):
            os.remove(path=core.LOG_FILE_NAME)

        # Set up logging
        if core.LOG_TO_FILE:
            self.log_handler = logging.basicConfig(format='%(asctime)s %(message)s', filename=core.LOG_FILE_NAME, encoding='utf-8', level=logging.INFO)
        else:
            self.log_handler = logging.basicConfig(format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO)

        # Try to import libraries
        try:
            logging.info(msg="Importing libraries...")
            # TODO: Add other needed libraries here
            import yt_dlp
            import vlc
            
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
        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
            "options": "-vn",
        }

        # Create the YTDL object
        self.ytdl = yt_dlp.YoutubeDL(ytdl_opts)

    def get_video(self, url):
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

        # Get the source url
        source_url = best_audio_format['url']

        print(source_url)
        print(type(source_url))

        # Return the source url
        return source_url

    def play_song(self, url):
        # Get the source url
        source_url = self.get_video(url)

        # Play the video
        inst = vlc.Instance()
        player = inst.media_player_new()
        media = inst.media_new(source_url)
        player.set_media(media)
        player.play()

c = core()
c.play_song("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
