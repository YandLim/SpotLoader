# [SpotLoader](https://github.com/YandLim/SpotLoader)
Start: 23/02/25  |  Finish: 28/02/25

Download any song, playlist even album to enjoy them locally as .mp3 format.
Easy to use, and lightweight made using python and custom tkinter for friendly interface.

## The story behind the project
Have you ever enjoying the song 

## How to run the program:
1. Donwload the modules from requirement.txt using
```
pip install -r requirements.txt
```

2. Set up your Spotify API credentials: Go to the Spotify Dashboard and create a new app. Then, copy and paste the Client ID, Client Secret, and Redirect URL into a .env file in the root directory of the project like the following:
```
CLIENT_ID=<YOUR_CLIENT_ID> CLIENT_SECRET=<YOUR_CLIENT_SECRET>
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

## Feedback
If you encounter any problems with this application or have idea for other feature, please feel free to open an issue on the Github page so that the maintainers can assist you.
