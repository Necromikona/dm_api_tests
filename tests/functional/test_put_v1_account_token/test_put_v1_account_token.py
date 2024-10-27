from resource.resource import get_activation_token_by_login, base

from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
import structlog

from restclient.configuration import Configuration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_put_v1_account_token():
    dm_api_configuration = Configuration(host='http://5.63.153.31:5051', disable_log=False, print_curl=True)
    mailhog_configuration = Configuration(host= 'http://5.63.153.31:5025', disable_log=False, print_curl=True)

    account_api= AccountApi(dm_api_configuration)
    mailhog_api= MailhogApi(mailhog_configuration)

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