import customtkinter as ctk
from tkinter import filedialog
import pyperclip
import time
import threading


def choose_dir():
    folder_path = filedialog.askdirectory()
    if folder_path:
        dir_text.configure(state="normal")
        dir_text.delete("1.0", "end")
        dir_text.insert("1.0", folder_path)
        dir_text.configure(state="disable", text_color="black")


def on_entry_click(event):
    """Hapus placeholder saat user mulai mengetik."""
    if link_entry.get() == "Paste Your Link Here":
        link_entry.delete(0, "end")
        link_entry.configure(text_color="black")  # Ubah warna teks jadi hitam


def on_focus_out(event):
    """Kembalikan placeholder jika input kosong."""
    if link_entry.get() == "":
        link_entry.insert(0, "Paste Your Link Here")
        link_entry.configure(text_color="gray")  # Ubah warna teks jadi abu-abu


def paste_text():
    text = pyperclip.paste()
    link_entry.delete(0, "end")
    link_entry.insert(0, text)
    link_entry.configure(text_color="black") 


def download():
    download_btn.configure(text="Downloading...", state="disabled", fg_color="#127A37")
    dir_btn.configure(state="disabled", fg_color="#127A37")

    dir_path = dir_text.get(1.0, "end-1c")
    if dir_path == "Choose Download Folder":
        print("NOP")
        download_btn.configure(state="normal", text="Download", fg_color="#1DB954")
        dir_btn.configure(state="normal", fg_color="#1DB954")
        return

    progress_bar.place(x=420, y=430)
    progress_bar.set(0)

    def run_progress():
        for i in range(100):
            time.sleep(0.05)  # Simulasi proses download
            progress_bar.set(i / 100)
        download_btn.configure(state="normal", text="Download", fg_color="#1DB954")
        dir_btn.configure(state="normal", text="Download", fg_color="#1DB954")
        progress_bar.place_forget()
    
    threading.Thread(target=run_progress, daemon=True).start()

app = ctk.CTk()
app.geometry("850x600")
app.title("SpotLoader")

main_frame = ctk.CTkFrame(app, fg_color="#1C1818", corner_radius=100)
main_frame.pack(fill="both", expand=True, padx=25, pady=25)

spot_label = ctk.CTkLabel(main_frame, text="Spot", font=("Montserrat", 50, "bold"), text_color="#1DB954", fg_color="#000000", bg_color="black", corner_radius=20) 
spot_label.place(x=20, y=400)

loader_label = ctk.CTkLabel(main_frame, text="Loader", font=("Arial Black", 50, "bold"), text_color="#000000", fg_color="#1DB954", bg_color="#1DB954", corner_radius=35) 
loader_label.place(x=110, y=455)

enjoy_label = ctk.CTkLabel(main_frame, text="Enjoy", font=("Roboto", 40), text_color="#D3D3D3")
enjoy_label.place(x=180, y=25)

your_label = ctk.CTkLabel(main_frame, text="Your Music", font=("Roboto", 40), text_color="#1DB954", fg_color="black", corner_radius=25)
your_label.place(x=280, y=50)

locally_label = ctk.CTkLabel(main_frame, text="Locally", font=("Roboto", 40), text_color="white")
locally_label.place(x=510, y=25)

line_frame = ctk.CTkFrame(main_frame, fg_color="#606060", corner_radius=35, height=20)
line_frame.pack(pady=125, padx=25, fill="x")

dir_frame = ctk.CTkFrame(main_frame, fg_color="white", height=40, width=290)
dir_frame.place(x=30, y=200)
dir_frame.pack_propagate(False)

dir_text = ctk.CTkTextbox(dir_frame, font=("Arial Black", 13, "italic"), text_color="gray", fg_color="white")
dir_text.pack(fill="both", expand=True, padx=5, pady=2)
dir_text.insert("1.0", "Choose Download Folder")
dir_text.configure(state="disable")

dir_btn = ctk.CTkButton(main_frame, text="Choose", font=("Times New Romans", 15, "bold"), command=choose_dir, corner_radius=32, height=40, width=150, text_color="black", fg_color="#1DB954", hover_color="#127A37")
dir_btn.place(x=89, y=270)

link_entry = ctk.CTkEntry(main_frame, fg_color="white", font=("Arial Black", 13, "italic"), height=40, width=290, text_color="#4D4A4A", justify="center")
link_entry.place(x=430, y=200)
link_entry.insert(0, "Paste Your Link Here")
link_entry.bind("<FocusIn>", on_entry_click)
link_entry.bind("<FocusOut>", on_focus_out)

paste_button = ctk.CTkButton(main_frame, text="📋", text_color="white", command=paste_text, font=("Arial Black", 20), fg_color="transparent", hover_color="gray", height=35, width=40)
paste_button.place(x=718, y=202)

download_btn = ctk.CTkButton(main_frame, text="Download", font=("Times New Romans", 15, "bold"), command=download, corner_radius=32, height=40, width=150, text_color="black", fg_color="#1DB954", hover_color="#127A37")
download_btn.place(x=490, y=270)

progress_bar = ctk.CTkProgressBar(main_frame, width=300, height=25, fg_color="black", progress_color="#1DB954")
progress_bar.place_forget

app.mainloop()