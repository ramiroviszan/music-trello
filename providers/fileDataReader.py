



from contracts.absAlbumDataProvider import AbsAlbumDataProvider
from domain.album import Album


class FileDataReader(AbsAlbumDataProvider):

    def __init__(self, path:str):
        self.path = path

    def open(self) -> None:
        self.file = open(self.path, 'r')

    def next_record(self) -> Album:
        line = self.file.readline()
        if line:
            split = line.split(" ", 1)
            year = int(split[0])
            name = split[1]
            return Album(year, name)
        else:
            return None

    def close(self) -> None:
        self.file.close()