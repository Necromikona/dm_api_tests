import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMPApiAccount


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

def test_put_v1_account_email():
    dm_api_configuration = Configuration(host='http://5.63.153.31:5051')
    mailhog_configuration = Configuration(host= 'http://5.63.153.31:5025')

    account= DMPApiAccount(configuration=dm_api_configuration)
    mailhog= MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = f'testing_116'
    password = '6789012345'
    email = f"{login}@mail.ru"

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

    account_helper.change_email_for_user(login=login, password=password, email=f'{login}_changed@mail.ru')

    account_helper.user_login_without_activate(login=login, password=password)

    account_helper.activate_token_for_user(login=login)
    account_helper.user_login(login=login, password=password)

