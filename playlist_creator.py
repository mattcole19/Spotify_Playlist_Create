from bs4 import BeautifulSoup
import requests
import os
import spotipy
import spotipy.util as util


'''Scrapes hotnewhiphop top 100 songs then creates and returns list of songs by artists I enjoy
parameters:
    fav_artists - artists I want songs from '''
def getTopSongs(fav_artists):
    artists = []
    song_titles = []
    songs = []
    url = 'https://www.hotnewhiphop.com/top100/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    for song in soup.find_all('div', class_='chartItem-body-artist'):
        song_title = song.a.text.strip()
        for artist in song.find('strong', class_='chartItem-artist-artistName'):
            if artist in fav_artists:
                songs.append([song_title, artist])
    return songs

'''Normalizes song name.  Removes producer name, and other aspects that will effect the song being found on Spotify
parameters:
    songs - list of songs to normalize'''
def normalizeSongs(songs):
    for song in songs:
        song_title = song[0]
        if '(' in song_title:
            index = song_title.find('(')
            song_title = song_title[0: index-1]
        song[0] = song_title
    print(songs, "\n")
    return songs

'''Gathers and returns access token to my Spotify account '''
def getToken():
    user = 'ccmatt19'
    desired_scope = 'playlist-modify-private'
    id = os.environ.get('SPOT_CLIENT')
    secret = os.environ.get('SPOT_SECRET')
    uri = 'http://google.com/'

    access_token = util.prompt_for_user_token(username=user, scope=desired_scope, client_id=id, client_secret=secret,
                                       redirect_uri=uri)
    if access_token:
        print('Token gathered successfully')
        return access_token
    else:
        print('Error obtaining token.')
        return

'''Searches Spotify for song.  If the song is found, the function returns the song id. If the song is not found it returns False
parameters:
    sp - spotify session
    song - song list containing name and artist.  Ex: ["Gooey", "Glass Animals"]'''
def spotifySearch(sp, song):
    song_id = ''
    return song_id

'''Adds song to the corresponding month's playlist.  Returns nothing
parameters:
    sp - spotify session
    id - song id for song to add
    playlist - monthly playlist name that song will be added to'''
def addSong(sp, id, playlist):
    return


def main():
    desired_artists = ['Drake']
    desired_songs = getTopSongs(desired_artists)
    songs = normalizeSongs(desired_songs)
    song_ids = []
    master_ids = [] #needs to be separate file to avoid being overwritten
    #create Spotify session
    token = getToken()
    session = spotipy.Spotify(auth=token)
    desired_playlist = '18July' #need function to create playlist / go to desired playlist each month
    for song in desired_songs:
        song_id = spotifySearch(session, song)
        if song_id:
            song_ids.append(id)
    for song_id in song_ids:
        if song_id not in master_ids:
            addSong(session, song_id, desired_playlist)
    print('\nProgram complete!')


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