import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import numpy as np
import pandas as pd
# These are the 3 global variables that we use in order to authenticate
# our developer profile and create the application
# Spotify sri$ export SPOTIFY_CLIENT_ID='ebe19929449c48ce86dc1057305e44fb'
# Srivenkats-MacBook-Pro:Spotify sri$ export SPOTIFY_CLIENT_SECRET='f6aabd7858264c1994805ccd808ab2ac'
# Srivenkats-MacBook-Pro:Spotify sri$ export SPOTIFY_REDIRECT_URI='http://google.com/''

# These two statements set our first argument within the command line to be
# the username for authentication and the scope allows us to access many different
# parts of the web api
argument = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
'user-read-recently-played user-library-read user-read-private user-library-modify'
'playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative'
'user-top-read user-read-email user-read-birthday streaming user-follow-modify'
'user-follow-read'
#username: wdjsq1q71u0i8nsx3eqnone2e?si=t8ViKBnlRxWM1Ckt8AuJGQ

# Erase cache and prompt for user permission

try:
    token = util.prompt_for_user_token(argument, scope, 'ebe19929449c48ce86dc1057305e44fb', 'f6aabd7858264c1994805ccd808ab2ac', 'http://google.com/')
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(argument, scope)

spotifyObject = spotipy.Spotify(auth = token)


# user is json object that prints out the data for the username given
user = spotifyObject.current_user()

# In this section I will be trying to retrieve each track from each one of my playlists
# And find the audio features for them
track_ids = []
user_playlists = spotifyObject.current_user_playlists()
user_playlists_info = user_playlists["items"]
playlist_ids = []
playlist_names = []
for item in user_playlists_info:
    playlist_ids.append(item["id"])
    playlist_names.append(item["name"])
print(playlist_ids)

# Attempt to return a dictionary of dictionaries that has the track_id, artist, and popularity
def track_stuffer(track_ids):
    id_list = []
    artist_list = []
    popularity_list = []
    big_list = []
    big_dict = {}
    for i in range(len(track_ids)):
        track = spotifyObject.track(track_ids[i])
        id_list.append(track["id"])
        artist_list.append(track["album"]["artists"][0]["name"])
        popularity_list.append(track["popularity"])
    for j in range(len(id_list)):
        big_dict[j] = {}
        big_dict[j]["id"] = id_list[j]
        big_dict[j]["artist"] = artist_list[j]
        big_dict[j]["popularity"] = popularity_list[j]
    return big_dict

playlist_namelist = []
track_stuff_namelist = []
for item in range(len(playlist_ids)):
    print(playlist_ids[item])
    tracks_on_playlist = spotifyObject.user_playlist_tracks(argument,playlist_ids[item])
    tracks_on_playlist_info = tracks_on_playlist["items"]
    track_ids = []
    for track in tracks_on_playlist_info:
        track_ids.append(track["track"]["id"])
    if len(track_ids) >= 20:
        song_features = spotifyObject.audio_features(track_ids)
        # print(json.dumps(song_features[:2], sort_keys = True, indent = 4))
        # track_stuffs = track_stuffer(track_ids)
        # print(track_stuffs)
        big_dict = track_stuffer(track_ids)
        with open(str(playlist_names[item]) +"track_stuff.json",'w') as outfile:
            json.dump(big_dict,outfile)
        track_stuff_namelist.append(str(playlist_names[item]) +"track_stuff.json")
        with open(str(playlist_names[item])+".json",'w') as outfile:
            json.dump(song_features,outfile)
        print(len(track_ids))
        playlist_namelist.append(str(playlist_names[item] + ".json"))
# wdjsq1q71u0i8nsx3eqnone2e?si=O4bxobCISdmbnP1cj_S-bw"""
# "wdjsq1q71u0i8nsx3eqnone2e"
