


from abc import ABC, abstractmethod
from domain.album import Album


class AbsBoardProvider(ABC):

    @abstractmethod
    def create_board(self, name:str) -> str:
        pass

    @abstractmethod
    def create_list(self, board_id:str, decade:int) -> str:
        pass

    @abstractmethod
    def create_card(self, list_id:str, card_name:str) -> str:
        pass

    @abstractmethod
    def set_card_cover(self, card_id:str, cover:str) -> None:
        pass