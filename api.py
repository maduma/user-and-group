from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_login import LoginManager, login_required, current_user
import login
import ldap_backend
import os


app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('token')
    return login.load_user_from_token(token)


class Group1(Resource):
    def get(self):
        return ldap_backend.get_groups()


class Group2(Resource):
    def get(self, group_id):
        return ldap_backend.get_group(group_id)

    @login_required
    def put(self, group_id):
        return ldap_backend.create_group(group_id)

    @login_required
    def delete(self, group_id):
        return ldap_backend.delete_group(group_id)


class Group3(Resource):
    def get(self, group_id):
        return ldap_backend.get_group_users(group_id)


class Group4(Resource):
    @login_required
    def put(self, group_id, user_id):
        return ldap_backend.add_user_in_group(user_id, group_id)

    @login_required
    def delete(self, group_id, user_id):
        return ldap_backend.delete_user_from_group(user_id, group_id)


class Users1(Resource):
    def get(self):
        return ldap_backend.get_users()


class Users2(Resource):
    def get(self, user_id):
        return ldap_backend.get_user(user_id)


class Users3(Resource):
    def get(self, user_id):
        return ldap_backend.get_user_groups(user_id)

class Users4(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('filter', required=True)

    def get(self):
        args = self.parser.parse_args()
        substring = args['filter']
        if len(substring) < 3:
            return {'message': 'filter should have a least 3 char'}, 400
        return ldap_backend.find_ldap_users('(uid=*' + substring + '*)')

class Login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        args = self.parser.parse_args()
        return login.login(args['username'], args['password'])


class Logout(Resource):
    @login_required
    def get(self):
        token = request.headers.get('token')
        return login.logout(token)


api.add_resource(Group1, '/groups')
api.add_resource(Group2, '/groups/<string:group_id>')
api.add_resource(Group3, '/groups/<string:group_id>/users')
api.add_resource(Group4, '/groups/<string:group_id>/users/<string:user_id>')
api.add_resource(Users1, '/users')
api.add_resource(Users2, '/users/<string:user_id>')
api.add_resource(Users3, '/users/<string:user_id>/groups')
api.add_resource(Users4, '/ldapusers')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    if os.environ.get('PRODUCTION'):
        app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
