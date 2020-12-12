"""
Name: Johnson Dinh
Final Project: Spotify GUI
"""

import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request as u
from threading import Timer
import requests
from io import BytesIO

repeat_counter = 0
shuffle_counter = 0
add_to_playlist_counter = 0
remove_from_playlist_counter = 0
create_playlist_counter = 0


class Spotify:
    def __init__(self):
        # initialize a user id by client id and secret id
        # self._sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="3234d025cf284364bc4a0065254a42be",
        #                                                            client_secret="be160b11ea984c00931d0f0127b8190d"))
        #
        # # search for songs from artists ('n' items)
        # results = self._sp.search(q='Lil Uzi Vert', limit=10)
        #
        # print("Lil Uzi Vert")
        # for index, track in enumerate(results['tracks']['items']):
        #     print(f"{index + 1:>2}: {track['name']}")

        # initialize a user id with redirect url and scope
        self._CLIENT_ID = "3234d025cf284364bc4a0065254a42be"
        self._CLIENT_SECRET = "be160b11ea984c00931d0f0127b8190d"
        self._REDIRECT_URL = "https://jdinh782.wixsite.com/lifeofjdinh"  # continuously update this
        self._SCOPE = "user-read-playback-state user-modify-playback-state playlist-modify-public " \
                      "playlist-modify-private user-top-read"

        self._sp_user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self._CLIENT_ID,
                                                                  client_secret=self._CLIENT_SECRET,
                                                                  redirect_uri=self._REDIRECT_URL,
                                                                  scope=self._SCOPE))

        # prints out songs from user's playlist
        # url = 'spotify:playlist:20LtD89u2QvuiJ02ZFf99Q'
        # results = self._sp_user.playlist_items(url)
        # playlist = self._sp_user.playlist(url)
        #
        # print(f"\n{playlist['name']} - {playlist['owner']['display_name']}")
        #
        # for index, item in enumerate(results['items'][:10]):
        #     track = item['track']
        #     print(f"{index + 1:>2}: {track['artists'][0]['name']} - {track['name']}")

        self._currently_playing = self._sp_user.currently_playing()

        self._artist_name = self._currently_playing['item']['artists'][0]['name']
        self._currently_playing_track_name = self._currently_playing['item']['name']

        # print(f"\n{self._currently_playing_track_name} - {self._artist_name}")

        s1 = self._currently_playing['item']['album']['images'][0]

        # print(s.get('url'))  # gets the url from the current song

        current_song_image_url = s1.get('url')

        u.urlretrieve(current_song_image_url, "pic.png")

        # print(f"{self._currently_playing['item']['uri']}")

        # prints user's top artists (short_term = 20 results)
        self._user_top_artists = self._sp_user.current_user_top_artists(limit=20, time_range='short_term')

        # for i in range(0, 19):
        #     print(self._user_top_artists['items'][i]['name'])

    def return_currently_playing_track_name(self):
        return self._currently_playing_track_name

    def return_currently_playing_artist_name(self):
        return self._artist_name

    def return_track_image(self):
        s1 = self._currently_playing['item']['album']['images'][0]
        current_song_image_url = s1.get('url')
        img_url = current_song_image_url
        response = requests.get(img_url)
        img_data = response.content

        return img_data

    # grab user input from entry (option)
    def get_input(self):
        input_from_entry = menu_entry.get()

        global choice
        choice = input_from_entry

        if input_from_entry == '1':
            print("\nEnter Artist Name In the Bottom Text Field")

        if input_from_entry == '2':
            print("\nEnter Keyword In the Bottom Text Field")

        if input_from_entry == '3':
            print("\nResetting Current Track...")
            self.reset_track()

        if input_from_entry == '4':
            print("\nEnter Song URI In The Bottom Text Field")

        if input_from_entry == '5':
            print("\nPlease Enter The Account URI In The Bottom Text Field (Only Numbers)")

        if input_from_entry == '6' or input_from_entry == '7':
            print("\nEnter Playlist URI In the Bottom Text Field")

    # resets the song
    def reset_track(self):
        self._sp_user.seek_track(position_ms=0)

    # will call a function to do a specific action based on user input
    def do_specific_action(self):
        search = Search()
        p = Playlist()

        if choice == '1' or choice == '2':
            search.search_songs()

        if choice == '4':
            self.add_track_to_queue()

        if choice == '5' or choice == '6' or choice == '7':
            p.get_playlist_input(choice)

    # adds a song to the queue
    def add_track_to_queue(self):
        self._sp_user.add_to_queue(input_entry.get())

    # returns the track image url to process the image in GUI
    def return_track_image_url(self):
        s1 = self._currently_playing['item']['album']['images'][0]
        current_song_image_url = s1.get('url')
        img_url = current_song_image_url
        response = requests.get(img_url)
        img_data = response.content

        return img_data

    # update the currently playing track details
    def update_track_details(self):
        global new_track_name, new_track_artist
        new_currently_playing = self._sp_user.currently_playing()
        s = new_currently_playing['item']['album']['images'][0]
        current_song_image_url = s.get('url')
        img_url = current_song_image_url
        response = requests.get(img_url)
        img_data = response.content

        new_image = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        image_panel.configure(image=new_image)
        image_panel.image = new_image

        new_track_name = new_currently_playing['item']['name']
        currently_playing_track_text.configure(text=new_track_name)

        new_track_artist = new_currently_playing['item']['artists'][0]['name']
        currently_playing_artist_text.configure(text=f"Main Artist: {new_track_artist}")

        print(f"\nPlaying: {new_track_name} - {new_track_artist}")


