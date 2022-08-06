import requests
from contracts.absBoardProvider import AbsBoardProvider
from contracts.providerException import ProviderException
from dotenv import dotenv_values

env = dotenv_values()
create_board_url = "https://api.trello.com/1/boards/?name={board_name}&defaultLists=false"
create_list_url = "https://api.trello.com/1/lists?name={list_name}&idBoard={board_id}"
create_card_url = "https://api.trello.com/1/cards?name={card_name}&idList={list_id}"
set_card_cover_attachment = "https://api.trello.com/1/cards/{card_id}/attachments?name=Cover&url={cover_url}&setCover=true"
trello_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "OAuth oauth_consumer_key=\"{api_key}\", oauth_token=\"{app_token}\"".format(api_key=env["TRELLO_API_KEY"], app_token=env["TRELLO_AUTH_TOKEN"])
}
AUTH_CODE_ERROR = 401

class TrelloBoardProvider(AbsBoardProvider):

    def create_board(self, name:str) -> str:
        try:
            response = requests.post(create_board_url.format(board_name = name), headers=trello_headers)
            return response.json()["id"]
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)

    def create_list(self, board_id:str, decade:int) -> str:
        try:
            response = requests.post(create_list_url.format(list_name = decade, board_id = board_id), headers=trello_headers)
            return response.json()["id"]
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)

    def create_card(self, list_id:str, card_name:str) -> str:
        try:
            response = requests.post(create_card_url.format(card_name=card_name, list_id = list_id), headers=trello_headers)
            return response.json()["id"]
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)

    def set_card_cover(self, card_id:str, cover:str) -> None:
        try:
            response = requests.post(set_card_cover_attachment.format(card_id=card_id, cover_url=cover), headers=trello_headers)
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)