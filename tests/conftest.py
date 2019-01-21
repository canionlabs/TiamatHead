from django.utils import timezone

from apps.common.utils.base_tests import BaseTest, UserModel, \
    AccessToken, Application

import datetime
import pytest
import uuid


@pytest.fixture(scope='class')
def oauth_user(request):
    user = UserModel.objects.create_user(
        username=request.instance.random_string(),
        email=request.instance.random_email(),
        password=request.instance.random_string()
    )

    non_user = UserModel.objects.create_user(
        username=request.instance.random_string(),
        email=request.instance.random_email(),
        password=request.instance.random_string()
    )

    application = Application(
            name=request.instance.random_string(),
            user=user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
    )
    application.save()

    valid_user_token = AccessToken.objects.create(
        user=user, token=uuid.uuid4().hex,
        application=application,
        expires=timezone.now() + datetime.timedelta(days=1),
        scope="read write dolphin"
    )

    valid_non_user_token = AccessToken.objects.create(
        user=non_user, token=uuid.uuid4().hex,
        application=application,
        expires=timezone.now() + datetime.timedelta(days=1),
        scope="read write dolphin"
    )

    request.cls.user = user
    request.cls.user_header = f"Bearer {valid_user_token.token}"

    request.cls.non_user = non_user
    request.cls.non_user_header = f"Bearer {valid_non_user_token.token}"
