
def test_put_v1_account_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

    account_helper.change_email_for_user(login=login, password=password, email=f'{login}_changed@mail.ru')

    account_helper.user_login_without_activate(login=login, password=password)

    account_helper.activate_token_for_user(login=login)
    account_helper.user_login(login=login, password=password)

