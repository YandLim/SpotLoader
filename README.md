# [SpotLoader](https://github.com/YandLim/SpotLoader)
Start: 23/02/25  |  Finish: 28/02/25

Download any song, playlist even album to enjoy them locally as .mp3 format.
Easy to use, and lightweight made using python and custom tkinter for friendly interface.

## The story behind the project
Have you ever enjoying the song but suddenly buffer is coming to ruin it or you want to watch youtube from your phone and enjoying music using bloototh speaker?
Of course it's happening so I was thinking. Why I dont use flashdisk or memory card to hear my music with speaker? And that's where the excitement of solving problem comes. To do that I need the music locally and i was thingking should i use YouTube to download them? But YouTube is complicated to adding video to one playlist Spotify is my favorite so far but you can't download them. What should i do then? Then I remember, that's right I'm a software developer my job is bring the solution from thought to live.

To Build the app i use Python as main language, and custom tkinter as modern friendly interface. Instead of scraping the spotify using bs4, or selenium I use the API of spotify itself that makes me unstoppable at get the data.
After get the name of each song from playlist or album I pass them to youtube to find the right accurate video of the song. And after that I download them and change the song cover to the same cover picture from the spotify.

## How to run the program:
1. Donwload the modules from requirement.txt using
```
pip install -r requirements.txt
```

2. Set up your Spotify API credentials: Go to the Spotify Dashboard and create a new app. Then, copy and paste the Client ID, Client Secret, and Redirect URL into a .env file in the root directory of the project like the following:
```
CLIENT_ID=<YOUR_CLIENT_ID>
CLIENT_SECRET=<YOUR_CLIENT_SECRET>
```

3. Open the main.py in your code editor and run it.

4. If you want to make it as exe file download pyinstaller and
```
pyinstaller --onedir --windowed --icon=SpotLoader.ico main.py
```

5. If you make the exe file copy the .ico file to same dir as the main.exe file and the ffmpeg_apk in the same dir as main.exe file as well

6. After the interface appear, click choose button to choose the dir to store the downloaded song
    
7. Enter the link playlist, song, or album
   
8. Click download and it would take some time

## The libraries or framework I work with:
1. Dotenv
   - Store the API code
   - More secure
2. Requests
   - To get the needed data from API
   - Faster and lightweight
3. Yt_Dlp
   - To Find the right video from YouTube
   - TO download the video from youtube
4. Mutagen.mp3
   - Convert the downloaded video to mp3 format
   - Changing the .mp3 file name
5. Custom Tkinter
   - To make modern Interface
   - Make better user experience
6. Tkinter
   - Use the FileDialog function to choose directory
7. Pyperclip
   - Make the paste button
8. Shutil
   - Removing the unusable directory

## What I Learn
- Separating the Interface and Backend is always a good idea
- Commenting a important function could be come in handy later
- Working with API is way more recomended than scraping without API
- Making flowchart for yourself can't be really helpfull(I Think)
   
## Feedback
If you encounter any problems with this application or have idea for other feature, please feel free to open an issue on the Github page so that the maintainers can assist you.
