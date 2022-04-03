import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# BASIC ACRONYM SONG SELECTOR

# NOTE:
# You will need to set up the developer access with Spotify and get your Client ID and Client Secret.
# The first time you run this, you will get taken to a webpage. Allow Spotify access to your account.
# You will then need to copy the url and paste it in as the input for the prompt the program gives you.
# This is only a first time thing to give clearance for this program to make a playlist in your Spotify Account.

# NOTE:
# The print statements were left on purpose for anyone interested in seeing the search process or for debugging.
# Feel free to delete them as you see fit.


SPOTIPY_CLIENT_ID =  # YOUR CLIENT ID
SPOTIPY_CLIENT_SECRET =  # YOUR CLIENT SECRET
SPOTIPY_REDIRECT_URI = "https://example.com"
scope = "playlist-modify-private"

LETTERS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
LETTERS_CHECK = [char for char in LETTERS]

print("Welcome to B.A.S.S (Basic Acronym Song Selector)! B.A.S.S. will ask you for a genre of music and for a word or phrase."
      "\nFor every letter in the word/phrase you provided, a random song whose title begins with that letter will be added to a playlist."
      "\nEvery song in the playlist will be from the genre that you chose."
      "\n\nThe playlist name will be a combination of the word/phrase and your genre, so feel free to get creative!\n")
print("Check here first for the correct spelling of your genre: https://spotify-top.com/genres\n")
user_genre = input("What genre do you want: ")
user_string = input("Write the word/phrase (only letters will be used for song titles) ")

letter_list = [char for char in user_string]
print(letter_list)

search_list = []

for letter in letter_list:
    if letter not in LETTERS_CHECK:
        print(f"{letter} is not a letter")
    else:
        search_list.append(letter)
print(search_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope))

user = sp.current_user()
user_id = user['id']

alphabet = "aeiouyxcvbnmsdfghjklptrwqz"

uri_list = []
for letter in search_list:
    song_results = []
    search_results = sp.search(q=f"track:{letter} genre:{user_genre}", type="track", offset=0, limit=50, market="US")
    results_list = search_results["tracks"]["items"]
    for song in results_list:
        print(song["name"])
        print(letter)
        if song["name"][0] in (letter.lower(), letter.upper()):
            print(f'WINNER: {song["name"]}')
            song_results.append(song["uri"])
        if len(song_results) < 5:
            for item in alphabet:
                new_search = f"{letter}{item}"
                print(new_search)
                search_results = sp.search(q=f"track:{new_search} genre:{user_genre}", type="track", offset=0, limit=50,
                                           market="US")
                results_list = search_results["tracks"]["items"]
                for result in results_list:
                    print(result["name"])
                    print(new_search)
                    if result["name"][0] in (letter.lower(), letter.upper()):
                        print(f'WINNER for {new_search}: {result["name"]}')
                        song_results.append(result["uri"])
                if len(song_results) > 5:
                    break
    random.shuffle(song_results)
    if len(song_results) != 0:
        same = len(uri_list)
        for song in song_results:
            if song not in uri_list:
                uri_list.append(song)
                break
        if len(uri_list) == same:
            uri_list.append(song_results[0])
    else:
        print("No results at all. Please check your genre input (spelling, symbols, too niche?)")


print("...")

playlist_create = sp.user_playlist_create(user=user_id,
                        name=f"{user_string} {user_genre.title()}",
                        public="False",
                        collaborative="False",
                        description="Songs that begins with each letter in the title, all in the genre of the title.")

p_id = playlist_create["id"]

if len(uri_list) > 0:
    add_songs_to_playlist = sp.playlist_add_items(playlist_id=p_id, items=uri_list, position=None)
    print("\nSuccess! You're playlist have been created. Go check your Spotify :)")
else:
    print("Sorry, there seems to be no results at all."
          "\nPerhaps the genre was misspelled or it was too specific and narrow to return results."
          "\n\nClick here to check out Spotify's genre list: https://spotify-top.com/genres")
