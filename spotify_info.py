import sys
import time
import urllib.request
from collections import Counter
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import spotipy
import spotipy.util as util
from keys import client_id, client_secret, redirect_uri


def get_track_ids(time_frame):
    return [song['id'] for song in time_frame['items']]


def get_artist_features(id, sp):
    meta = sp.track(id)
    artist_id = meta['album']['artists'][0]['uri']
    artist = sp.artist(artist_id)
    url = artist['external_urls']['spotify']
    artist_genre = artist['genres']
    image = artist['images'][0]['url']
    name = artist['name']
    return [name, artist_genre, image, url]


def verification(chid):
    username = chid
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
    return util.prompt_for_user_token(username, "user-top-read", client_id=client_id,
                                       client_secret=client_secret, redirect_uri=redirect_uri)


def get_token(username):
    return util.prompt_for_user_token(username, "user-top-read", client_id=client_id,
                                      client_secret=client_secret, redirect_uri=redirect_uri)


def wrapped(username):
    token = get_token(username)

    if token:
        sp = spotipy.Spotify(auth=token)
        top_tracks_short = sp.current_user_top_tracks(limit=100, offset=0, time_range="long_term")
    else:
        print("Can't get token for", username)
        return

    track_ids = get_track_ids(top_tracks_short)

    # Top five tracks
    tracks = [[music['name'], music['artists'][0]['name'], music['album']['name'], music['album']['images'][0]['url']] for music in top_tracks_short["items"]]
    top_musics = pd.DataFrame(tracks, columns=['name', 'artist', 'album', 'album_cover'])

    # Top artists
    artists = [get_artist_features(i, sp) for i in track_ids]
    artists_df = pd.DataFrame(artists, columns=['name', 'artist_genre', 'image', 'url'])
    artists_df['count'] = artists_df.groupby('name')['name'].cumcount() + 1
    top_artists = artists_df.sort_values(by='count', ascending=False).drop(columns='artist_genre').drop_duplicates(subset='name', keep='first')

    # Top genres
    genres = [i for sublist in artists_df['artist_genre'] for i in sublist]
    genres_dict = {i: genres.count(i) for i in genres}
    top_genres = dict(Counter(genres_dict).most_common(5))
    top_genres_chart = pd.DataFrame.from_dict(top_genres, orient='index', columns=['count'])

    img = Image.open('templates/musics2021.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('font/Gotham.ttf', 43)

    gg = 1044
    for i in top_artists.head(5)['name']:
        if len(i) > 16:
            i = i.replace(i[16:], '...')
        draw.text((150, gg + 46), i, (248, 215, 226), font=font)
        gg += 56

    gg = 1044
    for i in top_musics.head(5)['name']:
        if len(i) > 16:
            i = i.replace(i[16:], '...')
        draw.text((640, gg + 46), i, (248, 215, 226), font=font)
        gg += 56

    top_genre = list(top_genres.keys())[0]
    font2 = ImageFont.truetype('font/Gotham.ttf', 55)
    draw.text((560, 1510), top_genre.capitalize(), (248, 215, 226), font=font2)

    artist_image = save_image(list(top_artists.head(5)["image"])[0], "file_name", (600, 600))
    img.paste(artist_image, (245, 182))

    font3 = ImageFont.truetype('font/Gotham.ttf', 40)
    draw.text((400, 1870), "Spotify Wrapped, By Hossein M", (211, 12, 45), font=font3)

    img.save('Spotify-Wrapped.jpg')

    img2 = Image.open('templates/topsongs.jpg')
    draw2 = ImageDraw.Draw(img2)
    font = ImageFont.truetype('font/Gotham.ttf', 45)

    gg = 600
    for i in top_musics.head(5)['name']:
        if len(i) > 16:
            i = i.replace(i[16:], '...')
        draw2.text((500, gg), i, (0, 9, 5), font=font)
        gg += 235

    font = ImageFont.truetype('font/Gotham.ttf', 30)
    gg = 650
    for i in top_musics.head(5)['artist']:
        if len(i) > 16:
            i = i.replace(i[16:], '...')
        draw2.text((500, gg + 30), i, (72, 69, 60), font=font)
        gg += 235

    for i in top_musics.head(5)['album_cover']:
        artist_image = save_image(i, "file_name", (220, 220))
        img2.paste(artist_image, (235, gg + 63))
        gg += 238

    img2.save('Spotify-Wrapped2.jpg')

    img3 = Image.open('templates/topartist.jpg')
    draw3 = ImageDraw.Draw(img3)
    font = ImageFont.truetype('font/Gotham.ttf', 45)

    gg = 630
    for i in top_artists.head(5)['name']:
        if len(i) > 16:
            i = i.replace(i[16:], '...')
        draw3.text((500, gg), i, (35, 50, 109), font=font)
        gg += 235

    gg = 470
    for i in top_artists.head(5)["image"]:
        artist_image = save_image(i, "file_name", (220, 220))
        img3.paste(artist_image, (235, gg + 63))
        gg += 238

    img3.save('Spotify-Wrapped3.jpg')


def save_image(url, filename, size):
    urllib.request.urlretrieve(url, filename)
    artist_image = Image.open(filename)
    artist_image = artist_image.resize(size)
    return artist_image


if __name__ == "__main__":
    username = 'buv1vuw2rxppyefnqhx4aiaie'
    wrapped(username)
