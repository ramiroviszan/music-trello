import requests
from contracts.absAlbumMetadataProvider import AbsAlbumMetadataProvider
from contracts.providerException import ProviderException
from dotenv import dotenv_values

env = dotenv_values()
spotify_auth_url = "https://accounts.spotify.com/api/token"
spotify_auth_headers = {
    "grant_type": 'client_credentials',
    "client_id": env["SPOTIFY_CLIENT_ID"],
    "client_secret": env["SPOTIFY_CLIENT_SECRET"],
}
spotify_search_url = "https://api.spotify.com/v1/search?q={search_text}&type=album&market=ES&limit=1&offset=0"
spotify_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer {token}"
}

AUTH_CODE_ERROR = 401


class SpotifyMetadataProvider(AbsAlbumMetadataProvider):

    def login(self) -> None:
        try:
            response = requests.post(spotify_auth_url, spotify_auth_headers)
            self.token = response.json()["access_token"]
            spotify_headers["Authorization"] = spotify_headers["Authorization"].format(token = self.token)
        except Exception as e:
            print("401 - Spotify Login Failed -", response.json())
            raise ProviderException(e)

    def get_album_cover_url(self, name:str) -> str:
        try:
            response = requests.get(spotify_search_url.format(search_text = name), headers=spotify_headers)
            cover_url = response.json()["albums"]["items"][0]["images"][0]["url"]
            return cover_url
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Spotify Auth Failed -", response.json())
                raise ProviderException(e)
            return None

   