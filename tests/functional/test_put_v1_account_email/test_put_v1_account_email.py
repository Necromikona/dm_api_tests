from resource.resource import get_activation_token_by_login, base

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration

import structlog

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
    dm_api_configuration = Configuration(host='http://5.63.153.31:5051', disable_log=False, print_curl=True)
    mailhog_configuration = Configuration(host= 'http://5.63.153.31:5025', disable_log=False, print_curl=True)

    account_api= AccountApi(dm_api_configuration)
    login_api= LoginApi(dm_api_configuration)
    mailhog_api= MailhogApi(mailhog_configuration)

    login = f'testing_{int(base+3)}'
    password = '6789012345'
    email = f"{login}@mail.ru"
    login_json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, "Error create User"

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, f"Error. E-mail not found for {login}"

    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Not found token for {login}"

    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "User not activate"

    response = login_api.post_v1_account_login(json_data=login_json_data)
    assert response.status_code == 200, "User not authorized"

    json_data = {
        'login': login,
        'password': password,
        'email' : f'{login}_changed@mail.ru'
    }
    response = account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, f"Not change email for User {login}"

    #  Проверка, что не можем залогиниться, если не активирован новый почтовый ящик
    response = login_api.post_v1_account_login(json_data=login_json_data)
    assert response.status_code == 403, "Authorize user without activate email"

    # Получение последних сообщений
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, f"Error. E-mail not found for {login}"

    # Поиск по логину
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Not found token for {login}"

    # Активация нового токена
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "User not activate"

    # Логин
    response = login_api.post_v1_account_login(json_data=login_json_data)
    assert response.status_code == 200, "User not authorized"
