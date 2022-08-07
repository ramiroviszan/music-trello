from email import header
import requests
from dotenv import dotenv_values
from requests_oauthlib import OAuth1Session, OAuth1

from contracts.absBoardProvider import AbsBoardProvider
from contracts.providerException import ProviderException  

env = dotenv_values()
create_organization_url = "https://api.trello.com/1/organizations?displayName={name}"
create_board_url = "https://api.trello.com/1/boards?name={board_name}&organizationId={organization_id}&defaultLists=false"
create_list_url = "https://api.trello.com/1/lists?name={list_name}&idBoard={board_id}"
create_card_url = "https://api.trello.com/1/cards?name={card_name}&idList={list_id}"
set_card_cover_attachment = "https://api.trello.com/1/cards/{card_id}/attachments?name=Cover&url={cover_url}&setCover=true"
trello_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "OAuth oauth_consumer_key=\"{api_key}\", oauth_token=\"{app_token}\"" 
}
client_key = env["TRELLO_API_KEY"]
client_secret = env["TRELLO_CLIENT_SECRET"]
trello_auth_request_url = "https://trello.com/1/OAuthGetRequestToken"
trello_authorize_url = "https://trello.com/1/OAuthAuthorizeToken"
trello_access_url = "https://trello.com/1/OAuthGetAccessToken"
AUTH_CODE_ERROR = 401

class TrelloBoardProvider(AbsBoardProvider):

    def create_board(self, name:str) -> str:
        try:
            response = requests.post(
                create_board_url.format(
                    board_name = name, 
                    organization_id=self.organization_id
                ), 
                headers=self.headers
            )
            return response.json()["id"]
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)

    def create_list(self, board_id:str, decade:int) -> str:
        try:
            response = requests.post(
                create_list_url.format(
                    list_name = decade,
                    board_id = board_id
                ), 
                headers=self.headers
            )
            return response.json()["id"]
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)

    def create_card(self, list_id:str, card_name:str) -> str:
        try:
            response = requests.post(
                create_card_url.format(
                    card_name=card_name, 
                    list_id = list_id
                ), 
                headers=self.headers
            )
            return response.json()["id"]
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)

    def set_card_cover(self, card_id:str, cover:str) -> None:
        try:
            response = requests.post(
                set_card_cover_attachment.format(
                    card_id=card_id, 
                    cover_url=cover
                ), 
                headers=self.headers
            )
        except Exception as e:
            if(response.status_code == AUTH_CODE_ERROR):
                print("401 - Trello Auth Failed" )
            raise ProviderException(e)


    def login(self):
        try:
            print("Trello Setup Started...\n")

            oauth = self._get_auth_token()
            self._redirect_get_auth(oauth)
            token = input("\nPaste Trello's token here: ")
            self._create_headers(token)
            print("Trello Login Completed!\n")

            name = input("Please enter your Organization's name: ")
            self._create_organization(name)

            print("Trello Setup Completed!\n")
        except Exception as e:
            print("Trello Setup Failed\n")
            raise ProviderException(e)

    def _get_auth_token(self):
        oauth = OAuth1Session(client_key, client_secret=client_secret)
        oauth.fetch_request_token(trello_auth_request_url)
        return oauth

    def _redirect_get_auth(self, oauth):
        app_name = "Music-Trello"
        scope = "read,write"
        expiration = "1day"
        response_type="token"

        authorization_url = oauth.authorization_url(trello_authorize_url)
        print("Please click here to authorize,", 
                "{authorization_url}&scope={scope}&expiration={expiration}&name={app_name}&response_type={response_type}".format(
                    authorization_url=authorization_url,
                    expiration=expiration,
                    scope=scope,
                    app_name=app_name,
                    response_type=response_type
                )
            )

    def _create_headers(self, token):
        self.headers = trello_headers.copy()
        self.headers["Authorization"] = self.headers["Authorization"].format(
            api_key=client_key, 
            app_token=token
        )

    def _create_organization(self, organization_name):
        response = requests.post(
            create_organization_url.format(name= organization_name), 
            headers=self.headers
        )
        self.organization_id = response.json()["id"]
        print("Trello Organization created successfully.\n")
