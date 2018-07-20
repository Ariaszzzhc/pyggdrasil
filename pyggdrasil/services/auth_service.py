import uuid
import time
import json
import base64

from ..utils import mongo, bcrypt
from ..exceptions import ForbiddenOperationException, IllegalArgumentException


def validate_password(account):
    find_user = mongo.db.accounts.find_one({"email": account['username']})
    if find_user is None:
        raise ForbiddenOperationException("Invalid username or password.")

    if not bcrypt.check_password_hash(find_user['password'], account['password']):
        raise ForbiddenOperationException("Invalid username or password.")

    return find_user


def acquire_token(account_id, client_token, selected_profile_id=None):
    access_token = str(uuid.uuid4()).replace('-', '')
    if selected_profile_id is None:
        if mongo.db.profiles.count_documents({'owner': account_id}) == 1:
            bound_profile = mongo.db.profiles.find_one({'owner': account_id})
        else:
            bound_profile = None
    else:
        selected_profile = mongo.db.profiles.find_one({'id': selected_profile_id})
        if not selected_profile['owner'] == account_id:
            raise IllegalArgumentException("the character to select doesn't belong to the user")

        bound_profile = selected_profile

    if client_token is None:
        client_token = str(uuid.uuid4()).replace('-', '')

    if bound_profile is None:
        mongo.db.tokens.insert_one({
            'accessToken': access_token,
            'clientToken': client_token,
            'boundProfile': bound_profile,
            'createdAt': int(time.time()),
            'owner': account_id
        })

        return {
            'accessToken': access_token,
            'clientToken': client_token,
            'boundProfile': bound_profile
        }

    else:
        mongo.db.tokens.insert_one({
            'accessToken': access_token,
            'clientToken': client_token,
            'boundProfile': bound_profile['id'],
            'createdAt': int(time.time()),
            'owner': account_id
        })

        return {
            'accessToken': access_token,
            'clientToken': client_token,
            'boundProfile': serialize_profile(bound_profile)
        }


def available_profiles(account):
    ret = []
    cursor = mongo.db.profiles.find({'owner': account['id']})
    for doc in cursor:
        ret.append(doc)

    return ret


def serialize_account(account, preferred_language=None):
    ret = {
        'id': account['id'],
        'properties': []
    }

    if preferred_language:
        ret['properties'].append(preferred_language)

    return ret


def serialize_profile(profile, properties=False, signature=None):
    ret = {
        'id': profile['id'],
        'name': profile['name']
    }

    if properties:
        ret['properties'] = [
            {
                'name': 'textures',
                'value': None,
            }
        ]

        value = {'timestamp': round(time.time() * 1000),
                 'profileId': profile['id'],
                 'profileName': profile['name'],
                 'textures': {}
                 }
        if not profile['skin'] == '':
            value['textures']['skin'] = {
                'url': profile['skin'],
                'metadata': {
                    'model': profile['model']
                }
            }

        if not profile['cape'] == '':
            value['textures']['cape'] = {
                'url': profile['cape'],
                'metadata': {
                    'model': profile['model']
                }
            }

        value = base64.b64encode(json.dumps(value).encode()).decode()
        ret['properties'][0]['value'] = value

        if signature:
            ret['properties'][0]['signature'] = signature

    return ret


def validate_profile(profile):
    p = mongo.db.profiles.find_one({'id': profile['id']})
    if (p is None) or (p['name'] != profile['name']):
        raise IllegalArgumentException("No such profile.")

    return p


def validate_token(access_token, client_token):
    if access_token is None:
        raise IllegalArgumentException('credentials is null')

    token = mongo.db.tokens.find_one({'accessToken': access_token})
    if token is None:
        raise IllegalArgumentException('Invalid credentials.')

    now = int(time.time())

    if now - token['createdAt'] > 1209600:
        mongo.db.tokens.delete_one({'accessToken': access_token})
        raise ForbiddenOperationException('Invalid credentials.')
    elif now - token['createdAt'] > 604800:
        partial_expired = True
    else:
        partial_expired = False

    if client_token and client_token != token['clientToken']:
        raise ForbiddenOperationException('Invalid credentials.')

    return token, partial_expired

