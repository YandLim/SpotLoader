from dotenv import load_dotenv
from requests import post, get
import requests
import base64
import json
import re
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


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


def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}


def get_album_song(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_playlist_song(token, url):
    url = url
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    next_items = json_result["next"]
    return json_result, next_items


def get_songs(token, song_id):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_thumbnail(urls, save_name):
    length = 0
    counter = 1
    for url, raw_name in zip(urls, save_name):
        raw_name = raw_name.split("-")[1]
        name = os.path.join(DOWNLOAD_IMAGES, f"{raw_name}.jpg")
        response = requests.get(url)

        if os.path.exists(name):  # Cek apakah file sudah ada
            name = name.split(".")[0] + f"{counter}" + ".jpg" # Tambah angka sebelum ekstensi
            counter += 1

        if response.status_code == 200:
            with open(name, "wb") as f:
                f.write(response.content)
                length += 1
        else:
            print(f"❌ Error couldn't find {name} thumbnail image")
            

def sanitize_filename(filename):
    all_name = []
    for name in filename:
        sanitized = re.sub(r'[<>:"/\\|?*]', '', name)  # Hapus karakter ilegal
        all_name.append(sanitized.strip())
    return all_name


found_song = []
thumbnail_url = []
token = get_token()
DOWNLOAD_IMAGES = "Images"

user_link = input("Please enter the link to a playlist or song\n=> ")

if user_link.split("/")[3] == "album":
    playlist_id = user_link.split("/")[4]
    playlist_songs = get_album_song(token, playlist_id)
    items = playlist_songs["tracks"]["items"]

    for idx, song in enumerate(items):
        full_title = f"{song["artists"][0]["name"]} - {song['name']}"
        print(f"{idx + 1}: {full_title}")

        thumbnail_url.append(playlist_songs["images"][0]["url"])
        found_song.append(full_title)

elif user_link.split("/")[3] == "playlist":
    playlist_id = user_link.split("/")[4]
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    playlist_songs, next_playlist = get_playlist_song(token, playlist_url)
    items = playlist_songs["items"]

    if next_playlist:
        while next_playlist:
            playlist_songs, next_playlist = get_playlist_song(token, next_playlist)
            items.extend(playlist_songs["items"])

            for idx, song in enumerate(items):
                full_title = f"{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}"
                print(f"{idx + 1}: {full_title}")

                thumbnail_url.append(song["track"]["album"]["images"][0]["url"])
                found_song.append(full_title)
    
    else:
        for idx, song in enumerate(items):
            full_title = f"{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}"
            print(f"{idx + 1}: {full_title}")

            thumbnail_url.append(song["track"]["album"]["images"][0]["url"])
            found_song.append(full_title)



elif user_link.split("/")[3] == "track":
    song_id = user_link.split("/")[4]
    song = get_songs(token, song_id)
    full_title = f"{song["artists"][0]["name"]} - {song["name"]}"
    print("Song Name:", full_title)

    found_song.append(full_title)
    thumbnail_url.append(song["album"]["images"][0]["url"])
    
sanitize_name = sanitize_filename(found_song)
get_thumbnail(thumbnail_url, sanitize_name)
