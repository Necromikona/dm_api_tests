from dm_api_account.models.registration import Registration


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    registration = Registration(
        login=login,
        email=email,
        password=password,
    )

    account_helper.dm_account_api.account_api.post_v1_account(registration=registration)