class SpotifyGUI:
    def __init__(self, root):
        self._backend = Spotify()
        m = MediaPlayback()

        root.title("Bootleg Spotify")
        root.configure(background='black')
        root.geometry("1465x768")  # originally 745x550

        # img = ImageTk.PhotoImage(Image.open(BytesIO(self._backend.return_track_image_url())))
        img = ImageTk.PhotoImage(Image.open("pic.png").resize((640, 640)))

        global image_panel
        image_panel = tk.Label(root, image=img)
        image_panel.place(x=50, y=50)

        global currently_playing_track_text
        currently_playing_track_text = tk.Label(text=self._backend.return_currently_playing_track_name())
        currently_playing_track_text.config(font=("Segoe Print", 15), fg="White", bg="Black")
        currently_playing_track_text.place(x=715, y=450)

        global currently_playing_artist_text
        currently_playing_artist_text = tk.Label(
            text=f"Main Artist: {self._backend.return_currently_playing_artist_name()}")
        currently_playing_artist_text.config(font=("Segoe Print", 13), fg="White", bg="Black")
        currently_playing_artist_text.place(x=715, y=485)

        play_button_image = tk.PhotoImage(file="play_button_pic.png")
        play_button_image = play_button_image.zoom(10)
        play_button_image = play_button_image.subsample(7)
        play_button = tk.Button(image=play_button_image, command=m.play_button_action)
        play_button.place(x=950, y=550)

        pause_button_image = tk.PhotoImage(file="pause_button_pic.png")
        pause_button_image = pause_button_image.zoom(10)
        pause_button_image = pause_button_image.subsample(7)
        pause_button = tk.Button(image=pause_button_image, command=m.pause_button_action)
        pause_button.place(x=1075, y=550)

        skip_button_image = tk.PhotoImage(file="skip_button_pic.png")
        skip_button_image = skip_button_image.zoom(10)
        skip_button_image = skip_button_image.subsample(7)
        skip_button = tk.Button(image=skip_button_image, command=m.skip_button_action)
        skip_button.place(x=1185, y=550)

        previous_button_image = tk.PhotoImage(file="previous_button_pic.png")
        previous_button_image = previous_button_image.zoom(10)
        previous_button_image = previous_button_image.subsample(7)
        previous_button = tk.Button(image=previous_button_image, command=m.previous_button_action)
        previous_button.place(x=875, y=550)

        shuffle_button_image = tk.PhotoImage(file="shuffle_button_pic.png")
        shuffle_button_image = shuffle_button_image.zoom(10)
        shuffle_button_image = shuffle_button_image.subsample(7)
        shuffle_button = tk.Button(image=shuffle_button_image, command=m.shuffle_button_action)
        shuffle_button.place(x=965, y=650)

        repeat_button_image = tk.PhotoImage(file="repeat_button_pic.png")
        repeat_button_image = repeat_button_image.zoom(10)
        repeat_button_image = repeat_button_image.subsample(7)
        repeat_button = tk.Button(image=repeat_button_image, command=m.repeat_button_action)
        repeat_button.place(x=1090, y=650)

        # change to menu image
        menu_image = tk.PhotoImage(file="menu.png")
        menu_image = menu_image.zoom(10)
        menu_image = menu_image.subsample(8)
        menu = tk.Label(image=menu_image)
        menu.place(x=775, y=100)

        global menu_entry
        menu_entry = tk.Entry(bd=5, width=3, font="Calibri 20")
        menu_entry.place(x=1100, y=100, height=50)

        menu_button = tk.Button(bd=5, width=10, text='Enter', font=0, command=self._backend.get_input)
        menu_button.place(x=1154, y=100, height=52)

        global input_entry
        input_entry = tk.Entry(bd=5, width=36, font="Calibri 15")
        input_entry.place(x=770, y=315, height=50)

        input_entry_button = tk.Button(bd=5, width=10, text='Enter', font=0, command=self._backend.do_specific_action)
        input_entry_button.place(x=1106, y=315, height=52)

        root.mainloop()


