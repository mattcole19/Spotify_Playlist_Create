from bs4 import BeautifulSoup
import requests
import os
import spotipy
import spotipy.util as util
import datetime


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

'''Normalizes song name.  Removes producer name, and other aspects that will affect the song being found on Spotify
parameters:
    songs - list of songs to normalize'''
def normalizeSongs(songs):
    for song in songs:
        song_title = song[0]
        if '(' in song_title:
            index = song_title.find('(')
            song_title = song_title[0: index-1]
        song[0] = song_title
    print("Songs that I want from HotNewHipHop's top 100: ")
    print('--------------------')
    for song in songs:
        print('{} - {}'.format(song[0], song[1]))
    print('--------------------\n')
    return songs

'''Gathers and returns access token to my personal Spotify account
 parameters:
    user - username of account'''
def getToken(user):
    desired_scope = 'playlist-modify-private, playlist-read-private'
    id = os.environ.get('SPOT_CLIENT')
    secret = os.environ.get('SPOT_SECRET')
    uri = 'http://google.com/'

    access_token = util.prompt_for_user_token(username=user, scope=desired_scope, client_id=id, client_secret=secret,
                                       redirect_uri=uri)
    if access_token:
        return access_token
    else:
        print('ERROR obtaining token.')
        return

'''Decides playlist name to add songs to based on month and year.  Returns string in year-month format (ex: 18Nov)'''
def determinePlaylist():
    date = datetime.datetime.now()
    month = date.strftime('%b')
    year = date.strftime('%y')
    playlist_name = year + month
    return playlist_name

'''Searches to see if playlist exists in my Spotify library. Returns True if it does and False otherwise
parameters:
    sp - spotify session
    playlist_name = playlist that is being searched for'''
def playlistExists(sp, playlist_name):
    my_playlists = sp.current_user_playlists()
    for playlist in my_playlists['items']:
        if playlist_name == playlist['name']:
            return True
    return False


'''Creates Spotify playlist for current month
parameters:
    sp - spotify session
    user = username of account
    playlist_name - name of playlist to be created'''
def createPlaylist(sp, user, playlist_name):
    sp.user_playlist_create(user, playlist_name, public= False)
    print('New playlist, {}, created'.format(playlist_name))
    return

'''Obtains and returns desired playlist's id.
parameters:
    sp - spotify session
    user - username of account
    playlist_name - name of playlist to get id for'''
def getPlaylistID(sp, user, playlist_name):
    playlists = sp.user_playlists(user)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            id = playlist['id']
    return id

'''Searches Spotify for song.  If the song is found, the function returns the song id. If the song is not found it returns False
parameters:
    sp - spotify session
    song - song list containing name and artist.  Ex: ["Gooey", "Glass Animals"]'''
def spotifySearch(sp, song):
    tracks = []
    title, wanted_artist = song[0], song[1]
    query = '{} - {}'.format(title, wanted_artist)
    search_query = sp.search(query, type='track')
    for result in search_query['tracks']['items']:
        tracks.append(result['external_urls'])
    if not tracks:
        print('{} - {}'.format(song[0], song[1]))
        return
    track = tracks[0]
    wanted_track = track['spotify']
    link, song_id = wanted_track.split('https://open.spotify.com/track/')
    return song_id

'''Gathers and returns list of ids in master_ids
parameters:
    path - path of file being read'''
def readFile(path):
    contents = ''
    with open(path) as file:
        ids = file.read()
        file.close()
    contents = ids.split('\n')
    return contents

'''Writes ids to master_ids file
parameters:
    path - path of file to write to 
    id - song id to add'''
def writeToFile(path, id):
    with open(path, 'a+') as file:
        file.write(id)
        file.write('\n')
    return

'''Adds song to the corresponding month's playlist.  Returns nothing
parameters:
    sp - spotify session
    user - username of account
    id - song id for song to add
    playlist - monthly playlist name that song will be added to'''
def addSong(sp, user, id, playListID):
    track_uri = [id]
    print(track_uri)
    sp.user_playlist_add_tracks(user, playListID, track_uri)
    return


def main():
    desired_artists = ['Drake', 'Nav', 'Machine Gun Kelly', 'A$AP Rocky', 'NF', 'Post Malone', 'Chance The Rapper', 'J. Cole', 'Juice WRLD',
                       'Kanye West', 'Kid Cudi', 'Kendrick Lamar', 'Lil Uzi Vert', 'Russ', 'B.o.B', 'Lil Dicky', 'Chris Webby', 'Eminem',
                       'Travis Scott', 'Flatbush Zombies', 'Logic', 'Trippie Redd', 'Vic Mensa', 'Young Thug', 'Mac Miller']
    username = 'ccmatt19'
    file_path = '/Users/mattcole/Desktop/Spotify_Playlist_Creator/master_ids.txt'
    desired_songs = getTopSongs(desired_artists)
    songs = normalizeSongs(desired_songs)
    song_ids = []
    missing_ids = []
    token = getToken(username)
    session = spotipy.Spotify(auth=token)
    desired_playlist = determinePlaylist()
    if not playlistExists(session, desired_playlist):
        createPlaylist(session, username, desired_playlist)
        print()
    playlistID = getPlaylistID(session, username, desired_playlist)
    print('Songs not found on Spotify: ')
    print('---------------------------')
    for song in desired_songs:
        song_id = spotifySearch(session, song)
        if song_id:
            song_ids.append(song_id)
    master_file_contents = readFile(file_path)
    for song_id in song_ids:
        if song_id not in master_file_contents:
            addSong(session, username, song_id, playlistID)
            writeToFile(file_path, song_id)

    print('\nPROGRAM COMPLETE! ')


if __name__ == '__main__':
    main()
