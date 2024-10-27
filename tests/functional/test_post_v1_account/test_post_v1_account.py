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


def test_post_v1_account():
    dm_api_configuration = Configuration(host= 'http://5.63.153.31:5051')
    mailhog_configuration = Configuration(host='http://5.63.153.31:5025')

    mailhog = MailHogApi(configuration=mailhog_configuration)
    account= DMPApiAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = f'testing_129'
    password = '6789012345'
    email = f"{login}@mail.ru"

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    account_helper.dm_account_api.account_api.post_v1_account(json_data=json_data)


