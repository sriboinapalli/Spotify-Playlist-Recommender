import os
import sys
import json
import spotipy
import spotipy.util as util
import csv
from json.decoder import JSONDecodeError
def playlist_id_gatherer(spotifyobject):
    big_list = []
    user_playlists = spotifyobject.current_user_playlists()
    user_playlists_info = user_playlists["items"]
    playlist_ids = []
    playlist_names = []
    for item in user_playlists_info:
        playlist_ids.append(item["id"])
        playlist_names.append(item["name"])
        big_list.append([item["name"], item["id"]])
    return big_list

# This function takes in the list of lists that you have as a result of checks
# to see how many tracks are in the playlist, if there are less than 30 tracks
# in the playlist that item is removed from the list
def data_slimmer(username, playlist_names_ids, spotifyobject):
    final_list = []
    for item in playlist_names_ids:
        tracks_on_playlist = spotifyobject.user_playlist_tracks(username, item[1])
        playlist_length = tracks_on_playlist["total"]
        if playlist_length > 30:
            final_list.append(item)
    return final_list

# This function takes in the revised list of lists outputted by the previous function
# and will output a dictionary where every dict has a song's id as the key, and the playlist that a
# song belongs to, its popularity and its artist
def track_id_retriever(username, input_data, spotifyobject):
    track_id_list = []
    for item in input_data:
        tracks_info = spotifyobject.user_playlist_tracks(username, item[1])["items"]
        for track in tracks_info:
            song_list = []
            song_list.append(track["track"]["id"])
            song_list.append(track["track"]["popularity"])
            song_list.append(track["track"]["artists"][0]["name"])
            song_list.append(item[0])
            track_id_list.append(song_list)
    return track_id_list


# This function will take in the dictionary created in the last function and output a JSON file
# of song features and another file that we will compile in data analysis that includes
# a song's playlist, popularity, and artist
def song_features_creator(input_list_of_lists, spotifyobject):
    track_playlists_biglist = []
    input_len = len(input_list_of_lists)
    id_list1 = []
    id_list2 = []
    id_list3 = []
    id_list4 = []
    for item1 in input_list_of_lists[:(input_len//4)]:
        id_list1.append(item1[0])
    for item2 in input_list_of_lists[(input_len//4):(2*input_len//4)]:
        id_list2.append(item2[0])
    for item3 in input_list_of_lists[(2 * input_len//4):(3 * input_len//4)]:
        id_list3.append(item3[0])
    for item4 in input_list_of_lists[(3 * input_len//4):]:
        id_list4.append(item4[0])
    track_features1 = spotifyobject.audio_features(id_list1)
    for i in range(len(track_features1)):
        track_features1[i]["popularity"] = input_list_of_lists[i][1]
        track_features1[i]["main_artist"] = input_list_of_lists[i][2]
        track_features1[i]["playlist"] = input_list_of_lists[i][3]
    track_features2 = spotifyobject.audio_features(id_list2)
    for j in range(len(track_features2)):
        track_features2[j]["popularity"] = input_list_of_lists[input_len//4 + j][1]
        track_features2[j]["main_artist"] = input_list_of_lists[input_len//4 + j][2]
        track_features2[j]["playlist"] = input_list_of_lists[input_len//4 + j][3]
    track_features3 = spotifyobject.audio_features(id_list3)
    for k in range(len(track_features3)):
        track_features3[k]["popularity"] = input_list_of_lists[(2* input_len//4) + k][1]
        track_features3[k]["main_artist"] = input_list_of_lists[(2* input_len//4) + k][2]
        track_features3[k]["playlist"] = input_list_of_lists[(2* input_len//4) + k][3]
    track_features4 = spotifyobject.audio_features(id_list4)
    for l in range(len(track_features4)):
        track_features4[l]["popularity"] = input_list_of_lists[(3* input_len//4) +l][1]
        track_features4[l]["main_artist"] = input_list_of_lists[(3* input_len//4) +l][2]
        track_features4[l]["playlist"] = input_list_of_lists[(3* input_len//4) +l][3]
    track_playlists_biglist.append(track_features1)
    track_playlists_biglist.append(track_features2)
    track_playlists_biglist.append(track_features3)
    track_playlists_biglist.append(track_features4)
    return track_playlists_biglist

# This final function will write all of the song metrics to a csv file. It takes in a
# List of 4 dictionaries and iterates through them, the keys will be the keys to each
# dictionary object, and the rest of the values will be written into a csv file
def csv_writer(dictionary):
    biglist = []
    for item in dictionary:
        for feature in item:
            biglist.append(feature)
            fieldnames = feature.keys()
    with open('all_tracks.csv' , 'w') as fout:
        csvout = csv.DictWriter(fout, fieldnames = fieldnames)
        csvout.writeheader()
        csvout.writerows(biglist)



def main(spotifyObject):
    list_of_lists = playlist_id_gatherer(spotifyObject)
    revised_list_of_lists = data_slimmer(argument, list_of_lists, spotifyObject)
    track_info = track_id_retriever(argument, revised_list_of_lists, spotifyObject)
    tracks_playlist_biglist = song_features_creator(track_info,spotifyObject)
    csv_writer(tracks_playlist_biglist)
if __name__ == "__main__":
    # These are the 3 global variables that we use in order to authenticate
    # our developer profile and create the application
    # Spotify sri$ export SPOTIFY_CLIENT_ID='ebe19929449c48ce86dc1057305e44fb'
    # Srivenkats-MacBook-Pro:Spotify sri$ export SPOTIFY_CLIENT_SECRET='f6aabd7858264c1994805ccd808ab2ac'
    # Srivenkats-MacBook-Pro:Spotify sri$ export SPOTIFY_REDIRECT_URI='http://google.com/''

    # These two statements set our first argument within the command line to be
    # the username for authentication and the scope allows us to access many different
    # parts of the web api
    #username: wdjsq1q71u0i8nsx3eqnone2e?si=t8ViKBnlRxWM1Ckt8AuJGQ
    if len(sys.argv) > 2:
        argument = sys.argv[1]
    else:
        # I'm hardcoding in my user id for the sake of this project but this code should work
        # if you put in a keyword argument
        argument = "wdjsq1q71u0i8nsx3eqnone2e"
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    'user-read-recently-played user-library-read user-read-private user-library-modify'
    'playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative'
    'user-top-read user-read-email user-read-birthday streaming user-follow-modify'
    'user-follow-read'

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(argument, scope, 'ebe19929449c48ce86dc1057305e44fb', 'f6aabd7858264c1994805ccd808ab2ac', 'http://google.com/')
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(argument, scope)

    spotifyObject = spotipy.Spotify(auth = token)

    main(spotifyObject)
# wdjsq1q71u0i8nsx3eqnone2e?si=O4bxobCISdmbnP1cj_S-bw"""
# "wdjsq1q71u0i8nsx3eqnone2e"
