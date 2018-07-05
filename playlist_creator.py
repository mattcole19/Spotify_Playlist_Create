from bs4 import BeautifulSoup
import requests
import os
import spotipy
import spotipy.util as util

'''Scrapes hotnewhiphop top 100 songs then creates and returns list of songs by artists I enjoy
parameters:
    fav_artists - artists I want songs from '''
def getTopSongs(fav_artists):
    songs = []
    return

'''Searches Spotify for song.  If the song is found, the function returns the song id. If the song is not found it returns False
parameters:
    song - song list containing name and artist.  Ex: ["Gooey", "Glass Animals"]'''
def spotifySearch(song):
    song_id = ''
    return song_id

'''Adds song to the corresponding month's playlist.  Returns nothing
parameters:
    id - song id for song to add
    playlist - monthly playlist name that song will be added to'''
def addSong(id, playlist):
    return

def main():
    desired_artists = ['Drake']
    desired_songs = getTopSongs(desired_artists)
    song_ids = []
    master_ids = [] #needs to be separate file to avoid being overwritten
    #create Spotify session
    desired_playlist = '18July'#need function to create playlist / go to desired playlist each month
    for song in desired_songs:
        song_id = spotifySearch(song)
        if song_id:
            song_ids.append(id)
    for song_id in song_ids:
        if song_id not in master_ids:
            addSong(song_id, desired_playlist)
    print('Program complete!')




if __name__ == '__main__':
    main()


'''Pseudocode:
scrape top 100 songs and add song to playlist if artist in desired artists
create spotify session

for song in desired song list:
    search for song on spotify
    if theres a match:
        get song id and add to song_ids list

for song in song_ids:
    add song to playlist
'''