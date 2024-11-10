from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
    equal_to_ignoring_case,
)
from datetime import datetime

from hamcrest.core.core.isnone import (
    IsNone,
    none,
)


def test_get_v1_account_auth(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.auth_client(login=login, password=password)

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
                        'icq':none(),
                        'info': ''

                    }
                )
            )
        )
    )
    print(response)
