import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from bs4 import BeautifulSoup
import base64
import requests
import schedule
import time
os.environ['SPOTIPY_CLIENT_ID'] = os.environ.get('SPOTIPY_CLIENT_ID')
os.environ['SPOTIPY_CLIENT_SECRET'] = os.environ.get('SPOTIPY_CLIENT_SECRET')
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

scope = "playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

URL = "https://kworb.net/spotify/country/us_daily.html"
def fetch_songs():
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="spotifydaily")

    artist_song_elements = results.find_all("a", href=True)
    artist_song_elements = list(artist_song_elements)

    FETCHED_URIS = []
    for a_tag in artist_song_elements:
        link = a_tag["href"]
        if "track" in link:
            FETCHED_URIS.append("spotify:track:"+link.split("/")[-1].split(".")[0])

    print(f"Fetched {len(FETCHED_URIS)} songs")
    return FETCHED_URIS
username = os.environ.get("SPOTIPY_USERNAME"),
playlist_id = os.environ.get("SPOTIPY_PLAYLIST_ID")

def remove_current_songs(stage=None):
    current_songs = sp.playlist_items(playlist_id)["items"]
    current_song_uris = [song["track"]['id'] for song in current_songs]


    sp.user_playlist_remove_all_occurrences_of_tracks(
        username,
        playlist_id,
        current_song_uris,
    )
    print(f"Removed {len(current_song_uris)} songs from playlist for Stage {stage}")

def add_songs_to_playlist(uris_to_add, stage=None):
    sp.user_playlist_add_tracks(
        username,
        playlist_id,
        uris_to_add
    )
    print(f"Added {len(uris_to_add)} songs to playlist for Stage {stage}")

def update_playlist() -> None:
    FETCHED_URIS = fetch_songs()
    remove_current_songs(stage=1)
    remove_current_songs(stage=2)
    add_songs_to_playlist(FETCHED_URIS[:100], stage=1)
    add_songs_to_playlist(FETCHED_URIS[100:200], stage=2)
   
schedule.every().day.at("00:00").do(update_playlist)
while True:
    schedule.run_pending()
    time.sleep(1)