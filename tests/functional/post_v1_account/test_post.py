import json

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    account_api= AccountApi(host= 'http://5.63.153.31:5051')
    login_api= LoginApi(host= 'http://5.63.153.31:5051')
    mailhog_api= MailhogApi(host= 'http://5.63.153.31:5025')

    login = 'testing_3'
    password = '6789012345'
    email = f"{login}@mail.ru"
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data)
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