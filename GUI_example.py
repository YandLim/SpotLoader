import tkinter as tk
from tkinter import ttk, filedialog, StringVar

# Fungsi untuk memilih folder penyimpanan
def select_path():
    path = filedialog.askdirectory()
    if path:
        path_label.config(text=path)

# Inisialisasi GUI
screen = tk.Tk()
screen.title('Spotify Downloader')
screen.geometry("500x300")

# Frame utama
frame = ttk.Frame(screen, padding="20")
frame.pack(fill='both', expand=True)

# Label & Button untuk memilih folder penyimpanan
path_label = ttk.Label(frame, text="Select Download Path:")
path_label.pack(pady=10)
select_path_button = ttk.Button(frame, text="Browse", command=select_path)
select_path_button.pack(pady=10)

# Dropdown untuk memilih playlist
selected_playlist = StringVar()
playlist_dropdown = ttk.OptionMenu(frame, selected_playlist, "Select Playlist")
playlist_dropdown.pack(pady=10)

# Tombol Download dan Stop
download_button = ttk.Button(frame, text="Download")
download_button.pack(pady=10)

stop_button = ttk.Button(frame, text="Stop Downloading")
stop_button.pack(pady=10)

# Label Status
status_label = ttk.Label(frame, text="Status: Waiting...")
status_label.pack(pady=10)

# Menjalankan GUI
screen.mainloop()