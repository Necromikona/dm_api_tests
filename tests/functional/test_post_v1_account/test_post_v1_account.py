def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    account_helper.dm_account_api.account_api.post_v1_account(json_data=json_data)


