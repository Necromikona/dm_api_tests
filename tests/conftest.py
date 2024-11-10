from collections import namedtuple
from datetime import datetime
import random

import pytest
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

@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = Configuration(host= 'http://5.63.153.31:5025')
    mailhog = MailHogApi(configuration=mailhog_configuration)
    return mailhog

@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = Configuration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMPApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

# @pytest.fixture(scope="session")
# def auth_account_helper(mailhog_api):
#     dm_api_configuration = Configuration(host='http://5.63.153.31:5051', disable_log=False)
#     account = DMPApiAccount(configuration=dm_api_configuration)
#
#     account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
#     account_helper.auth_client(
#         login="testing_131",
#         password='6789012345'
#     )
#
#     return account_helper

@pytest.fixture(scope="function")
def prepare_user():
    suffix = random.randint(0,1000)
    now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    login = f'testing_{now}_{suffix}'
    password = '6789012345'
    email = f"{login}@mail.ru"

    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)

    return user