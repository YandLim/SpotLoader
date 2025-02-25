from dotenv import load_dotenv
from requests import post, get
import base64
import json
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


token = get_token()
user_link = input("Please enter the link to a playlist or song\n=> ")

if user_link.split("/")[3] == "album":
    playlist_id = user_link.split("/")[4]
    playlist_songs = get_album_song(token, playlist_id)
    items = playlist_songs["tracks"]["items"]

    for idx, song in enumerate(items):
        print(f"{idx + 1}: {song['name']}")

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
                print(f"{idx + 1}: {song["track"]['name']}")
    
    else:
        for idx, song in enumerate(items):
            print(f"{idx + 1}: {song["track"]['name']}")


elif user_link.split("/")[3] == "track":
    song_id = user_link.split("/")[4]
    songs = get_songs(token, song_id)
    print("Song Name: " + songs["name"])
