import json
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi

base = 29

def test_post_v1_account():
    account_api= AccountApi(host= 'http://5.63.153.31:5051')

    login = f'testing_{int(base)}'
    password = '6789012345'
    email = f"{login}@mail.ru"

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, "Error create User"

def test_put_v1_account_token():
    account_api= AccountApi(host= 'http://5.63.153.31:5051')
    mailhog_api= MailhogApi(host= 'http://5.63.153.31:5025')

    login = f'testing_{int(base+1)}'
    password = '6789012345'
    email = f"{login}@mail.ru"

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

def test_post_v1_account_login():
    account_api= AccountApi(host= 'http://5.63.153.31:5051')
    login_api= LoginApi(host= 'http://5.63.153.31:5051')
    mailhog_api= MailhogApi(host= 'http://5.63.153.31:5025')

    login = f'testing_{int(base+2)}'
    password = '6789012345'
    email = f"{login}@mail.ru"

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

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "User not authorized"

def test_put_v1_account_email():
    account_api= AccountApi(host= 'http://5.63.153.31:5051')
    login_api= LoginApi(host= 'http://5.63.153.31:5051')
    mailhog_api= MailhogApi(host= 'http://5.63.153.31:5025')

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