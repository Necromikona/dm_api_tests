from datetime import datetime

from hamcrest import (
    assert_that,
    starts_with,
    has_property,
    instance_of,
    has_properties,
    all_of,
    equal_to,
    none,
)

from dm_api_account.models.user_envelope import UserRole

class GetV1Account:

    @classmethod
    def check_response_values(
            cls,
            response
            ):
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
                            'info': '',
                            'roles': equal_to([UserRole.GUEST, UserRole.PLAYER])
                        }
                    )
                )
            )
        )