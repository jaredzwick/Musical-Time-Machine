# ----------------------------------- CONSTANTS --------------------------------------------------------- #
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import SpotifyOAuth
spotify_CID = ''
spotify_CS = ''

# ----------------------------------- Input Logic --------------------------------------------------------- #
prompt = input(
    'When would you like to travel to? In YYYY-MM-DD format please! :)\n')
URL = f'https://www.billboard.com/charts/hot-100/{prompt}'

# ----------------------------------- Scrape Website --------------------------------------------------------- #
response = requests.get(URL)
billboard = response.text
soup = BeautifulSoup(billboard, 'html.parser')
songs = soup.find_all(name='span', class_='chart-element__information__song')
song_names = []
for i in songs:
    song_names.append(i.getText())
print(song_names)

# ----------------------------------- Spotify API --------------------------------------------------------- #
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope='playlist-modify-private', client_id=spotify_CID, client_secret=spotify_CS,
                              cache_path='token.txt', redirect_uri='http://example.com')
)
user_id = sp.current_user()['id']
year = prompt.split('-'[0])
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song}", type='track')
    print(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
        print('SONG FOUND')
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")
playlist = sp.user_playlist_create(user=user_id, name=f'{prompt} Top 100 Hits', public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