# handles the media playback for the music
class MediaPlayback(Spotify):
    def __init__(self):
        super().__init__()

    # plays the current songs (or resumes from pausing)
    def play_button_action(self):
        self._sp_user.start_playback()

        t = Timer(0.5, self.update_track_details)  # use 0.5 or 1 to be safe
        t.start()

    # pauses user's playback
    def pause_button_action(self):
        self._sp_user.pause_playback()
        print("\nPause: On")
        t = Timer(0.5, self.update_track_details)  # use 0.5 or 1 to be safe
        t.start()

    # skips to next song in queue and update track details
    def skip_button_action(self):
        self._sp_user.next_track()

        # update the track image
        t = Timer(0.5, self.update_track_details)  # use 0.5 or 1 to be safe
        t.start()

        # currently_playing = self._sp_user.currently_playing()
        # new_track_name = currently_playing['item']['name']
        # currently_playing_track_text.configure(text=new_track_name)
        #
        # new_track_artist = currently_playing['item']['artists'][0]['name']
        # currently_playing_artist_text.configure(text=f"Main Artist: {new_track_artist}")
        #
        # current_track = currently_playing['item']['album']['images'][0]
        #
        # # fix this so that image updates in real time
        # current_song_image_url = current_track.get('url')
        # u.urlretrieve(current_song_image_url, "pic.png")
        # new_track_image = "pic.png"
        #
        # root.new_track_image = ImageTk.PhotoImage(Image.open(new_track_image).resize((260, 260)))
        # image.configure(image=root.new_track_image)

    # goes to the previous song
    def previous_button_action(self):
        self._sp_user.previous_track()

        t = Timer(0.5, self.update_track_details)  # use 0.5 or 1 to be safe
        t.start()

    # shuffles the user's playback queue
    def shuffle_button_action(self):
        global shuffle_counter
        if shuffle_counter == 0:
            self._sp_user.shuffle(state=True)  # if true, then shuffle
            print("\nShuffle Mode: On")
            shuffle_counter = 1

        elif shuffle_counter == 1:
            self._sp_user.shuffle(state=False)
            print("\nShuffle Mode: Off")
            shuffle_counter = 0

    # repeats the current song (adds it to top of queue)
    def repeat_button_action(self):
        global repeat_counter
        if repeat_counter == 0:
            self._sp_user.repeat(state="track")  # if "track", repeat the entire track again
            print("\nRepeat Mode: On")
            repeat_counter = 1

        elif repeat_counter == 1:
            self._sp_user.repeat(state="off")
            print("\nRepeat Mode: Off")
            repeat_counter = 0


