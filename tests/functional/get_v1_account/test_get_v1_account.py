from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.auth_client(login=login, password=password)

    with check_status_code_http():
        response = account_helper.dm_account_api.account_api.get_v1_account()

    GetV1Account.check_response_values(response)


def test_get_v1_account_no_auth(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.auth_client(login=login, password=password)

    account_helper.dm_account_api.account_api.get_v1_account()
