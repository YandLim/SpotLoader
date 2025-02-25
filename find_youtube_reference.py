import os
import urllib.parse
import urllib.request
import re
from yt_dlp import YoutubeDL

# Membuat folder downloads jika belum ada
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Fungsi untuk mencari lagu di YouTube
def search_youtube(song_name):
    search_query = urllib.parse.quote(song_name)
    url = f"https://www.youtube.com/results?search_query={search_query}"
    
    try:
        html = urllib.request.urlopen(url).read().decode()
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"  # Ambil video pertama
        
    except Exception as e:
        print(f"❌ Error saat mencari video: {e}")
        return None

# Fungsi untuk mengunduh lagu dari YouTube sebagai MP3
def download_song(video_url, song_name):
    save_path = os.path.join(DOWNLOAD_FOLDER, f"{song_name}.mp3")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': save_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'C:\Coding\python\Spotify Saver\ffmpeg-7.1-essentials_build\bin',
        'noplaylist': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"✅ Lagu berhasil diunduh: {save_path}")
    except Exception as e:
        print(f"❌ Error saat mengunduh lagu: {e}")

# Fungsi utama untuk memasukkan judul dan memulai pengunduhan
def main():
    song_name = input("Masukkan judul lagu yang ingin diunduh: ").strip()
    
    if not song_name:
        print("❌ Judul lagu tidak boleh kosong!")
        return

    print(f"🔍 Mencari lagu: {song_name} ...")
    video_url = search_youtube(song_name)
    
    if video_url:
        print(f"🎵 Lagu ditemukan: {video_url}")
        download_song(video_url, song_name)
    else:
        print("❌ Lagu tidak ditemukan.")

if __name__ == "__main__":
    main()
