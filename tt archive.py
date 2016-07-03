#! python3.5
# tt archive.py - Uses Spotipy to backup Spotify Throwback Thursday playlists

import sys
import os
import pprint
import datetime
import spotipy
import spotipy.util as util

user = 'paralysedbeaver' # Current users username. TODO: Ask user for their username
scope = 'playlist-modify-public' # Scope required to create/edit playlists
token = util.prompt_for_user_token(user, scope) # Get token

# Explicit statement of playlists wanted
# TODO: Ask the user for the playlist they want to copy
playlists = {'spotify': '4ORiMCgOe6UxBDqW8SF1Lm',
             'spotify_uk_': '3fFwkB1IzcZlvYZEuiDzUU'}

# Helper function to print all tracks in a playlist including artist(s)
def display_playlist_tracks(pl):
    print('Playlist Name: ' + pl['name'])
    print()
    for i in pl['tracks']['items']:
        trackname = i['track']['name']
        artist = [k['name'] for k in i['track']['artists']]
        artist = ' and '.join(artist)
        print(trackname + ' by ' + artist)
    print('Total Tracks: ' + str(pl['tracks']['total']))
    print()

# Function to create empty playlist, if it doesn't already exist
# Requires the username, source playlist ID, and new name for the playlist
def empty_dup(src_user, src_pl, name):
    global user_pls
    if name not in [i['name'] for i in user_pls['items']]:
        print('Creating empty playlist with name: %s' % (name))
        sp.user_playlist_create(user,name)
        user_pls = sp.user_playlists(user)

# Function to create the name of the archived playlist
# Requires playlist dictionary
def pl_name(pl):
    date = pl['tracks']['items'][0]['added_at']
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    if date.weekday() > 3 or date.weekday() < 3:
        date += datetime.timedelta(3 - date.weekday())
    date = date.strftime('%d-%m-%Y')
    title = pl['name']
    owner = pl['owner']['id'][0].upper() + pl['owner']['id'][1:]
    name = owner + ' ' + title + ' ' + date 
    return name

# Returns a list of track ID's containing all the tracks in the source playlist
def tracks(pl):
    return [i['track']['id'] for i in pl['tracks']['items']]

# Return the playlist ID of the newly created playlist, needed to add tracks to it
def plid(name, pls):
    return ''.join([i['id'] for i in pls['items'] if i['name'] == name])

# Requires source playlist, new name of the playlist, and playlist dictionary containing all of users playlists.
def add_tracks(pl, name, pls):
    track_list = tracks(pl)
    pl_id = plid(name, pls)
    print('Adding tracks to empty playlist...')
    sp.user_playlist_add_tracks(user, pl_id, track_list)

if token:
    sp = spotipy.Spotify(auth = token)
    user_pls = sp.user_playlists(user)
    for k, v in playlists.items():
        playlist = sp.user_playlist(k, v)
        name = pl_name(playlist)
        empty_dup(k, v, name)
        if len(tracks(sp.user_playlist(user, plid(name,user_pls)))) == 0:
            add_tracks(playlist, name, user_pls)
else:
    print("Can't get token for", username)
