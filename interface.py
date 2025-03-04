# Importing Modules
import customtkinter as ctk
from tkinter import filedialog
import pyperclip
import threading
from backend import Main
import os
import shutil

# Making the front-end class
class App(ctk.CTk):
    # Make the auto start function
    def __init__(self):
        super().__init__() # Set the CTK to be functioning
        # Make the base frame
        self.geometry("850x600")
        self.title("SpotLoader")
        self._set_appearance_mode("dark")
        self.iconbitmap("SpotLoader.ico")

        # Make the Main frame to store the content
        self.main_frame = ctk.CTkFrame(self, fg_color="#202528", corner_radius=100, border_width=5, border_color="black")
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Make the title
        self.spot_label = ctk.CTkLabel(self.main_frame, text="Spot", font=("Montserrat", 50, "bold"), text_color="#1DB954", fg_color="#000000", bg_color="black", corner_radius=20) 
        self.spot_label.place(x=20, y=400)

        self.loader_label = ctk.CTkLabel(self.main_frame, text="Loader", font=("Arial Black", 50, "bold"), text_color="#000000", fg_color="#1DB954", bg_color="#1DB954", corner_radius=35) 
        self.loader_label.place(x=110, y=455)

        self.enjoy_label = ctk.CTkLabel(self.main_frame, text="Enjoy", font=("Roboto", 40), text_color="#D3D3D3")
        self.enjoy_label.place(x=180, y=25)

        self.your_label = ctk.CTkLabel(self.main_frame, text="Your Music", font=("Roboto", 40), text_color="#1DB954", fg_color="black", corner_radius=25)
        self.your_label.place(x=280, y=50)

        self.locally_label = ctk.CTkLabel(self.main_frame, text="Locally", font=("Roboto", 40), text_color="white")
        self.locally_label.place(x=510, y=25)

        self.line_frame = ctk.CTkFrame(self.main_frame, fg_color="#606060", corner_radius=35, height=20)
        self.line_frame.pack(pady=125, padx=25, fill="x")

        # Make the Choose download folder section
        self.dir_frame = ctk.CTkFrame(self.main_frame, fg_color="white", height=40, width=290, border_width=4, border_color="gray")
        self.dir_frame.place(x=33, y=200)
        self.dir_frame.pack_propagate(False)

        self.dir_text = ctk.CTkTextbox(self.dir_frame, font=("Arial Black", 13, "italic"), text_color="gray", fg_color="white")
        self.dir_text.pack(fill="both", expand=True, padx=5, pady=2)
        self.dir_text.insert("1.0", "Choose Download Folder")
        self.dir_text.configure(state="disable")

        self.dir_btn = ctk.CTkButton(self.main_frame, text="Choose", font=("Times New Romans", 15, "bold"), command=self.choose_dir, corner_radius=32, height=40, width=150, text_color="black", fg_color="#1DB954", hover_color="#127A37", border_width=3, border_color="black")
        self.dir_btn.place(x=93, y=270)

        # Make the link entry section
        self.link_entry = ctk.CTkEntry(self.main_frame, fg_color="white", font=("Arial Black", 13, "italic"), height=40, width=290, text_color="#4D4A4A", justify="center", border_width=4, border_color="gray")
        self.link_entry.place(x=430, y=200)
        self.link_entry.insert(0, "Paste Your Link Here")
        self.link_entry.bind("<FocusIn>", self.on_entry_click)
        self.link_entry.bind("<FocusOut>", self.on_focus_out)

        self.paste_button = ctk.CTkButton(self.main_frame, text="📋", text_color="white", command=self.paste_text, font=("Arial Black", 20), fg_color="transparent", hover_color="gray", height=35, width=40)
        self.paste_button.place(x=718, y=202)

        self.download_btn = ctk.CTkButton(self.main_frame, text="Download", font=("Times New Romans", 15, "bold"), command=self.download, corner_radius=32, height=40, width=150, text_color="black", fg_color="#1DB954", hover_color="#127A37", border_width=3, border_color="black")
        self.download_btn.place(x=490, y=270)

        # Make info frame for printing info out
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color="#32CD32", width=345, height=120)
        self.info_frame.place(x=410, y=338)

        self.info_sign = ctk.CTkTextbox(self.main_frame, font=("Arial Black", 15), text_color="#428945", fg_color="transparent", width=320, height=95)
        self.info_sign.place(x=420, y=350)
        self.info_sign.insert("1.0", "Welcome to Spotloader 🎶🎶")
        self.info_sign.configure(state="disabled")

        # Set the proggres bar with precentage
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=300, height=25, fg_color="black", progress_color="#1DB954", border_width=1, border_color="white")
        self.progress_bar.place_forget()

        self.precentage_lbl = ctk.CTkLabel(self.main_frame, text="0%", font=("Times New Roman", 25, "bold"), text_color="gray")
        self.precentage_lbl.place_forget()


    # Function to printing in info
    def print_info(self, info):
        self.info_sign.configure(state="normal")
        self.info_sign.insert("end", "\n" + info)
        self.info_sign.configure(state="disabled")
        self.info_sign.see("end")


    # Updating the shown precentage
    def update_precentage(self, number, total):
        raw_value = number / total
        value = f"{raw_value * 100:.1f}%"
        self.precentage_lbl.configure(text=value)

    # Function to choosing the directory
    def choose_dir(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.dir_text.configure(state="normal")
            self.dir_text.delete("1.0", "end")
            self.dir_text.insert("1.0", folder_path)
            self.dir_text.configure(state="disable", text_color="black")


    # To make the default text visible and not visible when typing
    def on_entry_click(self, event):
        # Make the typing text more visible when typing
        if self.link_entry.get() == "Paste Your Link Here":
            self.link_entry.delete(0, "end")
            self.link_entry.configure(text_color="black")


    def on_focus_out(self, event):
        # printing the default text if it's empty
        if self.link_entry.get() == "":
            self.link_entry.insert(0, "Paste Your Link Here")
            self.link_entry.configure(text_color="gray")  # Ubah warna teks jadi abu-abu


    # Paste button
    def paste_text(self):
        text = pyperclip.paste()
        self.link_entry.delete(0, "end")
        self.link_entry.insert(0, text)
        self.link_entry.configure(text_color="black") 


    # Main funtion after clicking download button
    def download(self):
        # Define backend class
        main = Main()

        # Make all the button disable to click after clicking download button
        self.download_btn.configure(text="Downloading...", state="disabled", fg_color="#127A37")
        self.dir_btn.configure(state="disabled", fg_color="#127A37")

        # Checking if download path is avaible. If not, ask it again
        dir_path = self.dir_text.get(1.0, "end-1c")
        if dir_path == "Choose Download Folder":
            self.print_info("Pls Choose The Save Folder")
            self.download_btn.configure(state="normal", text="Download", fg_color="#1DB954")
            self.dir_btn.configure(state="normal", fg_color="#1DB954")
            return
        
        # Checking if spotify's link is avaible. If not, ask it again
        try:
            user_link = self.link_entry.get()
        except:
            self.print_info("Pls Enter The Spotify's link")
            self.download_btn.configure(state="normal", text="Download", fg_color="#1DB954")
            self.dir_btn.configure(state="normal", fg_color="#1DB954")
            return

        if user_link == "Paste Your Link Here":
            self.print_info("Pls Enter The Spotify's link")
            self.download_btn.configure(state="normal", text="Download", fg_color="#1DB954")
            self.dir_btn.configure(state="normal", fg_color="#1DB954")
            return
        
        # Clear the link to be readable
        splitting = user_link[8:].split("/")
        user_link = user_link[:8] + "/".join(splitting).split("?")[0]
        
        # Running the backend program
        def run_progress():
            # Define needed variabels
            found_song = []
            thumbnail_url = []
            token = main.get_token()
            max_tried = 3
            DOWNLOAD_FOLDER = dir_path
            PIC_FOLDER = os.path.join(DOWNLOAD_FOLDER, "Pic")

            # Checking if download path is avaible. If not, make one
            if not os.path.exists(PIC_FOLDER):
                os.makedirs(PIC_FOLDER)

            # Printing info out 
            self.print_info("\nFound Song:")

            try:
                # If it is album
                if user_link.split("/")[3] == "album":
                    playlist_id = user_link.split("/")[4]
                    playlist_songs = main.get_album_song(token, playlist_id)
                    items = playlist_songs["tracks"]["items"]

                    # Printing one by one with number for cleaner output
                    for idx, song in enumerate(items):
                        full_title = f"{song["artists"][0]["name"]} - {song['name']}"

                        # Store all founded songs and thumbnails 
                        thumbnail_url.append(playlist_songs["images"][0]["url"])
                        found_song.append(full_title)

                # If it is playlist
                elif user_link.split("/")[3] == "playlist":
                    playlist_id = user_link.split("/")[4]
                    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
                    playlist_songs, next_playlist = main.get_playlist_song(token, playlist_url)
                    items = playlist_songs["items"]

                    # If song is more than 100, proccesing every 100
                    if next_playlist:
                        while next_playlist:
                            playlist_songs, next_playlist = main.get_playlist_song(token, next_playlist)
                            items.extend(playlist_songs["items"])
                        for idx, song in enumerate(items):
                            try:
                                full_title = f"{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}"

                                thumbnail_url.append(song["track"]["album"]["images"][0]["url"])
                                found_song.append(full_title)
                            except:
                                continue
                            

                    # If not 100 or less than 100 
                    else:
                        for idx, song in enumerate(items):
                            full_title = f"{song["track"]["name"]} - {song["track"]["artists"][0]["name"]}"

                            thumbnail_url.append(song["track"]["album"]["images"][0]["url"])
                            found_song.append(full_title)

                # If it is individual song
                elif user_link.split("/")[3] == "track":
                    song_id = user_link.split("/")[4]
                    song = main.get_songs(token, song_id)
                    full_title = f"{song["artists"][0]["name"]} - {song["name"]}"

                    thumbnail_url.append(song["album"]["images"][0]["url"])
                    found_song.append(full_title)

                for idx, song in enumerate(found_song):
                    self.print_info(f"{idx + 1}: {song}")


                # Shown the hidden progress bar and precentage 
                self.progress_bar.set(0)
                self.progress_bar.place(x=420, y=480)
                self.precentage_lbl.configure(text= "0%")
                self.precentage_lbl.place(x=550, y=513)

                # Define the total item found
                found_song_len = len(found_song)

                # Remove all the ureadeable symbol from name
                sanitize_name = []
                self.progress_bar.set(0)
                self.precentage_lbl.configure(text= "0%")
                self.print_info("🧹 Cleaning file name")
                for i , file_name in enumerate(found_song):
                    for _ in range(max_tried):
                        try:
                            sanitize = main.sanitize_filename(file_name)
                            sanitize_name.append(sanitize)
                            self.progress_bar.set((i + 1)/ found_song_len)
                            self.update_precentage(i + 1, found_song_len)
                            break
                        except Exception as e:
                            self.print_info(f"Error {_}\nRetrying the procces")
                self.print_info("✨ Name clean")
        

                # Find the song, updating precentage and progress bar
                youtube_links = []
                self.print_info("\n🔎 Looking for the song in YouTube")     
                for i, song in enumerate(found_song):
                    youtube_link = main.search_youtube(song)
                    youtube_links.append(youtube_link)
                    self.progress_bar.set((i + 1)/ found_song_len)
                    self.update_precentage(i + 1, found_song_len)
                self.print_info(f"🎶 Found {len(youtube_links)} link")


                # Downloading the songs set precentage and progress bar to 0 and updating them again
                song_file_name = []
                self.progress_bar.set(0)
                self.precentage_lbl.configure(text= "0%")
                self.print_info("🗂️Downloading the songs") 
                for i, (url, name) in enumerate(zip(youtube_links, sanitize_name)):
                    for _ in range(max_tried):
                        try:                        
                            file_name = main.download_song(url, name, DOWNLOAD_FOLDER)
                            song_file_name.append(file_name)
                            self.progress_bar.set((i + 1)/ found_song_len)
                            self.update_precentage(i + 1, found_song_len)
                            break
                        except Exception as e:
                            self.print_info(f"Error ocured:\n{e}\nRetrying the procces")
                self.print_info(f"🎉 Success downloading {len(song_file_name)} Songs") 
                        
                    
                # Downloading the thumbnail
                cover_pic_name = []
                self.progress_bar.set(0)
                self.precentage_lbl.configure(text= "0%")
                self.print_info("🖼️Downloading the thumbnail") 
                for i, (url, name) in enumerate(zip(thumbnail_url, sanitize_name)):
                    for _ in range(max_tried):
                        try:
                            cover_name = main.get_thumbnail(url, name, PIC_FOLDER)
                            cover_pic_name.append(cover_name)
                            self.progress_bar.set((i + 1)/ found_song_len)
                            self.update_precentage(i + 1, found_song_len)
                            break
                        except Exception as e:
                            self.print_info(f"Error ocured:\n{e}\nRetrying the procces")
                self.print_info("👌 Got'em") 
                        

                # Changing the thumbnail for every song
                self.progress_bar.set(0)
                self.precentage_lbl.configure(text= "0%")
                self.print_info("🎨 Changing the song's thumbnail") 
                for i, (song, cover_pic) in enumerate(zip(song_file_name, cover_pic_name)):
                    for _ in range(max_tried):
                        try:
                            main.add_thumbnail(song, cover_pic, DOWNLOAD_FOLDER)
                            self.progress_bar.set((i + 1)/ found_song_len)
                            self.update_precentage(i + 1, found_song_len)
                            break
                        except:
                            continue
                self.print_info("🎵 All thumbnails updated successfully!") 
                    

                # Remove the pic folder with the thumbnail pic in it
                shutil.rmtree(PIC_FOLDER)

            except Exception as e:
                self.print_info("Some error occured pls try again and check the Internet Conection.\n If error keep happening, pls contact the developer team")

            finally:
                # Make the button avaible and hide the progress and precentage bar
                self.progress_bar.place_forget()
                self.precentage_lbl.place_forget()     
                self.download_btn.configure(state="normal", text="Download", fg_color="#1DB954")
                self.dir_btn.configure(state="normal", fg_color="#1DB954")


        threading.Thread(target=run_progress, daemon=True).start()
