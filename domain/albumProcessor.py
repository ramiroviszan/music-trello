from contracts.absAlbumDataProvider import AbsAlbumDataProvider
from contracts.absAlbumMetadataProvider import AbsAlbumMetadataProvider
from contracts.absBoardProvider import AbsBoardProvider
from domain.album import Album
from utils.utils import insert_sorted


class AlbumProcessor:

    def __init__(self, data_provider:AbsAlbumDataProvider, board_provider:AbsBoardProvider, metadata_provider:AbsAlbumMetadataProvider ) -> None:
        self.data_provider = data_provider
        self.board_provider = board_provider
        self.metadata_provider = metadata_provider

    def process(self, board_name:str) -> str:
        self.albums_by_decade = self.get_albums_by_decade()
        self.decades = self.get_sorted_decades()
        self.board_id = self.board_provider.create_board(board_name)
        self.create_lists_with_cards()
        return self.board_id

    def get_albums_by_decade(self) -> dict:
        albums_by_decade = {}
        self.data_provider.open()
        album = self.data_provider.next_record()
        while album:
            decade = album.decade
            if decade not in albums_by_decade.keys():
                albums_by_decade[decade] = [album]
            else:
                albums_by_decade[decade] = insert_sorted(albums_by_decade[decade], album)
            album = self.data_provider.next_record()
        self.data_provider.close()
        return albums_by_decade

    def get_sorted_decades(self) -> list:
        decades = list(self.albums_by_decade.keys())
        decades.sort()
        return decades

    def create_lists_with_cards(self) -> None:
        for decade in self.decades:
            print("\n\nProcessing decade: ", decade)
            albums = self.albums_by_decade[decade]
            list_id = self.board_provider.create_list(self.board_id, decade)
            for album in albums:
                print("Album: ", album)
                card_id = self.board_provider.create_card(list_id, card_name="{0} - {1}".format(album.year, album.name))
                self.create_cover(card_id, album)

    def create_cover(self, card_id:str, album:Album) -> None:
        cover = self.metadata_provider.get_album_cover_url(album.name)
        if cover:
            self.board_provider.set_card_cover(card_id, cover)
