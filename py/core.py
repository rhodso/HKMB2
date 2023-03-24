import logging
import os
import subprocess
import sys

os.add_dll_directory(r"C:\\Program Files\\VideoLAN\\VLC")


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

        # if(self.vlc_test()):
        #     logging.info(msg="VLC test passed")
        # else:
        #     logging.info(msg="VLC test failed")
        #     exit()

    def vlc_test(self):
        try:
            vlc_instance = vlc.Instance()
        except:
            logging.error(msg="Failed to create vlc instance: " + str(sys.exc_info()[1]))
            return False

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

        # print(source_url)
        # print(type(source_url))

        # Return the source url
        return source_url

    def play_song(self, url):
        # Get the source url
        source_url = self.get_video(url)

        # Create the vlc instance
        vlc_instance = vlc.Instance()
        vlc_player = vlc_instance.media_player_new()
        
        # Create the media
        media = vlc_instance.media_new(source_url)

        # Set the media
        vlc_player.set_media(media)

        # Play the media
        vlc_player.play()

def test():
    c = core()
    c.play_song("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if __name__ == '__main__':
    test()