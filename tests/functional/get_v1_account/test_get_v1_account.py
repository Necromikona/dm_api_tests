from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
)
from datetime import datetime

from hamcrest.core.core.isnone import (
    none,
)

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

    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with("testing_"))),
            has_property('resource', has_property('online', instance_of(datetime))),
            has_property(
                'resource', has_properties(
                    {
                        'rating': has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        ),
                        'icq': none(),
                        'info': ''

                    }
                )
            )
        )
    )


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
