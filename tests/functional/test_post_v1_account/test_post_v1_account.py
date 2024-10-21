from resource.resource import base

from dm_api_account.apis.account_api import AccountApi

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

