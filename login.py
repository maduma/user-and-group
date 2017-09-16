from flask_login import UserMixin
import uuid
import ldap_backend

tokens = {}


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_id(self):
        return self.id


def load_user_from_token(token):
    if token in tokens:
        return User(tokens[token])


def login(username,  password):
    if ldap_backend.check_password(username, password):
        token = str(uuid.uuid4())
        tokens[token] = username
        return {'token': token}
    return {'message': 'access denied'}, 403


def logout(token):
    del tokens[token]
    return {'message': 'logged out successfully'}
