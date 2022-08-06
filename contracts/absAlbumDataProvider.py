from abc import ABC, abstractmethod
from domain.album import Album


class AbsAlbumDataProvider(ABC):

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def next_record(self) -> Album:
        pass

    @abstractmethod
    def close(self) -> None:
        pass