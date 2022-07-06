# Spotify GUI
A graphical user interface application replicating Spotify information and features.

## Description
Using the official Spotify API, this program displays an interactive interface of a user's Spotify information which includes, but not limited to, their songs, playlists, and media playback features. The program uses the ```spotipy``` library which receives the data from the official Spotify API. The user must authenticate whether or not the program is allowed to use their information, which is prompted when the user runs the program for the first time. Once authenticated, the program reads and cleans the data for visualization.

## Getting Started
### Dependencies
* Ensure intended browser of use is updated to most recent version. Google Chrome or Mozilla Firefox is preferred.
* Python version is the latest installed.
* pip version is the latest installed.
```
python -m pip install --upgrade pip
```

### Setup
* You must have a valid ```client id``` and ```client_secret id``` from the official Spotify Web API in order to access a user's Spotify information. <br>
* Please visit https://developer.spotify.com/documentation/web-api/quick-start/ to learn how to setup this project with your API.

### Installation
Create a new folder and run the following commands in terminal:
``` 
git clone https://github.com/jdinh-782/Spotify-GUI.git

cd Spotify-GUI 
```

Now that you are inside the main directory, please install the included packages:
```
pip install -r requirements.txt
```

### Execution
Assuming all packages and dependencies are installed correctly, you may run the program with the following command: 

```python3 main.py```

## Help
For any concerns, feel free to reach out to me by [email](jdinh782@gmail.com).

## Authors and Contributors
[Johnson Dinh](https://www.linkedin.com/in/johnson-dinh/) <br>

## Acknowledgements
[Spotify](https://developer.spotify.com/documentation/web-api/) <br>
[Spotipy](https://spotipy.readthedocs.io/en/master/)
