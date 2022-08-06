from abc import ABC, abstractmethod

class AbsAlbumMetadataProvider(ABC):

    @abstractmethod
    def get_album_cover_url(self, name:str) -> str:
        pass