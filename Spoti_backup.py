import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to get all playlists of a user
def get_playlists(sp: spotipy.Spotify, user_id):
    playlists = []
    results = sp.user_playlists(user_id)

    while results:
        playlists.extend(results['items'])
        results = sp.next(results) if results['next'] else None

    return playlists

# Function to get artists followed by the user
def get_followed_artists(sp: spotipy.Spotify):
    artists = []
    results = sp.current_user_followed_artists(limit=20)

    while results:
        artists.extend(results['artists']['items'])
        results = sp.next(results['artists']) if results['artists']['next'] else None

    return artists

# Save playlist links and followed artists to a .txt file
def save_playlist_links_and_artists(client_id, client_secret, redirect_uri, user_id, output_file):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-read-private user-follow-read"
    ))

    playlists = get_playlists(sp, user_id)
    artists = get_followed_artists(sp)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Playlists:\n")
        for playlist in playlists:
            title = playlist["name"]
            playlist_id = playlist["id"]
            playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
            f.write(f"{title}: {playlist_url}\n")

        f.write("\nFollowed Artists:\n")
        for artist in artists:
            f.write(f"{artist['name']}: {artist['external_urls']['spotify']}\n")

    print(f"Saved {len(playlists)} playlist links and {len(artists)} followed artists to {output_file}")

# Save liked songs to a playlist
def save_liked_songs_to_playlist(client_id, client_secret, redirect_uri, user_id, playlist_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-read-private user-follow-read user-library-read playlist-modify-private"

    ))

    # Get liked songs
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)

    while results:
        liked_songs.extend(results['items'])
        results = sp.next(results) if results['next'] else None

    # Create a new playlist
    new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_id = new_playlist['id']

    # Add songs to the new playlist
    track_uris = [item['track']['uri'] for item in liked_songs]
    for i in range(0, len(track_uris), 100):  # Add tracks in batches of 100 (API limit)
        sp.playlist_add_items(playlist_id, track_uris[i:i+100])

    print(f"Saved {len(liked_songs)} liked songs to playlist '{playlist_name}'")

if __name__ == "__main__":
    # Replace these with your Spotify app credentials and user ID
    #you have to create an app from https://developer.spotify.com/dashboard and put client pulic id,client secret id and redirect url from there to here
    CLIENT_ID=input("Enter the client id: ") ,
    CLIENT_SECRET=input("Enter the client secret id: "),
    REDIRECT_URI=input("Enter the redirect url: ")
    USER_ID = input("go to your profile,paste things after /user/ (i mean https://open.spotify.com/user/*----HERE----*)")
    OUTPUT_FILED = input("enter the name you want for your list")
    OUTPUT_FILE = OUTPUT_FILED + ".txt"
    PLAYLIST_NAMED = input("enter the name you want for your liked playlist")#backup of your liked songs,you can change the name
    PLAYLIST_NAME = PLAYLIST_NAMED + ".txt"
    
    save_liked_songs_to_playlist(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USER_ID, PLAYLIST_NAME)
    save_playlist_links_and_artists(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USER_ID, OUTPUT_FILE)