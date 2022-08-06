from dotenv import dotenv_values
from domain.albumProcessor import AlbumProcessor
from contracts.providerException import ProviderException
from providers.fileDataReader import FileDataReader
from providers.spotifyMetadataProvider import SpotifyMetadataProvider
from providers.trelloBoardProvider import TrelloBoardProvider

def main():
    env = dotenv_values()
    data_reader = FileDataReader('discography.txt')
    board_provider = TrelloBoardProvider()
    metadata_provider = SpotifyMetadataProvider()
    print("Welcome to Music-Trello")
    print("Vist: https://developer.spotify.com/dashboard/applications - to setup a Spotify CLIENT_ID and CLIENT_SECRET")
    print("Vist: https://trello.com/app-key - to setup a Trello APP_KEY and AUTH_TOKEN")
    print("Please configure the Providers in .env file")
    print("Current env:", env)
    metadata_provider.login()
    name = input("Please enter the board name:")
    try:
        processor = AlbumProcessor(data_reader, board_provider, metadata_provider)
        board_id = processor.process(name)
        print("Data processes successfully, board created at:", "https://www.trello.com/b/{id}/{name}".format(id = board_id, name = name.lower()))
    except ProviderException as e:
        print("Something whent wrong while connecting to the provider", e)


main()