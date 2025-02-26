# Importing libraries
from dotenv import load_dotenv
from requests import post, get
from yt_dlp import YoutubeDL
import urllib.request
from tqdm import tqdm
import urllib.parse
import base64
import json
import os
import re


# Load the env data
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Get the token for authentication
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Set the header for cleaner code
def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}

# Take the song from album
def get_album_song(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


# Take the song from playlist
def get_playlist_song(token, url):
    url = url
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    next_items = json_result["next"]
    return json_result, next_items


# Take the an individual song 
def get_songs(token, song_id):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


# Finding song in YouTube using name
def search_youtube(song_name):
    print("\n🔎 Looking for the song in YouTube")
    found_link = []
    for song in tqdm(song_name, desc="Searching", unit="song"):
        # Find t=in youtube using name
        search_query = urllib.parse.quote(song)
        url = f"https://www.youtube.com/results?search_query={search_query}"
        
        # Find the videos id and turn into link then store them into found_link
        try:
            html = urllib.request.urlopen(url).read().decode()
            video_ids = re.findall(r"watch\?v=(\S{11})", html)
            if video_ids:
                found_link.append(f"https://www.youtube.com/watch?v={video_ids[0]}")  # Take the first video found
        
        # Error occured
        except Exception as e:
            print(f"❌ Error when looking for the video: {e}")

    print(f"🎶Found {len(found_link)} link")
    return found_link


# Function to download song from youtube to mp3
def download_song(video_url, song_name):
    print("\n🗂️  Downloading the songs")
    succes_song = 0
    for url, name in zip(video_url, song_name):
        save_path = os.path.join(DOWNLOAD_FOLDER, name)

        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': save_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'ffmpeg_apk\bin',
        'noplaylist': True
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
            
            succes_song += 1

        except Exception as e:
            print(f"❌ Erroring found while downloading the song: {e}")

        print("")

    print("🎉Success downloading", succes_song, "Songs")


# Make the needed variabels
found_song = []
token = get_token()
DOWNLOAD_FOLDER = "Songs"

# Make the folder to store downloaded song if it's not found
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Asking for link from user
user_link = input("Please enter the link to a playlist or song\n=> ")

# If it is album
if user_link.split("/")[3] == "album":
    playlist_id = user_link.split("/")[4]
    playlist_songs = get_album_song(token, playlist_id)
    items = playlist_songs["tracks"]["items"]
    print("Songs Found:")

    # Printing one by one with number for cleaner output
    for idx, song in enumerate(items):
        full_title = f"{song["artists"][0]["name"]} - {song['name']}"
        print(f"{idx + 1}: {full_title}")

        # Store all founded songs into found_song
        found_song.append(full_title)

# If it is playlist
elif user_link.split("/")[3] == "playlist":
    playlist_id = user_link.split("/")[4]
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    playlist_songs, next_playlist = get_playlist_song(token, playlist_url)
    items = playlist_songs["items"]
    print("Songs Found:")

    # If song is more than 100, proccesing every 100
    if next_playlist:
        while next_playlist:
            playlist_songs, next_playlist = get_playlist_song(token, next_playlist)
            items.extend(playlist_songs["items"])
        for idx, song in enumerate(items):
                full_title = f"{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}"
                print(f"{idx + 1}: {full_title}")
                found_song.append(full_title)
    
    # If not 100 or less than 100 
    else:
        for idx, song in enumerate(items):
            full_title = f"{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}"
            print(f"{idx + 1}: {full_title}")
            found_song.append(full_title)

# If it is individual song
elif user_link.split("/")[3] == "track":
    song_id = user_link.split("/")[4]
    song = get_songs(token, song_id)
    full_title = f"{song["artists"][0]["name"]} - {song["name"]}"
    print("Song Name:", full_title)
    found_song.append(full_title)

# Collecting youtube's links for all the songs
youtube_links = search_youtube(found_song)

# Downloading one by one song from youtube to mp3 format
download_song(youtube_links, found_song)
 