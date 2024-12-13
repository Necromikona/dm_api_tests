

import pytest

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
from dm_api_account.models.registration import Registration



def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    registration = Registration(
        login=login,
        email=email,
        password=password,
    )

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)




@pytest.mark.parametrize("login,password,email,error_message,expected_status_code",
                         [
                             ("testing2","pass", "testing2@mail.ru","Validation failed",400),
                             ("testing3","password", "testing","Validation failed",400),
                             ("t","password", "testing4@gmail.com","Validation failed",400)
                         ])
def test_post_v1_account_wit_user_params(
        account_helper, login, password, email, error_message, expected_status_code
):
    login = login
    password = password
    email = email

    registration = Registration(
        login=login,
        email=email,
        password=password,
    )
    with check_status_code_http(expected_status_code, error_message):
        account_helper.dm_account_api.account_api.post_v1_account(registration=registration)
