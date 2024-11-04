import json

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DMPApiAccount
from services.api_mailhog import MailHogApi

from dm_api_account.models.login_credentials import LoginCredentials

from retrying import retry


def retry_if_result_none(
        result
):
    return result is None

class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMPApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login:str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials= LoginCredentials(login=login, password=password, rememberMe=True),
            validate_response=False
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def change_password(
            self,
            login: str,
            email: str,
            oldPassword: str,
            newPassword: str
    ):
        reset_password = ResetPassword(
            login=login,
            email=email,
        )
        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

        token = self.get_activation_token_by_login(login=login, find_URI=True)

        change_password = ChangePassword(
            login=login,
            token=token,
            oldPassword=oldPassword,
            newPassword=newPassword,
        )
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            email=email,
            password=password,
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)

        token = self.get_activation_token_by_login(login= login)

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)

        return response

    def user_login(self, login:str, password:str, remember_me:bool = True, validate_response = False):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            rememberMe=remember_me,
        )
        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials, validate_response=validate_response)
        return response

    def user_login_without_activate(self, login:str, password:str, remember_me:bool = True):
        login_credentials=LoginCredentials(
            login=login,
            password=password,
            rememberMe=remember_me,
        )
        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials, validate_response=False)
        return response

    def change_email_for_user(self, login:str, password:str, email:str):
        change_email = ChangeEmail(
             login=login,
             password=password,
             email=email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        return response

    def activate_token_for_user(self, login:str):
        # Поиск по логину
        token = self.get_activation_token_by_login(login=login)

        # Активация нового токена
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    @retry(stop_max_attempt_number=5,retry_on_result=retry_if_result_none, wait_fixed = 1000)
    def get_activation_token_by_login(
            self,
            login,
            find_URI = False,
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                if find_URI:
                    token = user_data['ConfirmationLinkUri'].split('/')[-1]
                else:
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                return token
