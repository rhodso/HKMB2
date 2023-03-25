# Stanrdard library imports
import os
import logging

# Third party imports
import yt_dlp
import vlc

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

# Get the source url from the video url
def get_video(url):
    info = ytdl.extract_info(url, download=False)

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

    # Return the source url
    return source_url

# Play the song
def play_song(url):
    # Get the source url
    source_url = get_video(url)

    # Create the vlc instance
    vlc_instance = vlc.Instance()
    vlc_player = vlc_instance.media_player_new()
    
    # Create the media
    media = vlc_instance.media_new(source_url)

    # Set the media
    vlc_player.set_media(media)

    # Play the media
    vlc_player.play()

# Test here for now
if __name__ == '__main__':
    play_song("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
