from collections import namedtuple
from datetime import datetime
import random

from pathlib import Path
from vyper import v

import pytest
import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMPApiAccount

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
)

@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stg", help="run stg")
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)

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
    mailhog_configuration = Configuration(host= v.get("service.mailhog"))
    mailhog = MailHogApi(configuration=mailhog_configuration)
    return mailhog

@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = Configuration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMPApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture(scope="session")
def auth_account_helper(mailhog_api):
    dm_api_configuration = Configuration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DMPApiAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login=v.get("user.login"),
        password=v.get("user.password")
    )

    return account_helper

@pytest.fixture(scope="function")
def prepare_user():
    suffix = random.randint(0,1000)
    now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    login = f'testing_{now}_{suffix}'
    password = v.get("user.password")
    email = f"{login}@mail.ru"

    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)

    return user