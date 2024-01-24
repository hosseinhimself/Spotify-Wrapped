import spotipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from spotipy.oauth2 import SpotifyClientCredentials
from keys import client_id, client_secret, redirect_uri


def spotifyID(link):
    # https://open.spotify.com/playlist/3zCK80pE2XepeThGHfwUEz?si=8c637f1e7fde427f
    # https://open.spotify.com/playlist/5WwOvSn7sKdRFEFmmQV58W?si=a44bae5b88d94153
    link = link.replace("https://open.spotify.com/playlist/", "spotify:playlist:")
    return link


def playlist_analyse(link):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.playlist(spotifyID(link))
    playlist = results['name']
    owner = results['owner']['display_name']

    ids = []

    for item in results['tracks']['items']:
        track = item['track']['id']
        ids.append(track)

    song_meta = {'id': [], 'album': [], 'name': [],
                 'artist': [], 'explicit': [], 'popularity': []}

    for song_id in ids:
        # get song's meta data
        meta = sp.track(song_id)

        # song id
        song_meta['id'].append(song_id)

        # album name
        album = meta['album']['name']
        song_meta['album'] += [album]

        # song name
        song = meta['name']
        song_meta['name'] += [song]

        # artists name
        s = ', '
        artist = s.join([singer_name['name'] for singer_name in meta['artists']])
        song_meta['artist'] += [artist]

        # explicit: lyrics could be considered offensive or unsuitable for children
        explicit = meta['explicit']
        song_meta['explicit'].append(explicit)

        # song popularity
        popularity = meta['popularity']
        song_meta['popularity'].append(popularity)

    song_meta_df = pd.DataFrame.from_dict(song_meta)

    # check the song feature
    features = sp.audio_features(song_meta['id'])
    # change dictionary to dataframe
    features_df = pd.DataFrame.from_dict(features)

    # convert milliseconds to mins
    # duration_ms: The duration of the track in milliseconds.
    # 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
    features_df['duration_ms'] = features_df['duration_ms'] / 60000

    # combine two dataframe
    final_df = song_meta_df.merge(features_df)

    music_feature = features_df[
        ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
         'tempo', 'duration_ms']]

    min_max_scaler = MinMaxScaler()
    music_feature.loc[:] = min_max_scaler.fit_transform(music_feature.copy().loc[:])

    fig = plt.figure(figsize=(12, 8))

    categories = list(music_feature.columns)
    N = len(categories)
    value = list(music_feature.mean())
    value += value[:1]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    plt.polar(angles, value)
    plt.fill(angles, value, alpha=0.3)

    plt.title('Discover {} playlist of {}'.format(playlist, owner), size=35)

    plt.xticks(angles[:-1], categories, size=15)
    plt.yticks(color='grey', size=15)
    plt.show()


if __name__ == '__main__':
    playlist_analyse('https://open.spotify.com/playlist/5n862WPBVEHxD6Q3WrGgzK')
