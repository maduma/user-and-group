from flask_login import UserMixin
import uuid

tokens = {}


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_id(self):
        return id


def load_user_from_token(request):
    token = request.headers.get('token')
    if token in tokens:
        return User(tokens[token])


def login(username,  password):
    if username == 'snsakala' and password == 'Luxair123':
        token = str(uuid.uuid4())
        tokens[token] = 'snsakala'
        return {'token': token}
    return {'message': 'access denied'}, 403


def logout(request):
    token = request.headers.get('token')
    if token:
        del tokens[token]
        return {'message': 'logged out successfully'}
    return {'message': 'cannot found the token'}, 500