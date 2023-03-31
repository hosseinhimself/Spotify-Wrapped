import json
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'client_id' #insert your client id
client_secret = 'client_secret' # insert your client secret id here

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

aDict = sp.playlist("spotify:playlist:xxxxxxxx")
jsonString = json.dumps(aDict)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()