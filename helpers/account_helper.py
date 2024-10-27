import json
from services.dm_api_account import DMPApiAccount
from services.api_mailhog import MailHogApi

class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMPApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Error create User"

        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"Error. E-mail not found for {login}"

        token = self.get_activation_token_by_login(login= login, response= response)
        assert token is not None, f"Not found token for {login}"

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "User not activate"

        return response

    def user_login(self, login:str, password:str, remember_me:bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "User not authorized"
        return response

    def user_login_without_activate(self, login:str, password:str, remember_me:bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, "Authorize user without activate email"
        return response

    def change_email_for_user(self, login:str, password:str, email:str):
        json_data = {
             'login': login,
             'password': password,
             'email' : email
         }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f"Not change email for User {login}"
        return response

    def activate_token_for_user(self, login:str):
        # Получение последних сообщений
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, f"Error. E-mail not found for {login}"

        # Поиск по логину
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Not found token for {login}"

        # Активация нового токена
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "User not activate"
        return response

    @staticmethod
    def get_activation_token_by_login(
            login,
            response
    ):
        token = None
        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                return token