# class for for playlist operation
class Playlist(Spotify):
    def __init__(self):
        super().__init__()

    # determine what the user wants to do with the playlist
    def get_playlist_input(self, choice):
        if choice == '5':
            global playlist_account_id, create_playlist_counter
            if create_playlist_counter == 0:
                playlist_account_id = input_entry.get()
                input_entry.delete(0, 'end')

                print("\nNow Enter Playlist Name In The Bottom Text Field")
                create_playlist_counter += 1

            elif create_playlist_counter == 1:
                global created_playlist_name

                created_playlist_name = input_entry.get()

                self.create_playlist()
                input_entry.delete(0, 'end')
                create_playlist_counter = 0

        elif choice == '6':
            global add_to_playlist_uri, add_to_playlist_counter

            if add_to_playlist_counter == 0:
                add_to_playlist_uri = input_entry.get()
                input_entry.delete(0, 'end')  # only clears the text field

                print("\nNow Enter Track URI To Be Added In the Bottom Text Field")
                add_to_playlist_counter += 1

            elif add_to_playlist_counter == 1:
                global add_track_id_list
                add_track_id_list = list()
                add_track_id_list.append(input_entry.get())

                # print(playlist_uri)
                # print(add_track_id_list)

                self.add_track_to_playlist()
                input_entry.delete(0, 'end')
                add_track_id_list.clear()
                # add_to_playlist_uri = None
                add_to_playlist_counter = 0

        elif choice == '7':
            global remove_from_playlist_uri, remove_from_playlist_counter

            if remove_from_playlist_counter == 0:
                remove_from_playlist_uri = input_entry.get()
                input_entry.delete(0, 'end')  # only clears the text field

                print("\nNow Enter Track URI To Be Removed In the Bottom Text Field")
                remove_from_playlist_counter += 1

            elif remove_from_playlist_counter == 1:
                global remove_track_id_list
                remove_track_id_list = list()
                remove_track_id_list.append(input_entry.get())

                self.remove_track_from_playlist()
                input_entry.delete(0, 'end')
                remove_track_id_list = None
                remove_from_playlist_uri = None
                remove_from_playlist_counter = 0

    # begin creation of playlist (private)
    def create_playlist(self):
        # the "user=" id below must be the user id the user wants to create playlists to (essentially the account)
        self._sp_user.user_playlist_create(user=playlist_account_id, name=created_playlist_name, public=False,
                                           description="Made From Johnson's Spotify Program!")
        print(f'\nPlaylist "{created_playlist_name}" Added To Account!')

    # adds a track/episode to a user's playlist of choice
    def add_track_to_playlist(self):
        self._sp_user.playlist_add_items(playlist_id=add_to_playlist_uri, items=add_track_id_list)

    # removes a track/episode to a user's playlist of choice (all occurrences of it - duplicates)
    def remove_track_from_playlist(self):
        self._sp_user.playlist_remove_all_occurrences_of_items(playlist_id=remove_from_playlist_uri,
                                                               items=remove_track_id_list)


# handles the search function for Spotify
class Search(Spotify):
    def __init__(self):
        super().__init__()

    # searches songs by artist name/keyword - only one universal search function
    def search_songs(self):
        results = self._sp_user.search(q=input_entry.get(), type="track", limit=10)  # n = 10 items

        if choice == "1":
            print(f'\nArtist: "{input_entry.get()}" (Top 10 Results)')
        elif choice == '2':
            print(f'\nKeyword: "{input_entry.get()}" (Top 10 Results)')

        for index, track in enumerate(results['tracks']['items']):
            print(f"{index + 1:>2}: {track['name']} - {track['album']['artists'][0]['name']}"
                  f"\n - track id: spotify:track:{track['id']}\n")


if __name__ == "__main__":
    print("\n[1] Search Songs By Artist"
          "\n[2] Search Songs By Keyword"
          "\n[3] Reset Track"
          "\n[4] Add Song To Queue"
          "\n[5] Create Playlist"
          "\n[6] Add Song To Playlist"
          "\n[7] Remove Song From Playlist")

    root = tk.Tk()
    s = SpotifyGUI(root)
