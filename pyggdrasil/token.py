import uuid
import time

from .exceptions import IllegalArgumentException


def acquire_token(account, client_token, selected_profile=None):
    access_token = str(uuid.uuid4()).replace('-', '')
    if selected_profile is None:
        if len(account['profiles']) == 1:
            bound_profile = account['profiles'][0]['name']
            # TODO 角色信息序列化
        else:
            bound_profile = {}
    else:
        if selected_profile not in account['profiles']:
            raise IllegalArgumentException('Access token already has a profile assigned.')

        bound_profile = selected_profile

    if client_token is None:
        str(uuid.uuid4()).replace('-', '')

    create_time = int(time.time())

    user = account
    # TODO 用户信息序列化

    return {
        "accessToken": access_token,
        "clientToken": client_token,
        "availableProfiles": account['profiles'],
        "selectedProfile": bound_profile,
        "user": user
    }

