import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to read links from a file and process them
def process_spotify_links(file_path, encoding="utf-8-sig"):
    with open(file_path, 'r', encoding=encoding) as file:
        links = [line.strip() for line in file if line.strip()]
    return links


# Function to follow playlists or artists
def follow_spotify_links(sp, links):
    for link in links:
        if 'artist' in link:
            artist_id = link.split("artist/")[-1].split("?")[0]
            try:
                sp.user_follow_artists([artist_id])
                print(f"Followed artist: {link}")
            except Exception as e:
                print(f"Failed to follow artist {link}: {e}")

        elif 'playlist' in link:
            playlist_id = link.split("playlist/")[-1].split("?")[0]
            try:
                sp.current_user_follow_playlist(playlist_id)
                print(f"Followed playlist: {link}")
            except Exception as e:
                print(f"Failed to follow playlist {link}: {e}")
        else:
            print(f"Invalid Spotify link: {link}")

if __name__ == "__main__":
    # Prompt the user for input
    file_path = input("Enter the path to the file containing Spotify links: ")

    # Spotify API credentials setup
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=input("Enter the client id: ") ,
        client_secret=input("Enter the client secret id: "),
        redirect_uri=input("Enter the redirect url: "),
        scope="user-follow-modify playlist-modify-public"
    ))

    # Process the file and follow links
    spotify_links = process_spotify_links(file_path)
    follow_spotify_links(sp, spotify_links)
