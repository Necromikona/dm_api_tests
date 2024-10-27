import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMPApiAccount


def test_put_v1_account_token():
    dm_api_configuration = Configuration(host='http://5.63.153.31:5051')
    mailhog_configuration = Configuration(host= 'http://5.63.153.31:5025')

    account = DMPApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = f'testing_113'
    password = '6789012345'
    email = f"{login}@mail.ru"

    account_helper.register_new_user(login=login, password=password, email=email)